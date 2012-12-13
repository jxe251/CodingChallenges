import re
from collections import Counter
from string import ascii_lowercase
from hangman import is_letter

game = None
candidates = None
unguessed = set(ascii_lowercase)
guess = ''

escape = lambda c: c if is_letter(c) else '\\%s' % c
lettercnt = lambda phrase: Counter(c.lower() for c in phrase if is_letter(c))

def title():
    print("===========")
    print("  Hangman  ")
    print("===========")
    print("\nThis game is running in AI mode.")
    print("Press <Ctrl-c> to quit at any time.")
    input("Press Enter to continue.\n")

def game_state():
    disp_state = ' '.join(game.state)
    print("Secret phrase:", disp_state)
    print("Lives left:", game.lives)
    print("Missed:", game.missed)

def ask(question, is_valid, try_again_msg):
    if question == game.guess_letter_question:
        return _ai_guess()
    # still ask user abt next round
    while True:
        ret = input(question + ' ')
        if is_valid(ret):
            break
        print(try_again_msg)
    print()

    if question == game.play_again_question and ret == 'y':
        global candidates
        candidates = None

    return ret

def message(msg):
    print(msg)

def win():
    print("\nYou got the answer!\n")

def lose(phrase):
    print("\nThe answer was:\n%s\n" % phrase)

def goodbye():
    print("Goodbye!")

def _ai_guess():
    global candidates
    global unguessed
    global guess
    if candidates == None:
        candidates = {phrase:lettercnt(phrase) for phrase in game.phrases}
        unguessed = set(ascii_lowercase)
        guess = ''

    wild = '[%s]' % ''.join(unguessed)
    regex = [wild if c == '_' else escape(c) for c in game.state] + ['\Z']
    regex = re.compile(''.join(regex), re.IGNORECASE)

    candidates = {p:candidates[p] for p in candidates if regex.match(p)}
    
    letters = [dict(l=c, phrases=0, count=0) for c in unguessed]
    lethash = {let['l']:let for let in letters}

    for phrase in candidates:
        del candidates[phrase][guess]
        for c in candidates[phrase]:
            lethash[c]['count'] += candidates[phrase][c]
            lethash[c]['phrases'] += 1
    #entropy?
    letters.sort(key=lambda let: let['count'], reverse=True)
    letters.sort(key=lambda let: let['phrases'], reverse=True)

    guess = letters[0]['l']
    unguessed -= set(guess)
    return guess

