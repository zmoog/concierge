"""
https://www.dropbox.com/developers/documentation/python
https://dropbox-sdk-python.readthedocs.io/en/latest/
"""
import dropbox


class DropboxAdapter:

    def __init__(self, root_folder: str, access_token: str):
        self.root_folder = root_folder
        self.client = dropbox.Dropbox(access_token)

    def exists(self, key: str):
        # print('checking for {folder}/{key}'.format(key=key, folder=self.root_folder))
        return self.client.files_search(self.root_folder, key).matches

    def put_file(self, file_path: str, file_name: str):
        with open(file_path, "rb") as f:
            self.client.files_upload(f.read(), '%s/%s' % (self.root_folder, file_name), mute = True)
