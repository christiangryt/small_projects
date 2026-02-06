import curses
import time
import string

class drawer():

    def __init__(self, stdscr):
        """
        Initialize with stdscr from main.py and clear screen
        """

        self.stdscr = stdscr
        curses.curs_set(0)
        self.stdscr.clear()

        # Amount of letters per row
        # TODO: Import this from main somehow
        self.row_width = 4
        self.padding = 2

        # Start near the top in the middle of the screen
        self.screen_height, self.screen_width = stdscr.getmaxyx()
        self.start_x = int((self.screen_width -  self.row_width * self.padding) // 2)
        self.start_y = int(self.screen_height * 0.2)

        # Color pairs
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLACK)

        # Letters used
        self.alphabet = string.ascii_uppercase

        # Values for displaying and changing alphabet
        self.start_row = 8
        self.letters_per_row = 10
        self.offset_from_default_x = 2

        # Display welcome message
        welcome_msg = "Welcome to WORDLE"
        for i, letter in enumerate(welcome_msg):
            self.display(self.stdscr, -2, i-6, letter, 3)

        # Display alphabet
        self.drawAlphabet()

    def display(self, stdscr, guess, pos, letter, status):
        """
        Draw Letter at position (0-4) and Guess (row number 0-4)

        Depending on if the letter is grey (incorrect), yellow (wrong place) or green (right place).
        (subject to change) i will use different color pairs
        """

        color = 0
        match status:
            case 3:
                color = 3
            case 2:
                color = 2
            case 1:
                color = 1

        stdscr.addstr(self.start_y + guess, self.start_x + pos * self.padding, letter, curses.color_pair(color))

        stdscr.refresh()

    def display_word(self, stdscr, y, word, status, offset=0):

        # jank to be able to use constant color
        if not isinstance(status, list):

            status = len(word) * [status]

        for i, letter in enumerate(word):

            letter_pos = i - offset

            self.display(stdscr, y, letter_pos, letter, status[i])
            time.sleep(0.3)

    def takeGuess(self, guess):
        """
        Draw guess at reasonable posistion and clear when new guess comes

        Handles deletion of characters in attempt
        """

        # Clear guess Row before new round
        #for i in range(5):
            #self.display(self.stdscr, guess, i, " ", 3)

        attempt = ""
        while True:
            c = self.stdscr.getch()
            if c == curses.KEY_BACKSPACE:
                if len(attempt) > 0:
                    attempt = attempt[:-1]
                    self.display(self.stdscr, guess, len(attempt), " ", 3)

            elif len(attempt) >= 5:
                if c == 10:
                    break

            else:
                attempt += chr(c)
                self.display(self.stdscr, guess, len(attempt) - 1, chr(c), 3)

        return attempt

    def drawAlphabet(self):
        """
        Draws alphabet in uppercase below guessing rows and slightly wider than row width
        """

        for i, letter in enumerate(self.alphabet):

            self.display(self.stdscr, self.start_row + i//self.letters_per_row, i%self.letters_per_row - self.offset_from_default_x, letter, 3)

    def removeLetters(self, attempt, status):
        """
        Removes letters that are wrong.
        Colors letters yellow or green depending.
        """

        for j, letter in enumerate(attempt):

            i = self.alphabet.index(letter.upper())

            skriv = ""
            if status[j] == 0:
                skriv = " "

            else:
                skriv = letter.upper()

            self.display(self.stdscr, self.start_row + i//self.letters_per_row, i%self.letters_per_row - self.offset_from_default_x, skriv, status[j])

        # Dette er stinky, men orker ikke skrive om hvordan jeg passer status lista
        # TODO: Fiks om jeg gidder
        for k, letter in enumerate(attempt):
            if status[k] == 0:
                self.alphabet.replace(letter, " ")


    def printLine(self, word, row, offset=0, sleep=0):
        """
        Print line with display function.
        Row is calculated from base row (start_y)
        Offset is start_x + offset
        Sleep is wait between each letter
        TODO: Skriv denne og bytt ut i main og setup
        """

        None
