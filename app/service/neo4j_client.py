import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PW"))
)

def run_query(query, params=None):
    with driver.session(database=os.getenv("NEO4J_DB", "neo4j")) as session:
        result = session.run(query, params or {})
        return [record.data() for record in result]