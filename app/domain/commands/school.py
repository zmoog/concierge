from datetime import date

from . import Command


class ListHomework(Command):
    since: date
    until: date
