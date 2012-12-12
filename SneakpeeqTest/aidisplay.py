import re
from string import ascii_lowercase
from hangman import is_letter

game = None
candidates = None
unguessed = set(ascii_lowercase)

escape = lambda c: c if is_letter(c) else '\\%s' % c

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
    if candidates == None:
        candidates = set(game.phrases)
        unguessed = set(ascii_lowercase)

    regex = ['.' if c == '_' else escape(c) for c in game.state] + ['\Z']
    regex = re.compile(''.join(regex))

    candidates = {phrase for phrase in candidates if regex.match(phrase)}
    
    letters = [dict(l=c, phrases=0, count=0) for c in unguessed]

    for let in letters:
        for phrase in candidates:
            count = phrase.count(let['l'])
            let['phrases'] += 1 if count > 0 else 0
            let['count'] += count

    #entropy?
    letters.sort(key=lambda let: let['count'], reverse=True)
    letters.sort(key=lambda let: let['phrases'], reverse=True)

    guess = letters[0]['l']
    unguessed -= set(guess)
    return guess

