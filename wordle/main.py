import curses
import time
from drawer import drawer
from server import server
from wordleBOT import wordleBOT

def main(stdscr):

    bot = wordleBOT(draw=True)

    # Setup
    draw = drawer(stdscr)
    ser = server("words.txt")
    status = ser.length * [0]
    ser.getWord()
    guess = 0

    while guess < 6:

        #attempt = draw.takeGuess(guess)
        attempt = bot.findGuess()
        status = ser.checkWord(attempt)
        bot.updateState(attempt, status)

        draw.display_word(stdscr, guess, attempt, status)
        draw.removeLetters(attempt, status)

        if set(status) == {2}:
            break

        guess += 1

    # Print answer if failure
    if guess >= 6:
        draw.display_word(stdscr, 6, ser.secretWord, 3)
    else:
        draw.display_word(stdscr, 6, "Congratulations", 3, 5)

    stdscr.getch()

curses.wrapper(main)
