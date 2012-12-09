from sys import stdout
from terminal import __UESC__

def to(row, col):
    stdout.write('{0}[{1};{2}H'.format(__UESC__, row, col))
    stdout.flush()

def home():
    Cursor.To(0, 0)

def move(row, col):
    vert, horiz = '', ''
    isUp, isFwd = row < 0, col > 0
    if row != 0:
        vert = '{0}[{1}{2}'.format(__UESC__,
                                   -row if isUp else row,
                                   'A' if isUp else 'B')
    if col != 0:
        horiz = '{0}[{1}{2}'.format(__UESC__,
                                    col if isFwd else -col,
                                    'C' if isFwd else 'D')
    stdout.write(vert + horiz)
    stdout.flush()

def save():
    stdout.write('{0}[s'.format(__UESC__))
    stdout.flush()

def restore():
    stdout.write('{0}[u'.format(__UESC__))
    stdout.flush()
