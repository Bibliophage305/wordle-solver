from interface import Interface
import inquirer, os

def getGames():
    gamesRaw = [os.path.splitext(filename)[0] for filename in os.listdir('resources')]
    games = {}
    for f in gamesRaw:
        g = f.split('_')
        if len(g) != 2:
            raise ValueError(f'{f} is not formatted correctly as (name)_(length)')
        try:
            name, length = g[0], int(g[1])
        except ValueError as e:
            raise e
        if name not in games:
            games[name] = [length]
        else:
            games[name].append(length)

    return games

def main():

    games = getGames()

    gameNames = list(games.keys())
    gameNames.sort()
    gameNames.sort(key=lambda s: s != 'wordle')

    gamePrompt = [
        inquirer.List(
            'game',
            message='Which game to solve?',
            choices=gameNames,
            default='wordle',
        ),
    ]
    gameName = inquirer.prompt(gamePrompt)['game']

    if len(games[gameName]) > 1:
        lengthPrompt = [
            inquirer.List(
                'length',
                message='Which length?',
                choices=sorted(games[gameName]),
            ),
        ]

        length = inquirer.prompt(lengthPrompt)['length']
    
    else:
        length = games[gameName][0]

    settingsPrompt = [
        inquirer.Confirm(
            'hard',
            message='Use hard mode?',
            default=True,
        ),
        inquirer.Confirm(
            'precalculatedFirstGuess',
            message='Use precalculated first guess?',
            default=True,
        )
    ]

    settings = inquirer.prompt(settingsPrompt)
    
    interface = Interface(game=f'{gameName}_{length}', hard=settings['hard'], recalculateFirstGuess=not settings['precalculatedFirstGuess'])
    interface.play()

if __name__ == '__main__':
    main()