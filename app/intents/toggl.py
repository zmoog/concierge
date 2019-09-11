class TogglSummary(object):
    
    def __init__(self, toggl_service):
        self.toggl = toggl_service

    def execute(self, execution_id: str, entities: dict):

        summary = self.toggl.summary(entities["since"], entities["until"])

        print(summary)

        return {
            "title": "fake",
            "text": "fake",
            "attachments": ["fake"]
        }
