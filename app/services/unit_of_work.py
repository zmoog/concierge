from app.adapters import apple, dropbox, ifq, slack, toggl


class UnitOfWork:
    def __init__(
        self,
        toggl: toggl.TogglAdapter,
        ifq: ifq.IFQAdapter,
        dropbox: dropbox.DropboxAdapter,
        slack: slack.SlackAdapter,
        refurbished: apple.RefurbishedStoreAdapter,
    ):
        self.dropbox = dropbox
        self.ifq = ifq
        self.toggl = toggl
        self.slack = slack
        self.refurbished = refurbished

    def __enter__(self):
        pass

    def __exit__(self, *args):
        pass  # super().__exit__(*args)
