# pylint: disable=too-few-public-methods
from datetime import date
from typing import List  # Optional

# from dataclasses import dataclass
# from pydantic import BaseModel
# from pydantic.dataclasses import dataclass
from pydantic import BaseModel


class Command(BaseModel):
    pass


# @dataclass
class Summarize(Command):
    day: date


# @dataclass
class DownloadIFQ(Command):
    day: date


# @dataclass
class CheckRefurbished(Command):
    store: str
    products: List[str]
