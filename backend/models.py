from pydantic import BaseModel
from typing import List

class TimeBlock(BaseModel):
    task: str
    start_time: str
    end_time: str

class ProductivityInput(BaseModel):
    goals: List[str]
    available_hours: int
    distractions: List[str]
    start_time: str       # added feature(e.g. "09:00")
    energy_level: str     # added feature ("high" | "medium" | "low")

class ProductivityPlan(BaseModel):
    priority_order: List[str]
    schedule: List[TimeBlock]
    tips: List[str]


