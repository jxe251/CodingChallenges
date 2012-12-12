#!/usr/bin/env python3.2

from random import choice
from string import ascii_letters
import simpledisplay as display

testPath = 'phrases1.csv'

def keyboardexit(method):
    def wrapper(*args, **kw):
        try:
            return method(*args, **kw)
        except KeyboardInterrupt:
            print()
            display.goodbye()
            return
    return wrapper

end_if = { 'y' : True, 'n' : False }
is_yn = lambda c: len(c) == 1 and c in 'yn'
is_letter = lambda c: len(c) == 1 and c in ascii_letters
is_new_letter = lambda guessed, state: ( 
                    lambda c: (
                        is_letter(c) and
                        c.lower() not in guessed and
                        c.lower() not in state
                    )
                )

class Hangman():
    def __init__(self, path):
        self.phrases = {}
        inFile = open(path, 'rt')
        for line in iter(inFile):
            phrase, lives = map(lambda x: x.strip(), line.split('|'))
            self.phrases[phrase] = int(lives)

    @keyboardexit
    def Start(self):
        display.game = self
        display.title()
        self._gameloop()

    def _gameloop(self):
        while True:
            self.phrase = choice(list(self.phrases.keys()))
            self.phrase_lowered = self.phrase.lower()
            self.state = ['_'] * len(self.phrase)
            for c in filter(lambda x: not is_letter(x), self.phrase):
                self._solve(c)
            self.lives = self.phrases[self.phrase]
            self.missed = ""

            display.game_state()
            while True:
                guess = display.ask('Guess a letter:',
                                    is_new_letter(self.state, self.missed),
                                    '  Enter one new English letter.').lower()

                if guess in self.phrase_lowered:
                    self._solve(guess)
                else:
                    self.lives -= 1
                    self.missed += guess

                display.game_state()

                if '_' not in self.state:
                    display.win()
                    break
                elif self.lives == 0:
                    display.lose()
                    break

            if not self._ask_end():
                break
        display.goodbye()

    def _solve(self, guess):
        i = 0
        for c in self.phrase_lowered:
            if c == guess:
                self.state[i] = self.phrase[i]
            i += 1

    def _ask_end(self):
        ans = display.ask('Would you like to play again? (y/n):',
                          is_yn, 'Enter (y/n)')
        return end_if[ans]


if __name__ == '__main__':
    game = Hangman(testPath)
    game.Start()
