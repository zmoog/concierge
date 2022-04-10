import click

from app import bootstrap
from app.domain.commands.school import ListHomework


@click.command()
@click.option("--days", default=5, help="The next number of days")
def run_command(days):
    """Summarize the time tracking entries for a specific day"""
    cmd = ListHomework(days=days)

    messagebus = bootstrap.for_cli()
    messagebus.handle(cmd, {})


if __name__ == "__main__":
    run_command()
