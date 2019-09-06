import os
import datetime
from PyPDF4 import PdfFileReader

from app.services.ifq import IFQ

today = datetime.date.today()


# def test_exists_for_failure(archiver):
#     assert not archiver.exists('how-to-enlarge-your-penis.pdf')

def test_download(ifq):
    # filename = today.strftime('ilfatto-%Y%m%d.pdf')

    # tmp_file = ifq.download_pdf(today)
    tmp_file = '/var/folders/vl/dc89lvrs3xn9xf55xgwzm6n5fdnj16/T/tmp2c5ez2az'
    print(tmp_file)

    assert os.path.exists(tmp_file)

    # check file size
    stat = os.stat(tmp_file)
    assert stat.st_size > 5 * 1024 * 1024, 'The PDF file size does not reach the minimum value'

    # check is a real PDF file
    with open(tmp_file, 'rb') as file:
        doc = PdfFileReader(file)
        print(dir(doc))
        print(doc.documentInfo)

        assert doc.numPages > 15
    # assert ifq.download_pdf(today)