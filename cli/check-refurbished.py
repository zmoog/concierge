import click

from app.domain import commands
from app import bootstrap


@click.command()
@click.option(
    '--store',
    required=True,
    help='The store ID')
@click.option(
    '--product',
    required=True,
    help='The product ID')
def run_command(store: str, product: str):
    """Check the product availability in a given store"""

    cmd = commands.CheckRefurbished(
        store=store,
        products=[product],
    )

    messagebus = bootstrap.for_cli()
    messagebus.handle(cmd)


if __name__ == '__main__':
    run_command()
