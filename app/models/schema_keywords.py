from pydantic import BaseModel, Field

#Keywords AS List
class KeywordListResponse(BaseModel):
    keywords: list[str] = Field(default_factory=list)

#Challenges by Keyword AS List
class ChallengeByKeywordListItem(BaseModel):
    id: str
    teaches: str | None = None
    keywords: list[str] = Field(default_factory=list)

class ChallengesByKeywordListResponse(BaseModel):
    items: list[ChallengeByKeywordListItem] = Field(default_factory=list)

#Keywords AS Graph
class KeywordNode(BaseModel):
    keywords: str

class KeywordEdge(BaseModel):
    id: str
    keywords: str

class KeywordGraphResponse(BaseModel):
    nodes: list[KeywordNode] = Field(default_factory=list)
    edges: list[KeywordEdge] = Field(default_factory=list)
    
#Challenges by Keyword AS Graph
class ChallengeNode(BaseModel):
    id: str
    teaches: str | None = None
    keywords: list[str] = Field(default_factory=list)

class ChallengeEdge(BaseModel):
    source: str
    target: str

class ChallengesByKeywordGraphResponse(BaseModel):
    nodes: list[ChallengeNode] = Field(default_factory=list)
    edges: list[ChallengeEdge] = Field(default_factory=list)