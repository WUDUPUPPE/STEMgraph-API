
#Keywords AS List
key_list_query = """
MATCH (c:Challenge)
UNWIND c.keywords AS keywords
RETURN DISTINCT keywords
"""

#Challenges by Keyword AS List
chal_by_key_list_query = """
MATCH (c:Challenge)
WHERE $kw IN c.keywords
RETURN c.id AS id, c.teaches AS teaches, c.keywords AS keywords
"""

#Keywords AS Graph
key_graph_query = """
MATCH (c:Challenge)
UNWIND c.keywords AS keywords
RETURN DISTINCT c.id AS id, keywords AS keywords
"""

#Challenges by Keyword AS Graph
chal_by_key_graph_node_query = """
MATCH (c:Challenge)
WHERE $kw IN c.keywords
RETURN DISTINCT c.id AS id, c.teaches AS teaches, c.keywords AS keywords
"""

chal_by_key_graph_edge_query = """
MATCH (a:Challenge)-[:DEPENDS_ON]->(b:Challenge)
WHERE $kw IN a.keywords AND $kw IN b.keywords
RETURN DISTINCT a.id AS source, b.id AS target
"""