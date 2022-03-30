from state import State
import json

class Interface:
    def __init__(self, game='wordle', recalculateFirstGuess=False, hard=False, verbose=True):
        settings = self._getSettings(game)
        
        self.state = State(settings['wordLength'], settings['words'], settings['guesses'], hard, verbose)

        self.guess = None

        if 'firstGuess' not in settings:
            recalculateFirstGuess = True
        
        if not recalculateFirstGuess:
            self.guess = settings['firstGuess']
        
    def _getSettings(self, game):
        try:
            with open(f'resources/{game}.json') as f:
                settings = json.load(f)
        except FileNotFoundError:
            raise NotImplementedError(f'{game} has not been implemented yet')
        self._validateSettings(settings)
        return settings

    def _validateSettings(self, settings):
        if 'wordLength' not in settings:
            raise ValueError('Word length not found in settings')
        
        if 'words' not in settings:
            raise ValueError('Words not found in settings')
        badWords = [w for w in settings['words'] if len(w) != settings['wordLength']]
        if badWords:
            raise ValueError(f'Words {badWords} do not match word length {settings["wordLength"]}')

        if 'guesses' not in settings:
            raise ValueError('Guesses not found in settings')
        badGuesses = [g for g in settings['guesses'] if len(g) != settings['wordLength']]
        if badGuesses:
            raise ValueError(f'Guesses {badGuesses} do not match word length {settings["wordLength"]}')

        if 'firstGuess' in settings:
            if settings['firstGuess'] not in settings['guesses'] + settings['words']:
                raise ValueError('First guess not found in guesses')
    
    def _validateResult(self, result):
        if len(result) != self.state.wordLength:
            raise ValueError(f'Result {result} does not match word length {self.state.wordLength}')
        for c in result:
            if c not in '012':
                raise ValueError(f'Result {result} contains invalid character {c}')

    def _update(self, result):
        self._validateResult(result)
        self.state.update(self.guess, result)
        self.guess = self.state.bestGuess()
    
    def _getGuessFromUser(self):
        print(f'Suggested guess: {self.guess}')
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
            self.guess = input('Enter your guess: ')
            if self.guess in self.state.guesses:
                break
            print(self.state.getGuessesRemaining())
            print('Invalid guess')
    
    def _getResultFromUser(self):
        while True:
            result = input('Result: ')
            try:
                self._validateResult(result)
                break
            except ValueError as e:
                print(e)
        return result

    def play(self):
        guessCount = 1
        print(f'Guess {guessCount}')
        if self.guess is None:
            print('Recalculating first guess...')
            self.guess = self.state.bestGuess()
        while True:
            self._getGuessFromUser()
            result = self._getResultFromUser()
            if result == '2'*self.state.wordLength:
                break
            guessCount += 1
            print(f'\nGuess {guessCount}')
            self._update(result)
        print(f'\nYou win! The word was {self.guess}, and you guessed it in {guessCount} guesses')
