
#All Challenges AS Graph
all_nodes_query = """
MATCH (c:Challenge)
RETURN DISTINCT c.id AS id, c.teaches AS teaches, c.keywords AS keywords, c.author AS author, c.firstused AS firstused
"""

all_edges_query = """
MATCH (c:Challenge)-[:DEPENDS_ON]->(dep:Challenge)
RETURN DISTINCT c.id AS source, dep.id AS target
"""

#Dependency Challenges AS Graph
dep_node_query = """
MATCH (c:Challenge {id: $id})
RETURN DISTINCT c.id AS id, c.teaches AS teaches, c.keywords AS keywords
UNION
MATCH (c:Challenge {id: $id})-[:BUILDS_ON*]->(dep:Challenge)
RETURN DISTINCT dep.id AS id, dep.teaches AS teaches, dep.keywords AS keywords
"""

dep_edge_query = """
MATCH (c:Challenge {id: $id})-[:DEPENDS_ON*]->(a:Challenge)
MATCH (a)-[:DEPENDS_ON]->(b:Challenge)
RETURN DISTINCT a.id AS source, b.id AS target
"""

#Subgraph Path AS Graph
sub_node_query = """
MATCH path = shortestPath(
    (a:Challenge {id: $start})-[:DEPENDS_ON*]-(b:Challenge {id: $end})
)
UNWIND nodes(path) AS node
RETURN DISTINCT node.id AS id, node.teaches AS teaches, node.keywords AS keywords
"""

sub_edge_query = """
MATCH path = shortestPath(
    (a:Challenge {id: $start})-[:DEPENDS_ON*]-(b:Challenge {id: $end})
)
UNWIND relationships(path) AS rel
RETURN DISTINCT startNode(rel).id AS source, endNode(rel).id AS target
"""

#Neighbor Challenges for Pop-Up-Info
center_query = """
MATCH (c:Challenge {id: $id})
RETURN c.id AS id, c.teaches AS teaches, c.keywords AS keywords
"""

previous_query = """
MATCH (prev:Challenge)-[:DEPENDS_ON]->(c:Challenge {id: $id})
RETURN prev.id AS id, prev.teaches AS teaches, prev.keywords AS keywords
"""

next_query = """
MATCH (c:Challenge {id: $id})-[:DEPENDS_ON]->(next:Challenge)
RETURN next.id AS id, next.teaches AS teaches, next.keywords AS keywords
ORDER BY next.teaches
"""