from dataclasses import dataclass


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
    error: Exception


@dataclass
class RefurbishedProductAvailable(Event):
    text: str
