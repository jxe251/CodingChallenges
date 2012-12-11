from sys import stdout
from terminal import __UESC__

def to(row, col):
    stdout.write('{0}[{1};{2}H'.format(__UESC__, row, col))

def home():
    to(0, 0)

def move(row=None, col=None):
    vert, horiz = '', ''
    if row != None:
        vert = '{0}[{1}{2}'.format(__UESC__,
                                   -row if row < 0 else row,
                                   'A' if row < 0 else 'B')
    if col != None:
        horiz = '{0}[{1}{2}'.format(__UESC__,
                                    col if col > 0 else -col,
                                    'C' if col > 0 else 'D')
    stdout.write(vert + horiz)

def save():
    stdout.write('{0}[s'.format(__UESC__))

def restore():
    stdout.write('{0}[u'.format(__UESC__))
