readme_query = """
SELECT challenge_id, content_markdown, source_path, source_commit,  imported_at
FROM readmes
WHERE challenge_id = %s
"""


assets_query = """
SELECT id, file_name, relative_path, mime_type, file_size
FROM assets
WHERE challenge_id = %s
ORDER BY relative_path
"""


asset_content_query = """
SELECT content, file_name, mime_type
FROM assets
WHERE id = %s
  AND challenge_id = %s
"""