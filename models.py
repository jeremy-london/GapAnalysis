from typing import List

from pydantic import BaseModel


class Entity(BaseModel):
    """Represents an entity with an ID, name, summary, and sources."""
    id: int
    name: str
    summary: str
    sources: List[str]

class Relationship(BaseModel):
    """Defines a relationship between two entities."""
    id: int
    name: str
    start_entity_id: int
    start_entity_name: str
    end_entity_id: int
    end_entity_name: str
    summary: str
