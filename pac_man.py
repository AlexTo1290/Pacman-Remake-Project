# PAC-MAN GAME
# AUTHOR: PAK TO
# Date of last edit: 25/11/2022

# NOTE: WINDOW IS 1600X900. PLEASE SET ASPECT RATIO TO THIS BEFORE RUNNING

# This program has been developed for COMP16321 Introduction to Programming 1 Coursework 2. It is a recreation of the arcade game
# 'Pac-man' game with a menu, save and load feature, leaderboard feature, and change controls feature.


from tkinter import Tk

from Game.Settings import Settings
from Game.Worlds.Menu import Menu


class Main:
    """Sets up the window and initiates the program"""
    def __init__(self):
        # creating the window
        self.window = Tk()
        self.window.geometry(str(Settings.WINDOW_WIDTH) + "x" + str(Settings.WINDOW_HEIGHT))
        self.window.title("Pac-man")
        self.window.attributes("-fullscreen", True)   # uncommnent to make full screen

        # creating the menu
        menu = Menu(self.window)

        self.window.mainloop()


# START OF PROGRAM
if (__name__ == '__main__'):
    main = Main()
