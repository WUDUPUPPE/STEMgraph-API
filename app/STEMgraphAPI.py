import typer
import uvicorn
from app.main import app

cli = typer.Typer()

@cli.command()
def run(
    neo4j_user: str = typer.Option(..., envvar="NEO4J_USER"),
    neo4j_pw: str = typer.Option(..., envvar="NEO4J_PW"),
    write_token: str = typer.Option(..., envvar="WRITE_TOKEN"),
    host: str = "0.0.0.0",
    port: int = 8000,
):
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    cli()