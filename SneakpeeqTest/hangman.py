#!/usr/bin/env python3.2

import sys
import random
import string
import display

path = 'phrases1.csv'

def _keyboard_exit(method):
    def wrapper(*args, **kw):
        try:
            return method(*args, **kw)
        except KeyboardInterrupt:
            print()
            return
    return wrapper

def _ask(question, IsValid = lambda x: True, tryAgainMsg = 'Please try again.'):
    while True:
        sys.stdout.write(question + ' \x1b[K')
        sys.stdout.flush()
        ret = input()
        if IsValid(ret):
            break
        print('  ' + tryAgainMsg)
        sys.stdout.write('\x1b[2A')
        sys.stdout.flush()
    
    sys.stdout.write('\x1b[J')
    sys.stdout.flush()
    return ret

IsYN = lambda x: len(x) == 1 and x in 'ynYN'
IsLetter = lambda x: len(x) == 1 and x in string.ascii_lowercase

class Hangman:
    phrases = {}

    def __init__(self, path):
        inFile = open(path, 'rt')
        for line in iter(inFile):
            phrase, guesses = map(lambda x: x.strip(), line.split('|'))
            self.phrases[phrase] = int(guesses)

    @_keyboard_exit
    def Start(self):
        # config?
        print("   Welcome to Hangman!")
        print()

        self._game_loop()

    def _game_loop(self):
        while True:
            phrase = random.choice(list(self.phrases.keys()))
            guesses = self.phrases[phrase]
            state = '_' * len(phrase)
            missed = ""

            def _output_state():
                display = '"{0}", guesses left: {1}'.format(state, guesses)
                if len(missed) > 0:
                    display += " , missed: {0}".format(missed)
                print(display)
                
            while guesses > 0:
                _output_state()
                guess = _ask('Guess a letter:', IsLetter,
                             'Enter one English letter.')
                guesses -= 1
                

            print(phrase)
            if not self._askIfEnd():
                break

    def _ask_if_end(self):
        endIf = { 'y' : True, 'n' : False }
        ans = _ask('Would you like to play again? (y/n):',
                   IsYN, 'Enter (y/n).')
        return endIf[ans]


if __name__ == '__main__':
    game = Hangman(path)
    game.Start()
