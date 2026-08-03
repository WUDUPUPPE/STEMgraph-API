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

#Subgraph AS List
class SubgraphListResponse(BaseModel):
    uuid: str
    title: str 
    keywords: list[str] = Field(default_factory=list)
