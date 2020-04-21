import datetime


def test_find_previous_business_day__simple(summary_intent):

    thursday = datetime.date(2019, 9, 12)
    friday = datetime.date(2019, 9, 13)

    previous_business_day = summary_intent._find_previous_business_day(friday)

    assert previous_business_day == thursday


def test_find_previous_business_day__cross_weekend(summary_intent):

    friday = datetime.date(2019, 9, 13)
    monday = datetime.date(2019, 9, 16)

    previous_business_day = summary_intent._find_previous_business_day(monday)

    assert previous_business_day == friday
