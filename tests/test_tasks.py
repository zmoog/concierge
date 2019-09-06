import datetime


def test_happy_path(ifq2dropbox):
        
    ifq2dropbox.execute(datetime.date.today())

