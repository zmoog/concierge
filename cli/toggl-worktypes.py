import click

from app.domain.commands import SummarizeWorkTypes
from app import bootstrap


@click.command()
@click.option(
    '--since',
    type=click.DateTime(),
    required=True,
    help='The starting day to summarize work types')
@click.option(
    '--until',
    type=click.DateTime(),
    required=True,
    help='The ending day to summarize work types')
def run_command(since, until):
    """Summarize the time tracking entries for a specific day"""

    cmd = SummarizeWorkTypes(since=since,
                             until=until,
                             project_ids=["153201265"])

    messagebus = bootstrap.for_cli()
    messagebus.handle(cmd, {})


if __name__ == '__main__':
    run_command()
