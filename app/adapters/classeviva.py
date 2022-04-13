from datetime import date, datetime
from typing import List

from classeviva.client import Client
from classeviva.credentials import EnvCredentialsProvider

from app.domain.model.school import Assignment


class ClassevivaAdapter:
    def list_assignments(self, since: date, until: date) -> List[Assignment]:
        creds = EnvCredentialsProvider()

        with Client(creds) as client:
            entries = client.list_agenda(since, until)
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
