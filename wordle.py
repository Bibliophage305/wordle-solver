class Wordle:
    def __init__(self, hard=False, recalculateFirstGuess=False):
        """
        Initialises a new Wordle game
        
        Keyword arguments:
            recalculateFirstGuess (bool): If True, recalculates the first guess
            hard (bool): If True, uses hard mode
        """
        self.words = self._readFile('words.txt')
        self.guesses = self._readFile('guesses.txt') + self.words
        self.hard = hard
        if recalculateFirstGuess:
            print('Recalculating first guess...')
            self.firstGuess = self._bestGuess()
            print(f'First guess recalculated: {self.firstGuess}')
        else:
            self.firstGuess = 'aesir'
    
    def _readFile(self, filename):
        with open(filename) as f:
            words = f.read().splitlines()
        return words

    def _fitsGuess(self, word, guess, result):
        return self._findGuess(word, guess) == result

    def _findGuess(self, word, guess):
        """
        Returns a string of 0, 1, and 2, where 0 is grey, 1 is yellow, and 2 is green, as per Wordle rules
        If the characters in word and guess match, the result is a 2
        If the character in guess is not in word, the result is a 0
        If the character in guess is in word, but not in the same position, and the character in word hasn't already been used, the result is a 1
        Examples:
          _findGuess('aesir', 'aesir') -> '22222'
          _findGuess('brass', 'carbs') -> '01112'
          _findGuess('brass', 'barbs') -> '21102'
        """
        result = [None]*len(word)
        wordRemaining = []
        # First pass through and fill in all 2s (greens), and populate wordRemaining with unused characters in word
        for i, (w, g) in enumerate(zip(word, guess)):
            if w == g:
                result[i] = '2'
            else:
                wordRemaining.append(w)
        # Second pass through and fill in all 1s (yellows) and 0s (greys)
        for i, r in enumerate(result):
            if r is None:
                if guess[i] in wordRemaining:
                    result[i] = '1'
                    wordRemaining.remove(guess[i])
                else:
                    result[i] = '0'
        return ''.join(result)

    def _maxRemaining(self, guess):
        """
        Returns the maximum number of remaining words for a given guess
        findGuess has 3^5 = 243 possible results, so find the one of these results that occurs most often with the given wordset
        """
        d = {}
        for w in self.words:
            r = self._findGuess(w, guess)
            if r not in d:
                d[r] = 0
            d[r] += 1
        return max(d.values())

    def _bestGuess(self):
        """
        Returns the best guess given the current wordset
        """
        d = {g: self._maxRemaining(g) for g in self.guesses}
        bestGuesses = [g for g in d if d[g] == min(d.values())]
        for g in bestGuesses:
            if g in self.words:
                return g
        return bestGuesses[0]
    
    def _getGuessFromUser(self, guess):
        print(f'Suggested guess: {guess}')
        while True:
            useSuggestedGuessToken = input('Use suggested guess? (Y/n) ')
            if useSuggestedGuessToken in 'yY' or useSuggestedGuessToken == '':
                useSuggestedGuess = True
                break
            elif useSuggestedGuessToken in 'nN':
                useSuggestedGuess = False
                break
            print('Invalid input, must be y or n')
        while not useSuggestedGuess:
            guess = input('Enter your guess: ')
            if guess in self.guesses:
                break
            while True:
                token = input('Guess is not in Wordle\'s list of valid guesses; continue? (y/N) ')
                if token in 'nN' or token == '':
                    cont = False
                    break
                if token in 'yY':
                    cont = True
                    break
                print('Invalid input, must be y or n')
            if cont:
                break
        return guess
    
    def _getResultFromUser(self):
        while True:
            result = input('Result: ')
            if len(result) == len(self.firstGuess) and all(c in '012' for c in result):
                break
            print('Invalid result')
            print('Result must be a string of 0, 1, and 2, where 0 is grey, 1 is yellow, and 2 is green')
        return result
    
    def play(self):
        guessCount = 0
        guess = self.firstGuess
        while self.words:
            guessCount += 1
            print('-'*80)
            print(f'Guess {guessCount}')
            if len(self.words) < 11:
                print(f'{len(self.words)} words remaining: {", ".join(self.words)}')
            else:
                print(f'{len(self.words)} words remaining')
            guess = self._getGuessFromUser(guess)
            result = self._getResultFromUser()
            if result == '2'*len(guess):
                break
            self.words = [w for w in self.words if self._fitsGuess(w, guess, result)]
            if len(self.words) == 0:
                break
            if self.hard:
                for i, (c, r) in enumerate(zip(guess, result)):
                    if r == '2':
                        self.guesses = [g for g in self.guesses if g[i] == c]
            guess = self._bestGuess()
        if not self.words:
            print('Something went wrong, all words have been eliminated')
        else:
            print('-'*80)
            print(f'You win! The word was {guess}, and you guessed it in {guessCount} guesses')

def main():
    w = Wordle()
    w.play()

if __name__ == '__main__':
    main()
