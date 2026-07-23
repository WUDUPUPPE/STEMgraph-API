import os
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "bolt://neo4j:7678",
    auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PW"))
)

def run_query(query, params=None):
    with driver.session() as session:
        result = session.run(query, params or {})
        return [record.data() for record in result]