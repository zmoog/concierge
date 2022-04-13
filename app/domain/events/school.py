from dataclasses import dataclass
from typing import List

from app.domain.model.school import Assignment

from . import Event


@dataclass
class NoHomework(Event):
    days: int


@dataclass
class HomeworkAvailable(Event):
    assignments: List[Assignment]
    days: int
