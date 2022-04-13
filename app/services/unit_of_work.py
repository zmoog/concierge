from app.adapters import (
    apple,
    classeviva,
    dropbox,
    ifq,
    slack,
    telegram,
    toggl,
)


class UnitOfWork:
    def __init__(
        self,
        refurbished: apple.RefurbishedStoreAdapter,
        classeviva: classeviva.ClassevivaAdapter,
        dropbox: dropbox.DropboxAdapter,
        ifq: ifq.IFQAdapter,
        slack: slack.SlackAdapter,
        telegram: telegram.TelegramAdapter,
        toggl: toggl.TogglAdapter,
    ):
        self.refurbished = refurbished
        self.classeviva = classeviva
        self.dropbox = dropbox
        self.ifq = ifq
        self.slack = slack
        self.telegram = telegram
        self.toggl = toggl

    def __enter__(self):
        pass

    def __exit__(self, *args):
        pass  # super().__exit__(*args)
