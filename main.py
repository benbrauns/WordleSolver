import pickle
from string import ascii_lowercase as alphabet_string
import os
import json
1


alph = []

for c in alphabet_string:
    alph.append(c)

class Box:
    def __init__(self):
        self.poss_letters = self.getAlphabet()
        self.elim_letters = []
        self.solved = False
    
    def removeLetter(self, letter):
        if letter in self.poss_letters:
            self.poss_letters.remove(letter)
            self.elim_letters.append(letter)

    def solvedLetter(self, c):
        self.poss_letters.clear()
        self.elim_letters.clear()
        self.poss_letters.append(c.lower())
        self.elim_letters = self.getAlphabet()
        self.elim_letters.remove(c.lower())
        self.solved = True

    def getAlphabet(self):
        var = []
        for c in alphabet_string:
            var.append(c)
        return var

class Game:
    #Standard wordle is 5, 6 meaning 5 letters and 6 guesses
    def __init__(self, word_Length, num_Of_Guesses):
        self.word_Length = word_Length
        self.num_Of_Guesses = num_Of_Guesses
        self.words = self.loadWords()
        self.boxes = self.createBoxes()
        self.firstGuess = "adieu"
        self.word_Score = self.getWordScores()
        self.word_Frequency = self.getFrequency()
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def getFrequency(self):
        with open("lett_frequency.json", "r") as f:
            return json.load(f)

    def getWordScores(self):
        with open("word_scores.json", "r") as f:
            return json.load(f)

    def loadWords(self):
        with open("words", "rb") as f:
            return pickle.load(f)

    def createBoxes(self):
        boxes = []
        for i in range(self.word_Length):
            boxes.append(Box())
        return boxes

    def playGame(self):
        for i in range(self.num_Of_Guesses):
            print(len(self.words))
            if i == 0:
                guess = self.firstGuess
                os.system('cls' if os.name == 'nt' else 'clear')
            else:
                guess = self.findGuess()
                print(f"Please guess the word \"{guess}\"")

            results = self.guessWord(guess)
            self.parseResults(results)
            self.cullWords()
            # self.printLetters()

    def printLetters(self):
        for i, box in enumerate(self.boxes):
            print(f"Box {i}: {box.poss_letters}")

    def cullWords(self):
        for i, box in enumerate(self.boxes):
            var = list(self.words)
            for word in var:
                letter = word[i].lower()
                logic = letter not in box.poss_letters
                if letter.lower() not in box.poss_letters:
                    # print(word[i], box.poss_letters)
                    # var = input("Press enter to continues")
                    self.words.remove(word)
                    self.word_Score.pop(word)

    def parseResults(self, results):
        lett_To_Remove = results[0]
        #The values for these last two are the id stored as the key and the letter stored as the value
        #I'm not doing anything with this currently but I may in the future
        lett_Wrong_Pos = results[1]
        lett_Corr_Pos = results[2]
        for c in lett_Corr_Pos:
            #c should be the index of the letter (which is the value in the dict)
            #so this gets the correct box then uses the solvedLetter Method to complete that one
            self.boxes[c].solvedLetter(lett_Corr_Pos[c])
            var = list(self.words)

        for c in lett_Wrong_Pos:
            var = lett_Wrong_Pos[c].lower()
            self.boxes[c].removeLetter(var)

        for c in lett_To_Remove:
            for box in self.boxes:
                if box.solved == False:
                #This makes sure we don't remove a letter that appears elsewhere from where it was detected
                #I have to use list here because .values returns a weird view object and not a list
                    count = list(lett_Corr_Pos.values()).count(c) + list(lett_Wrong_Pos.values()).count(c)
                    rcount = lett_To_Remove.count(c)
                    if count <= lett_To_Remove.count(c):
                        # print(f"Remove: {lett_To_Remove.count(c)}, wrongPos: {list(lett_Corr_Pos.values()).count(c) + list(lett_Wrong_Pos.values()).count(c)}")
                        # print(f"Box {i}: {c}")
                        box.removeLetter(c.lower())

    def findGuess(self):
        # return max(self.word_Score, key=self.word_Score.get)
        score = {}
        for word in self.words:
            total = 0
            counted = []
            for i, c in enumerate(word):
                if c not in counted and not self.boxes[i].solved:
                    counted.append(c)
                    total += self.word_Frequency[c.lower()]
            score[word] = total
        return max(score, key=score.get)

    def guessWord(self, word):
        lett_To_Remove = []
        lett_Wrong_Pos = {}
        lett_Corr_Pos = {}
        print("Please enter the result of the guess")
        print("1 - Letter not in word")
        print("2 - Letter in wrong spot")
        print("3 - Letter in correct spot")
        results = input(": ")
        for i, c in enumerate(results):
            if c == "1":
                lett_To_Remove.append(word[i])
            elif c == "2":
                lett_Wrong_Pos[i] = word[i]
            elif c == "3":
                lett_Corr_Pos[i] = word[i]
            else:
                print("Error with input. Please Restart")
        os.system('cls' if os.name == 'nt' else 'clear')
        return [lett_To_Remove, lett_Wrong_Pos, lett_Corr_Pos]


wordle = Game(5, 6)
wordle.playGame()

