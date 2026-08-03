from pydantic import BaseModel, Field

#Keyword AS Graph
class KeywordsResponse(BaseModel):
    uuid: str 
    keywords: list[str] = Field(default_factory=list)