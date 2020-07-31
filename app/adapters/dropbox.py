"""
https://www.dropbox.com/developers/documentation/python
https://dropbox-sdk-python.readthedocs.io/en/latest/
"""
import dropbox


class DropboxAdapter:

    def __init__(self, root_folder: str, access_token: str):
        self.root_folder = root_folder
        self.client = dropbox.Dropbox(access_token)

    def exists(self, query: str) -> bool:
        options = dropbox.files.SearchOptions(
            path=self.root_folder
        )
        return len(self.client.files_search_v2(query, options).matches) > 0

    def put_file(self, file_path: str, file_name: str):
        with open(file_path, "rb") as f:
            self.client.files_upload(
                f.read(),
                f'{self.root_folder}/{file_name}',
                mute=True
            )
