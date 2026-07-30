from pydantic import BaseModel, Field

class ChallengeListResponse(BaseModel):
    uuid: str
    title: str | None = None
    keywords: list[str] = Field(default_factory=list)

class DependencyResponse(BaseModel):
    uuid: str
    title: str | None = None
    keywords: list[str] = Field(default_factory=list)

class GraphNodeResponse(BaseModel):
    uuid: str
    title: str | None = None

class GraphEdgeResponse(BaseModel):
    source: str
    target: str

class DependencyGraphResponse(BaseModel):
    nodes: list[GraphNodeResponse] = Field(default_factory=list)
    edges: list[GraphEdgeResponse] = Field(default_factory=list)
    
class NeighborChallenge(BaseModel):
    uuid: str
    title: str | None = None
    keywords: list[str] = Field(default_factory=list)

class NeighborsResponse(BaseModel):
    previous: list[NeighborChallenge] = Field(default_factory=list)
    next: list[NeighborChallenge] = Field(default_factory=list)
    
class SubgraphListResponse(BaseModel):
    uuid: str
    title: str 
    keywords: list[str] = Field(default_factory=list)