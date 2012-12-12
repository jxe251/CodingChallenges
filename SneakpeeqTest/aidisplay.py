import re
from string import ascii_lowercase
from hangman import is_letter

game = None
candidates = None
unguessed = set(ascii_lowercase)

escape = lambda c: c if is_letter(c) else '\\%s' % c
strip_lower = lambda s: [c.lower() for c in s if is_letter(c)]

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
        global unguessed
        candidates = None
        unguessed = set(ascii_lowercase)

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
        #candidates = {phrase:strip_lower(phrase) for phrase in game.phrases}
        candidates = list(game.phrases)

    #filter candidates
    #print(candidates)
    regex = ['.' if c == '_' else escape(c) for c in game.state] + ['\Z']
    #print(''.join(regex))
    regex = re.compile(''.join(regex))
    candidates = [phrase for phrase in candidates if regex.match(phrase)]
    #candidates = {p:candidates[p] for p in candidates if regex.match(p)}
    #print(candidates)
    #input()

    
    letters = [dict(l=c, phrases=0, count=0) for c in unguessed]

    for let in letters:
        for phrase in candidates:
            count = phrase.count(let['l'])
            let['phrases'] += 1 if count > 0 else 0
            let['count'] += count
    """
    method = 2
    if method == 1:
        # for every unguessed letter, count per phrase for every phrase
    elif method == 2:
        # for every phrase, 
        lethash = {let['l']:let for let in letters}
        reset_list = []
        for phrase in candidates:
            for c in candidates[phrase]:
                if c not in lethash:
                    continue
                lethash[c]['count'] += 1
                if lethash[c]['new']:
                    lethash[c]['phrases'] += 1
                    lethash[c]['new'] = False
                    reset_list.append(let)
                    #print(reset_list)
            for let in reset_list:
                #print(let['new'])
                let['new'] = True
            reset_list = []
    """

    letters.sort(key=lambda let: let['count'], reverse=True)
    letters.sort(key=lambda let: let['phrases'], reverse=True)

    guess = letters[0]['l']
    unguessed -= set(guess)
    return guess

