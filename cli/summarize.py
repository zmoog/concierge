import click

from app.domain.commands import Summarize
from app import bootstrap


@click.command()
@click.option(
    '--day',
    type=click.DateTime(),
    required=True,
    help='The day to summarize')
def run_command(day):
    """Summarize the time tracking entries for a specific day"""
    print(f'summarizing {day}')

    cmd = Summarize(day=day)

    messagebus = bootstrap.for_cli()
    messagebus.handle(cmd)


if __name__ == '__main__':
    run_command()
