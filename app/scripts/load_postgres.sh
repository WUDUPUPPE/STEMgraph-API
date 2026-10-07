#!/usr/bin/env bash
# load_content_postgres.sh
# Liest README.md (ohne JSON-Block) und assets/ aller lokalen Challenges und lädt sie nach PostgreSQL
# Erwartet: POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
API_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
WORKSPACE_DIR="$(cd "$API_ROOT/.." && pwd)"
DATA_DIR="$WORKSPACE_DIR/data"
mkdir -p "$DATA_DIR"

BASE_DIR="$WORKSPACE_DIR/challenges"
STATS_FILE="$DATA_DIR/stats_content.json"

if [[ ! -d "$BASE_DIR" ]]; then
  echo "FEHLER: Basisverzeichnis '$BASE_DIR' nicht gefunden."
  echo "Bitte vorher 'get_all_challenges.sh' ausführen."
  exit 1
fi

: "${POSTGRES_HOST:?FEHLER: POSTGRES_HOST ist nicht gesetzt}"
: "${POSTGRES_PORT:=5432}"
: "${POSTGRES_DB:?FEHLER: POSTGRES_DB ist nicht gesetzt}"
: "${POSTGRES_USER:?FEHLER: POSTGRES_USER ist nicht gesetzt}"
: "${POSTGRES_PASSWORD:?FEHLER: POSTGRES_PASSWORD ist nicht gesetzt}"

export BASE_DIR STATS_FILE POSTGRES_HOST POSTGRES_PORT POSTGRES_DB POSTGRES_USER POSTGRES_PASSWORD

echo "Lade README und Assets aus '$BASE_DIR' nach PostgreSQL ($POSTGRES_HOST)..."

python3 - << 'PY'
import os
import re
import json
import uuid
import hashlib
import mimetypes
import subprocess
import psycopg

base_dir = os.environ["BASE_DIR"]
stats_file = os.environ["STATS_FILE"]

MAX_ASSET_BYTES = 10 * 1024 * 1024          # einzelne Datei max. 10 MB, sonst überspringen
IGNORE_FILES = {".DS_Store", ".gitkeep"}    # Dateien, die keine echten Assets sind

# JSON-Kommentarblock <!--- ... ---> (gleiche Marker wie in den anderen Scripts)
META_RE = re.compile(r"<!---(.*?)--->", re.DOTALL)

conn = psycopg.connect(
    host=os.environ["POSTGRES_HOST"],
    port=os.environ["POSTGRES_PORT"],
    dbname=os.environ["POSTGRES_DB"],
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS readmes (
    challenge_id     UUID PRIMARY KEY,
    content_markdown TEXT NOT NULL,
    content_hash     TEXT NOT NULL,
    source_commit    TEXT,
    imported_at      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS assets (
    id            BIGSERIAL PRIMARY KEY,
    challenge_id  UUID NOT NULL REFERENCES readmes(challenge_id) ON DELETE CASCADE,
    file_name     TEXT NOT NULL,
    relative_path TEXT NOT NULL,
    mime_type     TEXT,
    file_size     BIGINT NOT NULL,
    content       BYTEA NOT NULL,
    UNIQUE (challenge_id, relative_path)
);
"""
with conn.transaction():
    conn.execute(SCHEMA)


def git_head(repo_dir):
    try:
        return subprocess.check_output(
            ["git", "-C", repo_dir, "rev-parse", "HEAD"], stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return None


def split_readme(path):
    """Gibt (meta_dict, readme_ohne_json_block) zurück oder (None, None)."""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    m = META_RE.search(text)
    if not m:
        return None, None
    try:
        meta = json.loads(m.group(1).strip())
    except Exception:
        return None, None
    clean = (text[:m.start()] + text[m.end():]).lstrip("\n").strip() + "\n"
    return meta, clean


def collect_assets(repo_dir):
    assets_dir = os.path.join(repo_dir, "assets")
    result = []
    if not os.path.isdir(assets_dir):
        return result
    for root, _dirs, files in os.walk(assets_dir):
        for name in sorted(files):
            if name in IGNORE_FILES:
                continue
            full = os.path.join(root, name)
            size = os.path.getsize(full)
            if size > MAX_ASSET_BYTES:
                print(f"    WARNUNG: '{full}' ist {size} Bytes groß, übersprungen")
                continue
            with open(full, "rb") as f:
                data = f.read()
            rel = os.path.relpath(full, repo_dir).replace(os.sep, "/")
            mime = mimetypes.guess_type(name)[0] or "application/octet-stream"
            result.append((name, rel, mime, size, data))
    result.sort(key=lambda a: a[1])
    return result


def make_hash(readme, assets):
    h = hashlib.sha256()
    h.update(readme.encode("utf-8"))
    for _name, rel, _mime, _size, data in assets:
        h.update(rel.encode("utf-8"))
        h.update(hashlib.sha256(data).digest())
    return h.hexdigest()


imported = skipped = unchanged = asset_count = 0

for entry in sorted(os.listdir(base_dir)):
    repo_dir = os.path.join(base_dir, entry)
    readme_path = os.path.join(repo_dir, "README.md")
    if not os.path.isdir(repo_dir) or not os.path.isfile(readme_path):
        continue

    meta, readme = split_readme(readme_path)
    if not meta:
        skipped += 1
        continue

    try:
        cid = str(uuid.UUID(str(meta.get("id", entry))))
    except ValueError:
        print(f"    WARNUNG: Ungültige Challenge-ID in '{entry}', übersprungen")
        skipped += 1
        continue

    assets = collect_assets(repo_dir)
    new_hash = make_hash(readme, assets)

    with conn.transaction():
        row = conn.execute(
            "SELECT content_hash FROM readmes WHERE challenge_id = %s", (cid,)
        ).fetchone()
        if row and row[0] == new_hash:
            unchanged += 1
            continue

        conn.execute(
            """
            INSERT INTO readmes (challenge_id, content_markdown, content_hash, source_commit, imported_at)
            VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (challenge_id) DO UPDATE
            SET content_markdown = EXCLUDED.content_markdown,
                content_hash     = EXCLUDED.content_hash,
                source_commit    = EXCLUDED.source_commit,
                imported_at      = CURRENT_TIMESTAMP
            """,
            (cid, readme, new_hash, git_head(repo_dir)),
        )
        conn.execute("DELETE FROM assets WHERE challenge_id = %s", (cid,))
        for name, rel, mime, size, data in assets:
            conn.execute(
                """
                INSERT INTO assets (challenge_id, file_name, relative_path, mime_type, file_size, content)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (cid, name, rel, mime, size, data),
            )
        imported += 1
        asset_count += len(assets)

conn.close()

with open(stats_file, "w", encoding="utf-8") as f:
    json.dump(
        {"imported": imported, "unchanged": unchanged, "skipped": skipped, "assets": asset_count},
        f, indent=2,
    )

print(f"Fertig. {imported} importiert, {unchanged} unverändert, {skipped} übersprungen, {asset_count} Assets geladen.")
PY

echo "PostgreSQL-Import abgeschlossen."