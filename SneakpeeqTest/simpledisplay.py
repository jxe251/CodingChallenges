game = None

def title():
    print("===========")
    print("  Hangman  ")
    print("===========")

def game_state():
    disp_state = ' '.join(game.state)
    print("\nSecret phrase:", disp_state)
    print("Lives left:", game.lives)
    print("Missed:", game.missed)

def ask(question, is_valid, try_again_msg):
    while True:
        ret = input(question + ' ')
        if is_valid(ret):
            break
        print(try_again_msg)
    return ret

def message(msg):
    print(msg)

def win():
    print("\nYou got the answer!\n")

def lose(phrase):
    print("\nThe answer was:\n%s\n" % phrase)

def goodbye():
    print("\nGoodbye!")
