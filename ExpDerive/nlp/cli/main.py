import click
import curses

from app import app

@click.command()
def main():
    click.echo('Hello World!')
    curses.wrapper(app)

if __name__ == '__main__':
    main()