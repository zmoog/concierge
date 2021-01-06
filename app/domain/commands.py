# pylint: disable=too-few-public-methods
from datetime import date
from typing import List  # Optional
# from dataclasses import dataclass
# from pydantic import BaseModel
# from pydantic.dataclasses import dataclass
from pydantic import BaseModel


class Command(BaseModel):
    pass


class Summarize(Command):
    day: date


class SummarizeWorkTypes(Command):
    since: date
    until: date
    project_ids: List[str] = None


class DownloadIFQ(Command):
    day: date


class CheckRefurbished(Command):
    store: str
    products: List[str]
