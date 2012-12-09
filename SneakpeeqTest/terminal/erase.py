from sys import stdout
from terminal import __UESC__

def right():
    stdout.write('{0}[K'.format(__UESC__))
    stdout.flush()

def left():
    stdout.write('{0}[1K'.format(__UESC__))
    stdout.flush()

def line():
    stdout.write('{0}[2K'.format(__UESC__))
    stdout.flush()

def down():
    stdout.write('{0}[J'.format(__UESC__))
    stdout.flush()

def up():
    stdout.write('{0}[1J'.format(__UESC__))
    stdout.flush()

def all():
    stdout.write('{0}[2J'.format(__UESC__))
    stdout.flush()
