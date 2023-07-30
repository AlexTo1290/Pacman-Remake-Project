from tkinter import PhotoImage, Canvas, Button
from .Game import Game
from .Leaderboard import Leaderboard
from ..Settings import Settings

class Menu:
    """Creates the menu of the game"""
    def __init__(self, window):
        # Instance variables
        self.window = window
        # Setting menu background
        self.background = PhotoImage(file="Game\images\menu_background.png")

        # Creating the canvas
        self.canvas = Canvas(self.window, width=Settings.WINDOW_WIDTH, height=Settings.WINDOW_HEIGHT, background="#141414")
        self.canvas.create_image(800, 450, image=self.background)

        # Adding buttons to the menu
        self.start_game_image = PhotoImage(file="Game/images/new_game_button.png")
        self.load_game_image = PhotoImage(file="Game/images/load_game_button.png")
        self.leaderboard_image = PhotoImage(file="Game/images/leaderboard_button.png")
        self.exit_image = PhotoImage(file="Game/images/exit_button.png")

        self.start_game_button = Button(self.window, image=self.start_game_image,
                                        highlightthickness=0, command=self.start_game)
        self.load_game_button = Button(self.window, image=self.load_game_image,
                                       highlightthickness=0, command=self.load_game)
        self.leaderboard_button = Button(self.window, image=self.leaderboard_image,
                                         highlightthickness=0, command=self.leaderboard)
        self.exit_button = Button(self.window, image=self.exit_image,
                                          highlightthickness=0, command=self.exit_game)

        self.start_game_button.place(x=540, y=340)
        self.load_game_button.place(x=540, y=510)
        self.leaderboard_button.place(x=540, y=660)
        self.exit_button.place(x=70, y=750)

        self.canvas.pack()

    def display_menu(self):
        """Sets up the menu canvas by setting the background and placing menu buttons"""

        self.canvas.create_image(800, 450, image=self.background)

        self.start_game_button = Button(self.window, image=self.start_game_image,
                                        highlightcolor="#141414", command=self.start_game)
        self.load_game_button = Button(self.window, image=self.load_game_image,
                                       highlightcolor="#141414", command=self.load_game)
        self.leaderboard_button = Button(self.window, image=self.leaderboard_image,
                                         highlightcolor="#141414", command=self.leaderboard)
        self.exit_button = Button(self.window, image=self.exit_image,
                                  highlightthickness=0, command=self.exit_game)

        self.start_game_button.place(x=540, y=340)
        self.load_game_button.place(x=540, y=510)
        self.leaderboard_button.place(x=540, y=660)
        self.exit_button.place(x=70, y=750)

    def start_game(self):
        """Creates a new game"""
        # The new game button has been clicked. Removing all objects in the menu and then moving on to the game
        self.canvas.delete('all')  # clearing the canvas before using it

        # removing all the buttons from the window
        self.start_game_button.destroy()
        self.load_game_button.destroy()
        self.leaderboard_button.destroy()
        self.exit_button.destroy()

        # starting the game
        game = Game(self.window, self, self.canvas, True)

    def load_game(self):
        """Loads saved game data into a game. If none exists, creates a new game"""
        # The load game button has been clicked. Removing all objects in the menu and then moving on to the game
        self.canvas.delete('all')  # clearing the canvas before using it

        # removing all the buttons from the window
        self.start_game_button.destroy()
        self.load_game_button.destroy()
        self.leaderboard_button.destroy()
        self.exit_button.destroy()

        # starting the game
        game = Game(self.window, self, self.canvas, False)

    def leaderboard(self):
        """Takes the user to the leaderboard screen"""
        # The load game button has been clicked. Removing all objects in the menu and then moving on to the game
        self.canvas.delete('all')  # clearing the canvas before using it

        # removing all the buttons from the window
        self.start_game_button.destroy()
        self.load_game_button.destroy()
        self.leaderboard_button.destroy()
        self.exit_button.destroy()

        # switching to the leaderboard screen
        leaderboard = Leaderboard(self.window, self, self.canvas)
    
    def display_leaderboard_after_game_end(self, canvas, score, level):
        leaderboard = Leaderboard(self.window, self, canvas, score, level)
        

    def exit_game(self):
        """Closes the window - terminates the program"""
        self.window.destroy()