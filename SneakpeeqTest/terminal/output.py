from sys import stdout
from terminal import cursor, erase

def clear():
    erase.screen()

def clear(lines):
    for i in range(lines):
        erase.line()
        stdout.write('\n')

def lines(multiline):
    lines = multiline.split('\n')
    for line in lines:
        stdout.write(line)
        cursor.move(1, None)

def unindented_lines(multiline):
    lines = _unindent(multiline)
    for line in lines:
        stdout.write(line)
        cursor.move(1, None)
"""
def lines(multiline, row, col):
    lines = multiline.split('\n')
    for line in lines:
        cursor.to(row, col)
        stdout.write(line)
        row += 1

def unindented_lines(multiline, row, col):
    lines = _unindent(multiline)
    for line in lines:
        cursor.to(row, col)
        stdout.write(line)
        row += 1
"""
def flush():
    stdout.flush()


def _unindent(multiline):
    if multiline[0] != '\n':
        return multiline
    indented = len(multiline) - len(multiline.lstrip('\n ')) - 1
    lines = map(lambda s: s[indented:], multiline.split('\n'))
    return list(lines)[1:]
