from pydantic import BaseModel

#All Challenges AS Graph
class Node(BaseModel):
    uuid: str
    title: str | None = None

class Edge(BaseModel):
    source: str
    target: str

class GraphResponse(BaseModel):
    nodes: list[Node]
    edges: list[Edge]

#Challenges Dependency AS Graph
class GraphNodeResponse(BaseModel):
    uuid: str
    title: str | None = None

class GraphEdgeResponse(BaseModel):
    source: str
    target: str

class DependencyGraphResponse(BaseModel):
    nodes: list[GraphNodeResponse] = Field(default_factory=list)
    edges: list[GraphEdgeResponse] = Field(default_factory=list)

#Subgraph AS Graph
class GraphNode(BaseModel):
    uuid: str
    title: str | None = None
    keywords: list[str] = Field(default_factory=list)

class GraphEdge(BaseModel):
    source: str
    target: str

class SubgraphGraphResponse(BaseModel):
    nodes: list[GraphNode] = Field(default_factory=list)
    edges: list[GraphEdge] = Field(default_factory=list)

