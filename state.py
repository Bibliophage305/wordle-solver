class State:
    def __init__(self, wordLength, words, guesses, hard=False, verbose=True):
        """
        Initialises a new State instance
        
        Keyword arguments:
            wordLength (int) -- the length of the word to be guessed
            words (list) -- a set of possible solutions
            guesses (list) -- a set of valid guesses
            hard (bool) -- whether to use the hard mode
            firstGuess (str) -- the first guess to use
            verbose (bool) -- whether to print out extra information
        """
        self.wordLength = wordLength
        self.words = set(words)
        self.guesses = set(guesses + words)
        self.hard = hard
        self.verbose = verbose
        self._validate()
    
    def _print(self, text):
        if self.verbose:
            print(text)

    def _validate(self):
        if len(self.words) == 0:
            raise ValueError('No words provided')
        if len(self.guesses) == 0:
            raise ValueError('No guesses provided')
        badWords = [w for w in self.words if len(w) != self.wordLength]
        if len(badWords) > 0:
            raise ValueError(f'All words in word list must be {self.wordLength} characters long\nBad words found: {badWords}')
        badGuesses = [g for g in self.guesses if len(g) != self.wordLength]
        if len(badGuesses) > 0:
            raise ValueError(f'All words in guess list must be {self.wordLength} characters long\nBad words found: {badGuesses}')

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

    def _maxRemaining(self, guess, bestSoFar):
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
            if d[r] > bestSoFar:
                return d[r]
        return max(d.values())
    
    def _bestGuesses(self):
        """
        Returns the best guesses given the current wordset
        """
        bestGuesses, bestSoFar = [], len(self.words)+1
        for g in self.guesses:
            r = self._maxRemaining(g, bestSoFar)
            if r < bestSoFar:
                bestGuesses, bestSoFar = [g], r
            elif r == bestSoFar:
                bestGuesses.append(g)

        bestGuessesFiltered = [g for g in bestGuesses if g in self.words]

        if bestGuessesFiltered:
            bestGuesses = bestGuessesFiltered

        bestGuesses.sort()

        self._print(f'Best guess{"es" if len(bestGuesses) > 1 else ""}: {", ".join(bestGuesses)}')
        self._print(f'Worst case after guess: {bestSoFar} remaining')
        return bestGuesses
    
    def _updateWords(self, guess, result):
        """
        Updates the words based on the guess and result
        """
        self.words = {w for w in self.words if self._fitsGuess(w, guess, result)}
        if len(self.words) == 0:
            raise RuntimeError('All words are now impossible')
        self._print(self.getWordsRemainingString())
    
    def _updateGuesses(self, guess, result):
        """
        Updates the guesses based on the guess and result
        """
        self.guesses = {g for g in self.guesses if self._fitsGuess(g, guess, result)}
        if len(self.guesses) == 0:
            raise RuntimeError('All guesses are now impossible')
        self._print(self.getGuessesRemainingString())

    def bestGuess(self):
        """
        Returns the best guess given the current wordset
        """
        return self._bestGuesses()[0]
    
    def update(self, guess, result):
        """
        Updates the state based on a guess and its result
        """
        if guess not in self.guesses:
            raise ValueError(f'{guess} is not a valid guess')
        if len(result) != len(guess):
            raise ValueError('Result must be the same length as the guess')
        self._updateWords(guess, result)
        if self.hard:
            self._updateGuesses(guess, result)
    
    def getWordsRemaining(self):
        """
        Returns the words remaining
        """
        return self.words

    def getWordsRemainingCount(self):
        """
        Returns the number of words remaining
        """
        return len(self.words)
    
    def getWordsRemainingString(self):
        """
        Returns a string of the words remaining
        """
        return f'{len(self.words)} word{"s" if len(self.words) > 1 else ""} remaining{(": " + ", ".join(self.words)) if len(self.words) < 11 else ""}'

    def getGuessesRemaining(self):
        """
        Returns the guesses remaining
        """
        return self.guesses

    def getGuessesRemainingCount(self):
        """
        Returns the number of guesses remaining
        """
        return len(self.guesses)
    
    def getGuessesRemainingString(self):
        """
        Returns a string of the guesses remaining
        """
        return f'{len(self.guesses)} guess{"es" if len(self.guesses) > 1 else ""} remaining{(": " + ", ".join(self.guesses)) if len(self.guesses) < 11 else ""}'

if __name__ == '__main__':
    with open('resources/mini-nerdle/words.txt') as f:
        words = set(f.read().split())
    with open('resources/mini-nerdle/guesses.txt') as f:
        guesses = set(f.read().split()) | words
    state = State(wordLength=6, words=words, guesses=guesses, hard=True, verbose=True)
    state.bestGuess()
    state.update('2*7=14', '121222')
    state.bestGuess()
