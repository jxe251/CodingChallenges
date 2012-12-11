#from sys import stdout
#from terminal import output, cursor, erase

def title():
    output.clear(13)
    output.unindented_lines("""
        =============
           Hangman
        =============""")
    stdout.flush()

def message(msg):
    output.lines(msg, 13, 1)
    stdout.flush()

def game_state(state, lives, missed):
    disp_state = ' '.join(state)
    out = """
        Secret phrase:

        %(disp_state)s
        
        Lives remaining: %(lives)i
        """
    if len(missed) > 0:
        out += "Missed: %(missed)s\n"
    output.unindented_lines(out % locals(), 6, 1)
    stdout.flush()

def ask(question, is_valid, try_again_msg, row, col):
    cursor.to(row, col)
    erase.line()
    while True:
        output.lines(question + ' ', row, col)
        erase.right()
        stdout.flush()
        ret = input()
        if is_valid(ret):
            break
        print('  ' + try_again_msg)
    
    cursor.to(row+1, 0)
    erase.line()
    stdout.flush()
    return ret

def solution(phrase):
    erase.down()
    output.unindented_lines("""
    The phrase was:
    
    %(phrase)s""" % locals(), 12, 1)
    stdout.flush()
    
def goodbye():
    print("goodbye!")
