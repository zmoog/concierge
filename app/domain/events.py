from dataclasses import dataclass
from typing import List

from app.domain.model import Product


class Event:
    pass


@dataclass
class TogglEntriesSummarized(Event):
    summary: str


@dataclass
class IFQIssueDownloaded(Event):
    filename: str


@dataclass
class IFQIssueAlreadyExists(Event):
    filename: str


@dataclass
class IFQIssueDownloadFailed(Event):
    filename: str
    error: Exception
    traceback: str


@dataclass
class RefurbishedProductAvailable(Event):
    store: str
    product: str
    products: List[Product]


@dataclass
class RefurbishedProductNotAvailable(Event):
    store: str
    product: str
