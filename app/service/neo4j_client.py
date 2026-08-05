import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PW"))
)

def run_query(query, params=None):
    """
    Execute a Cypher query against the Neo4j database.
    
    query: The Cypher query string.
    params: Optional dictionary of parameters for the query.
    driver: A Neo4j driver object for connecting to the database.
    with driver.session(): Creates a new session for executing queries.
    session: A Neo4j session object for executing queries.
    session.run(): Executes the query and returns a result object.
    record: Each record is a dictionary with keys corresponding to the query's return values.
    record.data(): Returns the data of the record as a dictionary.
    return: List of dictionaries representing query results.
    """
    with driver.session(database=os.getenv("NEO4J_DB", "neo4j")) as session:
        result = session.run(query, params or {})
        return [record.data() for record in result]