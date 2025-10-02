from typing import List, Literal, Optional
from pydantic import BaseModel


TopicName = Literal[
    "Research & Prevention",
    "Early Detection and Diagnosis",
    "Drug Discovery and Development",
    "Treatment Methods",
    "Precision Oncology",
]


class NewsItem(BaseModel):
    title: str
    url: str
    publish_date: Optional[str] = None
    snippet: Optional[str] = None


class TopicItems(BaseModel):
    topic: TopicName
    items: List[NewsItem]


class FetchResult(BaseModel):
    topics: List[TopicItems]


class TopicSummary(BaseModel):
    topic: TopicName
    summary: str
    bullets: List[str] = []


class SummariesOutput(BaseModel):
    overview: str
    topics: List[TopicSummary]


