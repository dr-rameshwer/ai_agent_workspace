from typing import List
from pydantic import BaseModel, Field

class ConceptCard(BaseModel):
    term: str = Field(description="The key technical term, formula, or concept")
    definition: str = Field(description="Clear, concise 1-2 sentence definition")
    example: str = Field(description="A practical real-world example or use case")

class SessionSummary(BaseModel):
    subject: str = Field(description="The primary subject analyzed")
    key_takeaways: List[str] = Field(description="3-5 core bullet points learned")
    cards: List[ConceptCard] = Field(description="List of 3-5 concept cards for review")