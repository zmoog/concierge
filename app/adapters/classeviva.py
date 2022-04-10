from datetime import datetime, timedelta
from typing import List

from classeviva.client import Client
from classeviva.credentials import EnvCredentialsProvider

from app.domain.model.school import Assignment


class ClassevivaAdapter:
    def list_assignments(self, days: int = 5) -> List[Assignment]:
        creds = EnvCredentialsProvider()

        with Client(creds) as client:
            since = datetime.today()
            until = since + timedelta(days=days)

            entries = client.list_agenda(since=since, until=until)
            return [
                Assignment(
                    id=entry.id,
                    teacher=entry.author,
                    notes=entry.notes,
                    starts_at=datetime.fromisoformat(entry.starts_at),
                    ends_at=datetime.fromisoformat(entry.ends_at),
                )
                for entry in entries
            ]
