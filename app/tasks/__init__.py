class Ifq2DropboxTask(object):
    
    def __init__(self, ifqService, dropboxService):
        self.ifq = ifqService
        self.dropbox = dropboxService

    def execute(self, pub_date, filename_pattern='ilfatto-%Y%m%d.pdf'):

        local_file_path = self.ifq.download_pdf(pub_date)

        filename = pub_date.strftime(filename_pattern)

        self.dropbox.put_file(local_file_path, filename)
