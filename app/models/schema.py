from pydantic import BaseModel, Field

#All Challenges AS List
class ChallengeListResponse(BaseModel):
    uuid: str
    title: str | None = None
    keywords: list[str] = Field(default_factory=list)

#Challenges Dependency AS List
class DependencyResponse(BaseModel):
    uuid: str
    title: str | None = None
    keywords: list[str] = Field(default_factory=list)

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

#Challenge Previous and Next for Pop-Up
class NeighborChallenge(BaseModel):
    uuid: str
    title: str | None = None
    keywords: list[str] = Field(default_factory=list)

class NeighborsResponse(BaseModel):
    previous: list[NeighborChallenge] = Field(default_factory=list)
    next: list[NeighborChallenge] = Field(default_factory=list)

#Subgraph AS List
class SubgraphListResponse(BaseModel):
    uuid: str
    title: str 
    keywords: list[str] = Field(default_factory=list)

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