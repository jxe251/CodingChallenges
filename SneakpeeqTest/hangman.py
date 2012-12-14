#!/usr/bin/env python3.2
"""Implement the classic Hangman game."""

from sys import argv
from random import choice
from string import ascii_letters

def keyboardexit(method):
    """Decorate a method to handle <ctrl-c> interrupts."""
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
    """Hangman game engine."""
    guess_letter_question = 'Guess a letter:'
    play_again_question = 'Would you like to play again? (y/n):'

    def __init__(self, path, aimode=False):
        """Load a list of phrase/score pairs at <path>.
        Pairs are delimited by newlines and take the form:
            <phrase>|<integer score>
        Neither '_' nor '|' are allowed in the phrase.
        Any character that's not an English letter is considered punctuation.
        Set aimode to True to let the AI play the game.
        """
        global display
        if aimode:
            import aidisplay as display
        else:
            import simpledisplay as display
        display.game = self
        self.phrases = {}
        inFile = open(path, 'rt')
        for line in iter(inFile):
            if line.count('|') != 1:
                continue
            phrase, lives = (x.strip() for x in line.split('|'))
            if not self._is_valid(phrase, lives):
                continue
            self.phrases[phrase] = int(lives)

    @keyboardexit
    def Start(self):
        """Begin gameplay."""
        display.title()
        if len(self.phrases) == 0:
            display.message('No phrases in phrase list found! Exiting...')
            return
        self._gameloop()

    def _gameloop(self):
        while True:
            self._phrase = choice(list(self.phrases))
            self._phrase_lowered = self._phrase.lower()
            self.state = ['_'] * len(self._phrase)
            self._solve_positions(lambda c: not is_letter(c))
            self.lives = self.phrases[self._phrase]
            self.missed = ""

            display.game_state()
            while True:
                guess = display.ask(Hangman.guess_letter_question,
                                    is_new_letter(self.state, self.missed),
                                    '  Enter one new English letter.').lower()

                if guess in self._phrase_lowered:
                    self._solve_positions(lambda c: guess == c)
                else:
                    self.lives -= 1
                    self.missed += guess

                display.game_state()

                if '_' not in self.state:
                    display.win()
                    break
                elif self.lives == 0:
                    display.lose(self._phrase)
                    break

            if not self._ask_end():
                break
        display.goodbye()

    def _solve_positions(self, where):
        i = 0
        for c in self._phrase_lowered:
            if where(c):
                self.state[i] = self._phrase[i]
            i += 1

    def _ask_end(self):
        ans = display.ask(Hangman.play_again_question,
                          is_yn, '  Enter (y/n)')
        return end_if[ans]

    def _is_valid(self, phrase, lives):
        if len(phrase) == 0 or len(lives) == 0:
            return false
        if '_' in phrase:
            return False
        try:
            int(lives)
        except ValueError:
            return False
        return True


if __name__ == '__main__':
    if len(argv) < 2:
        print('No phrase list provided! Exiting...')
        exit(0)
    game = Hangman(argv[1], True)
    game.Start()
