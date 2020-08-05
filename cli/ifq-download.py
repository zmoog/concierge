import click

from app.domain.commands import DownloadIFQ
from app import bootstrap


@click.command()
@click.option(
    '--day',
    type=click.DateTime(),
    required=True,
    help='The day to summarize')
def run_command(day):
    """Downloads the IFQ issue for a specific day"""
    print(f'downloading IFQ for {day}')

    cmd = DownloadIFQ(day=day)

    messagebus = bootstrap.for_cli()
    messagebus.handle(cmd)


if __name__ == '__main__':
    run_command()
