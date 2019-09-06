import datetime

today = datetime.date.today()


def test_exists_for_failure(dropbox):
    assert not dropbox.exists('how-to-enlarge-your-penis.pdf')

def test_exists_for_success(dropbox):
    filename = today.strftime('ilfatto-%Y%m%d.pdf')
    assert dropbox.exists(filename)    