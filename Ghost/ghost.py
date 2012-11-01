import time, string

def _KeyboardExit(method):
    def wrapper(*args, **kw):
        try:
            return method(*args, **kw)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            return
    return wrapper

class Ghost:
    path = "WORD.LST"
    vocab = {}
    narrowDownLimit = 20

    @_KeyboardExit
    def Start(self):
        self._Init()
        self._GameLoop()

    def _Init(self):
        def AddVocab(word):
            def RecurseAdd(subVocab, partialWord, word):
                if 'score' not in subVocab:
                    subVocab['score'] = 0
                if len(partialWord) == 0:
                    subVocab['word'] = word
                    subVocab['score'] = 1 if len(word) % 2 == 1 else -1
                    return
                letter = partialWord[0]
                if (letter not in subVocab):
                    subVocab[partialWord[0]] = {}
                RecurseAdd(subVocab[partialWord[0]], partialWord[1:], word)
                
            RecurseAdd(self.vocab, word, word)

        def ComputeScore(vocab):
            sumChildScores = 0
            for subKey in vocab:
                if len(subKey) != 1: continue
                sumChildScores += ComputeScore(vocab[subKey])
            vocab['score'] = vocab['score'] + sumChildScores
            return vocab['score']

        print("Hi! Welcome to Ghost!")
        print("Stop the game at any time by pressing 'ctrl-c'")
        
        # suggestion: sorting file by word length + async load to lessen wait
        inFile = open(self.path, "rt")
        last = time.time()
        for line in iter(inFile):
            AddVocab(line.rstrip('\n'))

            now = time.time()
            if now - last > 1:
                print("Loading... %s" % line)
                last = now
        ComputeScore(self.vocab)
##        print(self.vocab['score'])
##        for l in string.ascii_lowercase:
##            print(self.vocab[l]['score'])

    def _PossibleWords(self, spellTree):
        def RecurseFind(words, spellTree):
            for nextLetter in spellTree:
                if nextLetter == 'score': continue
                if nextLetter == 'word':
                    words.append(spellTree[nextLetter])
                    continue
                RecurseFind(words, spellTree[nextLetter])

        words = []
        RecurseFind(words, spellTree)
        return words

    def _GameLoop(self):
        print()
        human = True
        if human:
            print("Why don't you go first?")
        prefix, spellTree = "", self.vocab
        while True:
            #sleep(1)
            print("Is Human: ", human)
            if human:
                while True:
                    nextLetter = input("Give me a letter: ")
                    if len(nextLetter) != 1:
                        print("Please enter exactly one letter")
                    elif nextLetter not in string.ascii_letters:
                        print("Please enter only letters")
                    else:
                        break
            else:
                currVocab = self.vocab
                for letter in prefix:
                    if letter not in currVocab:
                        break;
                    currVocab = currVocab[letter]
                choices = filter(lambda key: len(key) == 1, currVocab)
                choices = list(map(lambda letter: (currVocab[letter]['score'], letter), choices))
                choices.sort(reverse=True)
                print(choices)
                if len(choices) < 1:
                    spellTree = {}
                    break
                nextLetter = choices[0][1]
                print("I choose the letter, '%s'" % nextLetter)
        
            prefix += nextLetter

            if nextLetter in spellTree:
                spellTree = spellTree[nextLetter]
            else:
                spellTree = {}
            
            words = self._PossibleWords(spellTree)
            suffix = lambda w: w[len(prefix):]
            evenLen = lambda s: len(s) % 2 == 0
            zeroLen = lambda s: len(s) == 0
            scoreEvenLen = lambda s: 1 if evenLen(s) else 0
            #scoreZeroLen = lambda s: -2 if zeroLen(s) else 0
            #scoreSuffix = lambda s: scoreEvenLen(s) + scoreZeroLen(s)

            suffixes = map(lambda w: suffix(w), words)
            suffixes = filter(lambda s: not zeroLen(s), suffixes)
            suffixes = list(suffixes)
            evenSuffixes = filter(lambda s: evenLen(s), suffixes)
            evenSuffixes = list(evenSuffixes)
            oddSuffixes = filter(lambda s: not evenLen(s), suffixes)
            oddSuffixes = list(oddSuffixes)

            suffixScores = list(map(lambda s: [1, s], evenSuffixes))
            for oddSuffix in oddSuffixes:
                for suffixScore in suffixScores:
                    if oddSuffix.startswith(suffixScore[1]):
                        suffixScore[0] -= 1
                suffixScores = list(filter(lambda s: s[0] >= 0, suffixScores))

            suffixScores.sort(reverse=True)
            print("%s suffixes" % (len(suffixScores)))
            print(suffixScores[:4])
            print(suffixScores[len(suffixScores)-4:])
            
            evenLenSuffixes = filter(lambda w: len(w[1]) % 2 == 0 and len(w[1]) > 0, suffixScores)
            evenLenSuffixes = sorted(list(evenLenSuffixes), key=lambda s: len(s))
            evenLenSuffixWords = list(filter(lambda w: len(suffix(w)) % 2 == 0 and len(suffix(w)) > 0, words))
            oddLenSuffixWords = list(filter(lambda w: len(suffix(w)) % 2 == 1, words))
            
            if len(words) < self.narrowDownLimit:
##                currVoc = self.vocab
##                for letter in prefix:
##                    if letter not in currVoc:
##                        break
##                    currVoc = currVoc[letter]
##                print(currVoc)
                print(words)
##                print(oddSuffixes)
##                print(suffixScores)
                #print(evenLenSuffixes)
            else:
                print("%s words match '%s'. Narrow it down." % (len(words), prefix ))

            if len(words) == 0:
                print()
                winner = "I" if human else "You"
                print("%s win! Let's play again!" % winner)
                human = True
                prefix, spellTree = "", self.vocab
                if human:
                    print("Why don't you go first?")
            elif len(words) == 1 and prefix == words[0]:
                print()
                winner = "I" if human else "You"
                print("%s win! Let's play again!" % winner)
                human = True
                prefix, spellTree = "", self.vocab
                if human:
                    print("Why don't you go first?")
            else:
                human = not human
            

if __name__ == "__main__":
    game = Ghost()
    game.Start()
