game = None

def title():
    print("===========")
    print("  Hangman  ")
    print("===========")

def game_state():
    disp_state = ' '.join(game.state)
    print("Secret phrase:", disp_state)
    print("Lives left:", game.lives)
    print("Missed:", game.missed)

def ask(question, is_valid, try_again_msg):
    while True:
        ret = input(question + ' ')
        if is_valid(ret):
            break
        print(try_again_msg)
    print()
    return ret

def message(msg):
    print(msg)

def win():
    print()
    print("You got the answer!")

def lose():
    print()
    print("The answer was:", game.phrase)

def goodbye():
    print("Goodbye!")
