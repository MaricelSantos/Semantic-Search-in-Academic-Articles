from pydantic import BaseModel


class SearchResponse(BaseModel):
    ID: str
    title: str
    author: str
    abstract: str
    similarity_score: float