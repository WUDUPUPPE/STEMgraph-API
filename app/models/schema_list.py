from pydantic import BaseModel, Field
  
#All Challenges AS List
class ChallengeListResponse(BaseModel):
    id: str
    teaches: str | None = None
    keywords: list[str] = Field(default_factory=list)

#Challenges Dependency AS List
class DependencyResponse(BaseModel):
    id: str
    teaches: str | None = None
    keywords: list[str] = Field(default_factory=list)

#Subgraph AS List
class SubgraphListResponse(BaseModel):
    id: str
    teaches: str 
    keywords: list[str] = Field(default_factory=list)
    
#Challenge Previous and Next for Pop-Up
class NeighborChallenge(BaseModel):
    id: str
    teaches: str | None = None
    keywords: list[str] = Field(default_factory=list)

class NeighborsResponse(BaseModel):
    previous: list[NeighborChallenge] = Field(default_factory=list)
    next: list[NeighborChallenge] = Field(default_factory=list)
