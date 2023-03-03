import curses
import click

class Options():
    def __init__(self, question, classes, selected=0, attributes={}):
        self.question = question
        self.classes = classes
        self.selected = selected
        self.attributes = attributes
    
    def render(self, stdscr):
        c = 0
        while c != 10:
            stdscr.erase()
            stdscr.addstr(f'{self.question}\n', curses.A_UNDERLINE)
            for i in range(len(self.classes)):
                if i == self.selected:
                    attr = curses.A_REVERSE
                else:
                    attr = curses.A_NORMAL
                stdscr.addstr("{0}. ".format(i + 1))
                stdscr.addstr(self.classes[i] + '\n', attr)
            c = stdscr.getch()  
            if c == curses.KEY_UP and self.selected > 0:
                self.selected -= 1
            elif c == curses.KEY_DOWN and self.selected < len(self.classes) - 1:
                self.selected += 1
        curses.reset_shell_mode()
        stdscr.addstr(f"You chose {self.classes[self.selected]}\n")
        stdscr.addstr(f"You chose {self.classes[self.selected]} a\n")
        click.echo(f"You chose {self.classes[self.selected]} b")
        stdscr.getch()

    def get_selected(self):
        return self.classes[self.selected]