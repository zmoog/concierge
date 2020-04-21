import datetime
from typing import Optional


def find_previous_business_day(day: Optional[datetime.date] = None):
    """Find the previous business day of the given date.

    The current definition of 'business day' is quite simple
    and limited to week days between mon-fri. It doesn't
    consider holidays at all (it can be a future improvement).

    :param day: the date of the given day. :return: a date object
    of the previous business day (see the description above
    for a devinition of the 'business day' term.
    """
    business_days = [0, 1, 2, 3, 4]  # Monday to Friday

    previous_day = day or datetime.date.today() - datetime.timedelta(days=1)

    while previous_day.weekday() not in business_days:
        previous_day -= datetime.timedelta(days=1)

    return previous_day
