from typing import Optional

from sqlmodel import SQLModel, Field


class BaitBase(SQLModel):
    name: str = Field(nullable=False)
    content: str = Field(nullable=False)

class Bait(BaitBase, table=True):
    __tablename__ = "bait"
    __table_args__ = {"extend_existing": True}
    id: Optional[int] = Field(default=None, primary_key=True)
