import click

from app.domain.commands import SummarizeWorkTypes
from app import bootstrap


@click.command()
@click.option(
    '--day',
    type=click.DateTime(),
    required=True,
    help='The day to summarize work types')
def run_command(day):
    """Summarize the time tracking entries for a specific day"""
    print(f'summarizing work types {day}')

    cmd = SummarizeWorkTypes(since=day,
                             until=day,
                             project_ids=["153201265"])

    messagebus = bootstrap.for_cli()
    messagebus.handle(cmd, {})


if __name__ == '__main__':
    run_command()
