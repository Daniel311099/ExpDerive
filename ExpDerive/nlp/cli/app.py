import click
import os
import curses
# only for training, 

# from .models import store, train
from components import Options


def app(stdscr: curses.window) -> None:
    click.echo(
        click.style(
        'Welcome to ExpDerive, a tool to train and persist models',
        fg='green',
        )
    )
    model_types = ['fine tune', 'train']
    model_type_question = 'What type of model do you want to create?'
    model_type_options = Options(model_type_question, model_types)
    curses.wrapper(model_type_options.render)
    
    # which model to train or finetune
    # change default architecture, optional,
    # pass module and class name as string

    # where is the data
    # (archietchure defined )
    # train and persist model
    # test model

if __name__ == '__main__':
    curses.wrapper(app)