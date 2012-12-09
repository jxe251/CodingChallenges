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
    class Vocab:
        def __init__(self):
            self.Score = 0
            self.Word = None
            self.Tree = {}
        def __len__(self): return len(self.Tree)
        def __getitem__(self, key):
            if len(key) == 0: return None
            if len(key) == 1 and key in string.ascii_letters:
                if key not in self.Tree:
                    self.Tree[key] = Ghost.Vocab()
                return self.Tree[key]
            else:
                currVocab = self
                for letter in key:
                    if letter not in string.ascii_letters: return None
                    currVocab = currVocab[letter]
                return currVocab
            return None            
        def __setitem__(self, key, value): self.Tree[key] = value
        def __contains__(self, item): return item in self.Tree
        def __iter__(self): return iter(self.Tree)
        def __str__(self):
            word = self.Word if self.Word != None else ""
            subTrees = []
            for letter in self.Tree:
                subTrees.append(letter + ":" + str(self.Tree[letter]))
            subTrees = "{%s}" % ", ".join(subTrees)
            tree = ("| %s") % subTrees if len(self.Tree) > 0 else ""
            return "(%i)%s%s" % (self.Score, word, tree)

        def ComputeScore(self):
            if self.Word == None:
                self.Score = 0
            else:
                self.Score = 1 if len(self.Word) % 2 == 0 else -1
            if len(self.Tree) == 0: return self.Score
            self.Score = self.Score + sum(list(map(lambda voc: self.Tree[voc].ComputeScore(), self.Tree)))
            return self.Score
        
    class RootVocab(Vocab):
        def AddWord(self, word):
            currVocab = self
            for letter in word:
                currVocab = currVocab[letter]
            currVocab.Word = word
            currVocab.Score = 1 if len(word) % 2 == 0 else -1
        
    path = "WORD.LST"
    vocab = RootVocab()
    narrowDownLimit = 20

    @_KeyboardExit
    def Start(self):
        self._Init()
        self._GameLoop()

    def _Init(self):
        print("Hi! Welcome to Ghost!")
        print("Stop the game at any time by pressing 'ctrl-c'")
        
        # suggestion: sorting file by word length + async load to lessen wait
        inFile = open(self.path, "rt")
        last = time.time()
        for line in iter(inFile):
            #AddVocab(line.rstrip('\n'))
            self.vocab.AddWord(line.rstrip('\n'))

            now = time.time()
            if now - last > 1:
                print("Loading...")
                last = now
        self.vocab.ComputeScore()
        print(self.vocab.Score)

    def _PossibleWords(self, spellTree):
        def RecurseFind(words, spellTree):
            if spellTree.Word != None:
                words.append(spellTree.Word)
            for nextLetter in spellTree:
                RecurseFind(words, spellTree[nextLetter])

        words = []
        RecurseFind(words, spellTree)
        return words

    def _GameLoop(self):
        print()
        print("Why don't you go first?")
        prefix, spellTree = "", self.vocab
        while True:
            #sleep(1)
            while True:
                nextLetter = input("Give me a letter: ")
                if len(nextLetter) != 1:
                    print("Please enter only one letter")
                elif nextLetter not in string.ascii_letters:
                    print("Please enter only letters")
                else:
                    prefix += nextLetter
                    break

            if nextLetter in spellTree:
                spellTree = spellTree[nextLetter]
            else:
                spellTree = Ghost.RootVocab()
            
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

            #make a decision
            print(len(self.vocab[prefix]))
            if len(self.vocab[prefix]) < 20:
                print(sorted(self.vocab[prefix]))
            
            if len(words) < self.narrowDownLimit:
                print(words)
                print(oddSuffixes)
                print(suffixScores)
                #print(evenLenSuffixes)
            else:
                print("%s words match '%s'. Narrow it down." % (len(words), prefix ))

            if (len(words) <= 1):
                print()
                print("The game has ended. Let's play again!")
                prefix, spellTree = "", self.vocab
                print("Why don't you go first?")
            

if __name__ == "__main__":
    game = Ghost()
    game.Start()
