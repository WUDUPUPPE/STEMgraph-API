from pydantic import BaseModel, Field
  
#All Challenges AS List
class ChallengeListResponse(BaseModel):
    id: str
    teaches: str | None = None
    keywords: list[str] = Field(default_factory=list)
    author: list[str] | str | None = None
    firstused: str | None = None

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
