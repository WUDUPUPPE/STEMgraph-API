import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PW"))
)

def run_query(query, params=None):
    print("NEO4J_URI =", os.getenv("NEO4J_URI"))
    print("NEO4J_DB =", os.getenv("NEO4J_DB"))
    print("QUERY =", query)
    print("NEO4J_DB raw =", os.getenv("NEO4J_DB"))
    print("NEO4J_DB effective =", os.getenv("NEO4J_DB", "neo4j"))

    with driver.session(database=os.getenv("NEO4J_DB", "neo4j")) as session:
        result = session.run(query, params or {})
        data = [record.data() for record in result]
        print("RESULT =", data[:5])
        return data