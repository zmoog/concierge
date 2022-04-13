from datetime import datetime, timedelta

import click

from app import bootstrap
from app.domain.commands.school import ListHomework


@click.command()
# @click.option("--days", default=5, help="The next number of days")
@click.option(
    "--since",
    type=click.DateTime(),
    required=True,
    help="Since",
    default=datetime.today() + timedelta(days=1),
)
@click.option(
    "--until",
    type=click.DateTime(),
    required=True,
    help="Until",
    default=datetime.today() + timedelta(days=4),
)
def run_command(since: datetime, until: datetime):
    cmd = ListHomework(since=since, until=until)

    messagebus = bootstrap.for_cli()
    messagebus.handle(cmd, {})


if __name__ == "__main__":
    run_command()
