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
    filename: str
    error: Exception
    traceback: str


@dataclass
class RefurbishedProductAvailable(Event):
    text: str
