import click

from .done import done


@click.command()
@click.argument("sound", type=str, required=False, default="flute")
def cli(sound: str):
    ts = done(sound)
    click.echo(
        f"{click.style(ts,fg='black',bg='blue')}! Played {click.style(sound, bold=True, fg='green')} sound",
    )
