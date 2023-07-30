from tkinter import PhotoImage, Button, Label, Entry
from collections import defaultdict
import random
import sys

from ..Settings import Settings

from ..Scripts.Blinky import Blinky
from ..Scripts.Inky import Inky
from ..Scripts.Pinky import Pinky
from ..Scripts.Clyde import Clyde
from ..Scripts.Junction import Junction
from ..Scripts.Coin import Coin
from ..Scripts.Pacman import Pacman

from .Leaderboard import Leaderboard

class Game:
    """Creates the main pacman game"""
    def __init__(self, window, menu, canvas, is_new_game):
        # Initialising instance variables
        self.window = window
        self.menu = menu

        self.junctions = []  # holds a list of the junction objects
        self.are_junctions_visible = False;
        self.paths_graph = defaultdict(list)  # holds a dictionary representing the graph of junctions
        # connected by paths. Graph format per entry::  junction(no): [[junction(no2), direction, weight], ...]

        self.coins = []
        self.ghosts = []
        self.score = 0
        self.level = 1
        self.lives = 3  # holds num of lives. Will decrement after every collision with a ghost
        self.is_paused = False
        self.is_leave = False
        self.game_speed = Settings.GAME_SPEED

        self.pinky_path_find_prob = Settings.PINKY_PATH_FIND_PROB
        self.inky_path_find_prob = Settings.INKY_PATH_FIND_PROB
        self.blinky_path_find_prob = Settings.BLINKY_PATH_FIND_PROB
        self.clyde_path_find_prob = Settings.CLYDE_PATH_FIND_PROB

        # creating the canvas
        self.background = PhotoImage(file="Game/images/pac_man_background.png")
        self.canvas = canvas
        self.canvas.create_image(800, 450, image=self.background)

        # creating options instance variables (instantiated in show_options() method)
        self.left_key_binding = "<Left>"
        self.right_key_binding = "<Right>"
        self.up_key_binding = "<Up>"
        self.down_key_binding = "<Down>"

        self.is_options_open = False
        self.options_background = None
        self.options_header = None

        self.options_left_label = None
        self.options_right_label = None
        self.options_up_label = None
        self.options_down_label = None

        self.options_left_button = None
        self.options_right_button = None
        self.options_up_button = None
        self.options_down_button = None

        self.options_left_entry = None
        self.options_right_entry = None
        self.options_up_entry = None
        self.options_down_entry = None

        self.create_junctions()  # creates the junctions in the game
        self.create_paths()  # creates the paths connecting the junctions
        if is_new_game:
            self.create_coins()  # creates the coins for pacman to collect

        # creating the score object and adding it to the canvas
        self.score_text = Label(self.window, text=("Score: " + str(self.score)),
                                font=("Arial", 50, "bold"), fg="white", anchor="nw", bg="#141414")
        self.score_text.place(x=610, y=30)

        # creating the menu buttons (pause/play, options, save game, exit)
        self.pause_play_button_image = PhotoImage(file="Game/images/pause_play_button_image.png")
        self.save_button_image = PhotoImage(file="Game/images/save_game_button_image.png")
        self.options_button_image = PhotoImage(file="Game/images/options_button_image.png")
        self.leave_button_image = PhotoImage(file="Game/images/leave_button_image.png")

        self.pause_play_button = Button(self.window, image=self.pause_play_button_image, command=self.
                                        pause_game_by_button_click)
        self.save_button = Button(self.window, image=self.save_button_image, command=self.save_game)
        self.options_button = Button(self.window, image=self.options_button_image, command=self.show_options)
        self.leave_button = Button(self.window, image=self.leave_button_image, command=self.leave_game)

        self.pause_play_button.place(x=385, y=780)
        self.options_button.place(x=595, y=780)
        self.save_button.place(x=805, y=780)
        self.leave_button.place(x=1015, y=780)

        # creating the Pacman object
        self.pacman = Pacman(self.canvas)

        # creating the ghost objects
        self.pinky = Pinky(self.canvas, 713, 410)
        self.blinky = Blinky(self.canvas, 713, 480)
        self.clyde = Clyde(self.canvas, 883, 410)
        self.inky = Inky(self.canvas, 883, 480)

        # adding the ghosts to the ghost array
        self.ghosts.append(self.pinky)
        self.ghosts.append(self.blinky)
        self.ghosts.append(self.clyde)
        self.ghosts.append(self.inky)

        # creating rectangles at exit points of the maze (so that when pacman enters it, it will be hidden behind the
        # rectangles before being teleported to the other side of the maze)
        self.canvas.create_rectangle(323, 430, 373, 470, fill="#141414", outline="#141414")
        self.canvas.create_rectangle(1228, 430, 1268, 470, fill="#141414", outline="#141414")

        self.canvas.pack()

        # displaying the current level
        self.level_label = Label(self.window, text=("Level: " + str(self.level)), fg="white", bg="#141414",
                                 font=("Arial", 50, "bold"))
        self.level_label.place(x=10, y=5)

        # displaying lives
        self.lives_label = Label(self.window, text=("Lives: " + str(self.lives)), fg="white", bg="#141414",
                                 font=("Arial", 50, "bold"))
        self.lives_label.place(x=1260, y=5)

        self.set_controls()  # creates the key bindings for the user

        # checking if this is a new game. If not, loading saved data from storage
        if not is_new_game:
            self.load_game()

        self.window.after(50, self.game_loop)  # starts the game

    def set_controls(self):
        """Sets the key bindings for the game such as Pacman movement, menu popup button, etc."""
        self.canvas.bind('<Left>', self.pacman.change_direction_left)
        self.canvas.bind('<Right>', self.pacman.change_direction_right)
        self.canvas.bind('<Up>', self.pacman.change_direction_up)
        self.canvas.bind('<Down>', self.pacman.change_direction_down)
        self.canvas.bind('p', self.pause_game_by_button_press)
        # self.canvas.bind('r', self.calculate_path_weights)
        self.canvas.bind('j', self.toggle_junctions_visiblity)

        self.canvas.bind_all("<Button-1>", lambda event: event.widget.focus_set())
        self.canvas.focus_set()

    def calculate_path_weights(self, event):
        """Calculates the weights of paths in the file paths.txt (function to be called once). This assumes that entries in the file
        are in the form JUNCTION_FROM,JUNCTION_TO,DIRECTION.  Each entry in the file is modified to the form
        JUNCTION_FROM,JUNCTION_TO,DIRECTION,WEIGHT"""
        
        paths = open("Game/Text-Files/paths.txt", "r")
        new_paths = open("Game/Text-Files/new_paths.txt", "a")

        for line in paths:
            line = line.strip("\n")
            entry = line.split(",")
            
            x_diff = abs(self.junctions[int(entry[0])].getx() - self.junctions[int(entry[1])].getx())
            y_diff = abs(self.junctions[int(entry[0])].gety() - self.junctions[int(entry[1])].gety())
            
            total_diff = str(x_diff + y_diff)
            entry.append(total_diff)

            line = ",".join(entry)
            line += "\n"

            new_paths.write(line)

    def change_left_binding(self):
        """Changes the move left key binding to the key specified in the change left key binding text field"""

        try:
            new_key_binding = self.options_left_entry.get()
            print(new_key_binding)
            self.canvas.bind(new_key_binding, self.pacman.change_direction_left)
            self.canvas.unbind(self.left_key_binding)   # unbinding previous key binding
            self.left_key_binding = new_key_binding
        except Exception:
            # The binding in the text field was not valid
            print("binding not valid")

    def change_right_binding(self):
        """Changes the move right key binding to the key specified in the change right key binding text field"""

        try:
            new_key_binding = self.options_right_entry.get()

            self.canvas.bind(new_key_binding, self.pacman.change_direction_right)
            self.canvas.unbind(self.right_key_binding)   # unbinding previous key binding
            self.right_key_binding = new_key_binding
        except Exception:
            # The binding in the text field was not valid
            print("binding not valid")

    def change_up_binding(self):
        """Changes the move up key binding to the key specified in the change up key binding text field"""

        try:
            new_key_binding = self.options_up_entry.get()

            self.canvas.bind(new_key_binding, self.pacman.change_direction_up)
            self.canvas.unbind(self.up_key_binding)   # unbinding previous key binding
            self.up_key_binding = new_key_binding
        except Exception:
            # The binding in the text field was not valid
            print("binding not valid")

    def change_down_binding(self):
        """Changes the move down key binding to the key specified in the change down key binding text field"""

        try:
            new_key_binding = self.options_down_entry.get()

            self.canvas.bind(new_key_binding, self.pacman.change_direction_down)
            self.canvas.unbind(self.down_key_binding)   # unbinding previous key binding
            self.down_key_binding = new_key_binding
        except Exception:
            # The binding in the text field was not valid
            print("binding not valid")

    def pause_game_by_button_press(self, event):
        """Inverts the is_paused' variable"""
        self.is_paused = not self.is_paused

    def pause_game_by_button_click(self):
        """Inverts the is_paused' variable"""
        self.is_paused = not self.is_paused

    def show_options(self):
        """Displays the options the user can adjust"""
        if not self.is_options_open:
            # Creating option objects
            self.options_header = Label(self.window, font=("Arial", "30", "bold"), text="CONTROLS")

            self.options_left_label = Label(self.window, font=("Arial", "20", "bold"), text="left button binding:")
            self.options_right_label = Label(self.window, font=("Arial", "20", "bold"), text="right button binding:")
            self.options_up_label = Label(self.window, font=("Arial", "20", "bold"), text="up button binding:")
            self.options_down_label = Label(self.window, font=("Arial", "20", "bold"), text="down button binding:")

            self.options_left_button = Button(self.window, text="change left binding", command=self.change_left_binding)
            self.options_right_button = Button(self.window, text="change right binding",
                                               command=self.change_right_binding)
            self.options_up_button = Button(self.window, text="change up binding", command=self.change_up_binding)
            self.options_down_button = Button(self.window, text="change down binding", command=self.change_down_binding)

            self.options_left_entry = Entry(self.window, bd=10, selectborderwidth=5, fg="black",
                                            font=("Arial", "10", "bold"))
            self.options_right_entry = Entry(self.window, bd=10, selectborderwidth=5, fg="black",
                                             font=("Arial", "10", "bold"))
            self.options_up_entry = Entry(self.window, bd=10, selectborderwidth=5, fg="black",
                                          font=("Arial", "10", "bold"))
            self.options_down_entry = Entry(self.window, bd=10, selectborderwidth=5, fg="black",
                                            font=("Arial", "10", "bold"))

            # Showing options objects
            self.options_background = self.canvas.create_rectangle(1270, 130, 1570, 770, fill="#959494", outline="white"
                                                                   , width=3)

            self.options_header.place(x=1300, y=145)

            self.options_left_label.place(x=1275, y=220)
            self.options_right_label.place(x=1275, y=370)
            self.options_up_label.place(x=1275, y=520)
            self.options_down_label.place(x=1275, y=670)

            self.options_left_button.place(x=1440, y=280)
            self.options_right_button.place(x=1440, y=430)
            self.options_up_button.place(x=1440, y=580)
            self.options_down_button.place(x=1440, y=730)
            self.options_left_entry.place(x=1275, y=270)
            self.options_right_entry.place(x=1275, y=420)
            self.options_up_entry.place(x=1275, y=570)
            self.options_down_entry.place(x=1275, y=720)

            self.is_options_open = True

        else:
            # removing options objects
            self.canvas.delete(self.options_background)
            self.options_header.destroy()

            self.options_left_label.destroy()
            self.options_right_label.destroy()
            self.options_up_label.destroy()
            self.options_down_label.destroy()

            self.options_left_button.destroy()
            self.options_right_button.destroy()
            self.options_up_button.destroy()
            self.options_down_button.destroy()

            self.options_left_entry.destroy()
            self.options_right_entry.destroy()
            self.options_up_entry.destroy()
            self.options_down_entry.destroy()

            self.is_options_open = False

    def save_game(self):
        """Saves the current state of the game into a file"""
        # Writing the states of the game into files

        # writing the game state into save/game_state
        file = open("Game/save/game_state.txt", "w")

        file.write(str(self.score) + "\n")  # writing score to file
        file.write(str(self.level) + "\n")  # writing current level to file
        file.write(str(self.lives) + "\n")  # writing remaining lives to file

        file.close()

        # writing pacman state to file
        file = open("Game/save/pacman.txt", "w")

        file.write(str(self.pacman.getx()) + "\n")  # writing the x coordinate of pacman
        file.write(str(self.pacman.gety()) + "\n")  # writing the y coordinate of pacman
        file.write(str(self.pacman.get_direction()) + "\n")

        # writing the "can_move_..." states into the file
        can_move_direction = [self.pacman.get_can_move_left(), self.pacman.get_can_move_right(),
                              self.pacman.get_can_move_up(), self.pacman.get_can_move_down()]

        for i in range(len(can_move_direction)):
            if can_move_direction[i]:
                file.write("1\n")  # writing 1 if true
            else:
                file.write("0\n")  # writing 0 if false
        file.close()

        # writing ghost states to files

        # writing pinky to file
        file = open("Game/save/pinky.txt", "w")
        file.write(str(self.pinky.getx()) + "\n")  # writing x coordinate of pinky
        file.write(str(self.pinky.gety()) + "\n")  # writing y coordinate of pinky
        file.write(self.pinky.get_direction() + "\n")  # writing direction of pinky

        can_move_direction = [self.pinky.get_can_move_left(), self.pinky.get_can_move_right(),
                              self.pinky.get_can_move_up(), self.pinky.get_can_move_down()]

        for i in range(len(can_move_direction)):  # writing the 'can_move_...' states into the file
            if can_move_direction[i]:
                file.write("1\n")  # writing 1 if true
            else:
                file.write("0\n")  # writing 0 if false
        file.close()

        # writing inky to file
        file = open("Game/save/inky.txt", "w")
        file.write(str(self.inky.getx()) + "\n")  # writing x coordinate of inky
        file.write(str(self.inky.gety()) + "\n")  # writing y coordinate of inky
        file.write(self.inky.get_direction() + "\n")  # writing direction of inky

        can_move_direction = [self.inky.get_can_move_left(), self.inky.get_can_move_right(),
                              self.inky.get_can_move_up(), self.inky.get_can_move_down()]

        for i in range(len(can_move_direction)):  # writing the 'can_move_...' states into the file
            if can_move_direction[i]:
                file.write("1\n")  # writing 1 if true
            else:
                file.write("0\n")  # writing 0 if false
        file.close()

        # writing blinky to file
        file = open("Game/save/blinky.txt", "w")
        file.write(str(self.blinky.getx()) + "\n")  # writing x coordinate of blinky
        file.write(str(self.blinky.gety()) + "\n")  # writing y coordinate of blinky
        file.write(self.blinky.get_direction() + "\n")  # writing direction of blinky

        can_move_direction = [self.blinky.get_can_move_left(), self.blinky.get_can_move_right(),
                              self.blinky.get_can_move_up(), self.blinky.get_can_move_down()]

        for i in range(len(can_move_direction)):  # writing the 'can_move_...' states into the file
            if can_move_direction[i]:
                file.write("1\n")  # writing 1 if true
            else:
                file.write("0\n")  # writing 0 if false
        file.close()

        # writing clyde to file
        file = open("Game/save/clyde.txt", "w")
        file.write(str(self.clyde.getx()) + "\n")  # writing x coordinate of clyde
        file.write(str(self.clyde.gety()) + "\n")  # writing y coordinate of clyde
        file.write(self.clyde.get_direction() + "\n")  # writing direction of clyde

        can_move_direction = [self.clyde.get_can_move_left(), self.clyde.get_can_move_right(),
                              self.clyde.get_can_move_up(), self.clyde.get_can_move_down()]

        for i in range(len(can_move_direction)):  # writing the 'can_move_...' states into the file
            if can_move_direction[i]:
                file.write("1\n")  # writing 1 if true
            else:
                file.write("0\n")  # writing 0 if false
        file.close()

        # writing location of existing coins into file
        file = open("Game/save/coins.txt", "w")

        # looping through every coin in coins and writing their coordinates in each line of the file in format "x,y"
        for index in range(len(self.coins)):
            coin = self.coins[index]
            x = coin.getx()
            y = coin.gety()
            file.write(str(x) + "," + str(y) + "\n")

        file.close()

    def new_game(self):
        """Creates a new game setting score to 0, lives to 1, ..."""
        # Updating game state
        self.score = 0
        self.update_score()

        self.lives = 3
        self.update_score()

        self.level = 1
        self.update_level()

        # Moving all the objects (pacman and ghosts) to thier start positions
        self.reset_object_positions()

    def load_game(self):
        """Loads save data into the game"""

        # Loading game state (score, remaining lives, ...) into the game
        try:
            file = open("Game/save/game_state.txt", "r")
            score = int(file.readline()[:-1])  # (:-1 offset to remove "\n")
            level = int(file.readline()[:-1])
            lives = int(file.readline()[:-1])

            file.close()

            # updating the game's state with the state read in file
            self.score = score
            self.update_score()

            self.level = level
            self.update_lives()

            self.lives = lives
            self.update_lives()

            # Loading pacman's state from files into the game
            file = open("Game/save/pacman.txt", "r")

            x = int(file.readline()[:-1])  # reading x coord of pacman (:-1 offset to remove "\n")
            y = int(file.readline()[:-1])
            direction = file.readline()[:-1]
            can_move_left = convert_int_to_boolean(int(file.readline()[:-1]))  # since file store true as 1 and false
            # as 0, converting integer to boolean
            can_move_right = convert_int_to_boolean(int(file.readline()[:-1]))
            can_move_up = convert_int_to_boolean(int(file.readline()[:-1]))
            can_move_down = convert_int_to_boolean(int(file.readline()[:-1]))

            file.close()

            # updating the pacman object's state
            self.pacman.set_coordinates(x, y)
            self.pacman.set_direction(direction)
            self.pacman.set_can_move_left(can_move_left)
            self.pacman.set_can_move_right(can_move_right)
            self.pacman.set_can_move_up(can_move_up)
            self.pacman.set_can_move_down(can_move_down)

            # Loading ghost states into the game

            # loading pinky save data
            file = open("Game/save/pinky.txt", "r")

            x = int(file.readline()[:-1])
            y = int(file.readline()[:-1])

            direction = file.readline()[:-1]
            can_move_left = convert_int_to_boolean(int(file.readline()[:-1]))  # since file store true as 1 and false
            # as 0, converting integer to boolean
            can_move_right = convert_int_to_boolean(int(file.readline()[:-1]))
            can_move_up = convert_int_to_boolean(int(file.readline()[:-1]))
            can_move_down = convert_int_to_boolean(int(file.readline()[:-1]))

            file.close()

            # updating pinky object's state
            self.pinky.set_coordinates(x, y)
            self.pinky.set_direction(direction)
            self.pinky.set_can_move_left(can_move_left)
            self.pinky.set_can_move_right(can_move_right)
            self.pinky.set_can_move_up(can_move_up)
            self.pinky.set_can_move_down(can_move_down)

            # loading clyde save data
            file = open("Game/save/clyde.txt", "r")

            x = int(file.readline()[:-1])
            y = int(file.readline()[:-1])

            direction = file.readline()[:-1]
            can_move_left = convert_int_to_boolean(int(file.readline()[:-1]))  # since file store true as 1 and false
            # as 0, converting integer to boolean
            can_move_right = convert_int_to_boolean(int(file.readline()[:-1]))
            can_move_up = convert_int_to_boolean(int(file.readline()[:-1]))
            can_move_down = convert_int_to_boolean(int(file.readline()[:-1]))

            file.close()

            # updating clyde object's state
            self.clyde.set_coordinates(x, y)
            self.clyde.set_direction(direction)
            self.clyde.set_can_move_left(can_move_left)
            self.clyde.set_can_move_right(can_move_right)
            self.clyde.set_can_move_up(can_move_up)
            self.clyde.set_can_move_down(can_move_down)

            # loading inky save data
            file = open("Game/save/inky.txt", "r")

            x = int(file.readline()[:-1])
            y = int(file.readline()[:-1])
            direction = file.readline()[:-1]
            can_move_left = convert_int_to_boolean(int(file.readline()[:-1]))  # since file store true as 1 and false
            # as 0, converting integer to boolean
            can_move_right = convert_int_to_boolean(int(file.readline()[:-1]))
            can_move_up = convert_int_to_boolean(int(file.readline()[:-1]))
            can_move_down = convert_int_to_boolean(int(file.readline()[:-1]))

            file.close()

            # updating inky object's state
            self.inky.set_coordinates(x, y)
            self.inky.set_direction(direction)
            self.inky.set_can_move_left(can_move_left)
            self.inky.set_can_move_right(can_move_right)
            self.inky.set_can_move_up(can_move_up)
            self.inky.set_can_move_down(can_move_down)

            # loading binky save data
            file = open("Game/save/blinky.txt", "r")

            x = int(file.readline()[:-1])
            y = int(file.readline()[:-1])
            direction = file.readline()[:-1]
            can_move_left = convert_int_to_boolean(int(file.readline()[:-1]))  # since file store true as 1 and false
            # as 0, converting integer to boolean
            can_move_right = convert_int_to_boolean(int(file.readline()[:-1]))
            can_move_up = convert_int_to_boolean(int(file.readline()[:-1]))
            can_move_down = convert_int_to_boolean(int(file.readline()[:-1]))

            file.close()

            # updating binky object's state
            self.blinky.set_coordinates(x, y)
            self.blinky.set_direction(direction)
            self.blinky.set_can_move_left(can_move_left)
            self.blinky.set_can_move_right(can_move_right)
            self.blinky.set_can_move_up(can_move_up)
            self.blinky.set_can_move_down(can_move_down)

            # Loading the coins into the game
            file = open("Game/save/coins.txt", "r")

            for line in file:
                current_line = line[:-1].split(",")  # splitting the line into an array. Array x and y coords [x,y]

                x = int(current_line[0])
                y = int(current_line[1])

                # creating current coin and adding it to the canvas
                coin = Coin(self.canvas, x, y)
                self.coins.append(coin)

            file.close()

        except Exception:
            # Error was found when trying to load one of the files. Aborting load and creating new game
            self.new_game()

    def leave_game(self):
        """Takes the user back to the menu. Game will not be saved"""
        # Removing all objects from the canvas
        self.canvas.delete("all")

        # Removing Label and Button objects from the world
        self.pause_play_button.destroy()
        self.options_button.destroy()
        self.save_button.destroy()
        self.leave_button.destroy()

        self.level_label.destroy()
        self.lives_label.destroy()
        self.score_text.destroy()

        self.is_leave = True

        # Displaying the menu to the user (taking user back to menu screen)
        self.menu.display_menu()

    def create_junctions(self):
        """Creates all the junctions in the maze and places them onto the canvas"""
        file = open("Game/Text-Files/junction_locations.txt", "r")

        for line in file:
            current_line = line.split(",")
            junction_number = current_line[0]
            x = int(current_line[1])
            y = int(current_line[2])

            junction = Junction(self.canvas, junction_number, x, y)
            self.junctions.append(junction)
            

    def toggle_junctions_visiblity(self, event):
        if not self.are_junctions_visible:
            for junction in self.junctions:
                junction.show()
        else:
            for junction in self.junctions:
                junction.hide()
        
        self.are_junctions_visible = not self.are_junctions_visible

    def create_paths(self):
        """Creates all the paths from junction to junction appending each path to the instance variables paths_graph"""
        file = open("Game/Text-Files/paths.txt", "r")

        for line in file:
            line = line[:-1]  # removing the last two chars as these are the "\n" line break char
            current_line = line.split(",")

            start = current_line[0]
            end = current_line[1]
            direction = current_line[2]
            weight = current_line[3]

            path = [end, direction, weight]

            self.paths_graph[start].append(path)

    def create_coins(self):
        """Adds all the coins onto the canvas"""
        file = open("Game/Text-Files/coin_locations.txt", "r")

        for line in file:
            line = line[:-1]  # removing the last two characters of line as they are the line break character
            current_line = line.split(",")
            x = current_line[0]
            y = current_line[1]

            coin = Coin(self.canvas, x, y)
            self.coins.append(coin)

    def check_coin_collisions(self):
        """Checks if pacman is touching any of the coins and removing the coins from the canvas if he is"""

        not_touching_pacman = []  # holds an array where the coins that are not touching pacman
        # will be appended to this array
        # Looping through every coin in coins and checking if any of the coins are touching pacman
        for index in range(len(self.coins)):
            # Getting the current coin
            coin = self.coins[index]

            # Getting the coordinates of the current coin
            coinX = coin.getx()
            coinY = coin.gety()

            # Getting the coordinates of the pacman
            pacmanX = self.pacman.getx()
            pacmanY = self.pacman.gety()

            # Checking if center of pacman is within a 5 pixel radius of the center of the current coin. If yes, then
            # pacman is touching the coin
            if (coinX - 5 <= pacmanX <= coinX + 5) and (coinY - 5 <= pacmanY <= coinY + 5):
                # Player is touching the coin. Updating the score and removing the coin from the game
                self.score += Settings.SCORE_INCREASE_ON_COIN
                self.update_score()
                coin.leave_canvas()
            else:
                # Pacman is not touching the current coin
                not_touching_pacman.append(self.coins[index])

        self.coins = not_touching_pacman.copy()  # storing the adjusted coins array into the instance variable coins

    def check_out_of_maze(self):
        """Checks if pacman or the ghosts have left the maze either through the left side or the right size.
        If pacman or the ghosts attempts to leave through the right side,
        they will be teleported to the left side, and vice versa."""
        # Checking if pacman has left the maze and teleport him if he has
        x = self.pacman.getx()

        if x < 353:
            # pacman is leaving the maze on the left side. Teleporting pacman to the right side of the maze
            self.pacman.set_coordinates(1248, 450)
        elif x > 1248:
            # pacman is leaving the maze on the right side. Teleporting pacman to the left sid of the maze
            self.pacman.set_coordinates(353, 450)

        # Checking if any of the ghosts have left the maze and teleporting them if they have
        for i in range(len(self.ghosts)):
            ghost = self.ghosts[i]
            ghostX = ghost.getx()

            if ghostX < 353:
                # pacman is leaving the maze on the left side. Teleporting pacman to the right side of the maze
                ghost.set_coordinates(1248, 450)
            elif ghostX > 1248:
                # pacman is leaving the maze on the right side. Teleporting pacman to the left sid of the maze
                ghost.set_coordinates(353, 450)

    def check_pacman_junction_collisions(self):
        """Checks if pacman is at a new junction. When pacman is at a new junction, the directions pacman can travel
        in is updated"""

        for index in range(len(self.junctions)):
            # getting the current junction being evaluated
            junction = self.junctions[index]

            # getting the coordinates of the junction
            junctionX = junction.getx()
            junctionY = junction.gety()

            # getting the coordinates of pacman
            pacmanX = self.pacman.getx()
            pacmanY = self.pacman.gety()
            if ((junctionX - 2) <= pacmanX <= (junctionX + 2)) and ((junctionY - 2) <= pacmanY <= (junctionY + 2)):
                # There is a collision between the current junction and pacman. Updating Pacman directions
                paths = self.paths_graph.get(junction.get_junction_number())  # getting the new paths

                # Resetting all of pacman directions and then updating them
                self.pacman.reset_valid_directions()

                # getting directions from new path and allowing pacman to move in these new directions only
                for i in range(len(paths)):
                    current_direction = paths[i][1]

                    # updating the direction pacman can move in
                    if current_direction == "left":
                        self.pacman.set_can_move_left(True)
                    elif current_direction == "right":
                        self.pacman.set_can_move_right(True)
                    elif current_direction == "up":
                        self.pacman.set_can_move_up(True)
                    elif current_direction == "down":
                        self.pacman.set_can_move_down(True)

                # Updating the junction Pac-man is travelling to (and from)
                self.pacman.set_last_junction(junction.get_junction_number())

    def check_ghost_junction_collisions(self):
        """Checks if the ghosts are at a new junction. If so, the directions the ghosts can travel are updated
        (individually)"""

        for i in range(len(self.ghosts)):
            # getting the current ghost to be checked of their collisions
            ghost = self.ghosts[i]

            # getting the coordinates of the current ghost
            ghostX = ghost.getx()
            ghostY = ghost.gety()

            # checking if the ghost is colliding with any of the junctions
            for index in range(len(self.junctions)):
                # getting the current junction being evaluated
                junction = self.junctions[index]

                # getting the coordinates of the junction
                junctionX = junction.getx()
                junctionY = junction.gety()

                if ((junctionX - 2) <= ghostX <= (junctionX + 2)) and ((junctionY - 2) <= ghostY <= (junctionY + 2)):
                    # There is a collision between the current junction and pacman. Updating Pacman directions
                    paths = self.paths_graph.get(junction.get_junction_number())  # getting the new paths

                    # Resetting all of pacman directions and then updating them
                    ghost.reset_valid_directions()

                    # getting directions from new path and allowing the ghost to move in these new directions only
                    for j in range(len(paths)):
                        current_direction = paths[j][1]

                        # updating the direction the ghost can move in
                        if current_direction == "left":
                            ghost.set_can_move_left(True)
                        elif current_direction == "right":
                            ghost.set_can_move_right(True)
                        elif current_direction == "up":
                            ghost.set_can_move_up(True)
                        elif current_direction == "down":
                            ghost.set_can_move_down(True)

                        # checking if this junction is the entrance of the ghost spawn box (junction 74). If it is,
                        # then forcing the ghost to move up and out of the box
                        if junction.get_junction_number() == 74:
                            ghost.change_direction_up()  # changing the ghost's direction to up

                    # attempting to change the ghost's direction if possible
                    # giving a chance that the ghost will go directly to the user (if outside of spawn)
                    if (int(junction.get_junction_number()) < 68 or int(junction.get_junction_number()) > 83):
                        self.direct_path_chance(ghost, junction)

                    if ghost.get_next_direction() == []:
                        ghost.randomise_direction()  # randomising the ghost's direction
                    else:
                        # changing the direction to the next direction in the queue of direction changes
                        if ghost.next_direction[0] == "left":
                            if ghost.get_can_move_left():
                                ghost.set_direction("left")
                                ghost.next_direction.pop(0)  # removes this "next" direction from the queue

                        elif ghost.next_direction[0] == "right":
                            if ghost.get_can_move_right():
                                ghost.set_direction("right")
                                ghost.next_direction.pop(0)  # removes this "next" direction from the queue

                        elif ghost.next_direction[0] == "up":
                            if ghost.get_can_move_up():
                                ghost.set_direction("up")
                                ghost.next_direction.pop(0)  # removes this "next" direction from the queue

                        elif ghost.next_direction[0] == "down":
                            if ghost.get_can_move_down():
                                ghost.set_direction("down")
                                ghost.next_direction.pop(0)  # removes this "next" direction from the queue


    def check_pacman_ghost_collisions(self):
        """Checks whether pacman is colliding with any of the ghosts. If it is, then the method decreases the lives
        and resets the round"""
        pacman_coords = self.pacman.get_bbox()

        is_collision = False

        for i in range(len(self.ghosts)):
            ghost = self.ghosts[i]
            ghost_coords = ghost.get_bbox()

            if pacman_coords[0] < ghost_coords[2] and pacman_coords[2] > ghost_coords[0] and \
                    pacman_coords[1] < ghost_coords[3] and pacman_coords[3] > ghost_coords[1]:
                is_collision = True
                break

        if is_collision:
            self.game_end(False)    

    def direct_path_chance(self, ghost, junction):
        """Gives a chance for the ghost to travel directly to the user"""

        findPath = False
        num = random.random()

        # Stimulating pinky's chance
        if isinstance(ghost, Pinky):
            if num <= self.pinky_path_find_prob:
                findPath = True

        elif isinstance(ghost, Inky):
            if num <= self.inky_path_find_prob:
                findPath = True
        
        elif isinstance(ghost, Clyde):
            if num <= self.clyde_path_find_prob:
                findPath = True
        
        elif isinstance(ghost, Blinky):
            if num <= self.blinky_path_find_prob:
                findPath = True
        
        if findPath:
            # Giving direct path directions for the ghost to reach the user
            
            # finding the junction pacman is going towards
            end_junction = self.pacman.get_last_junction()
            possible_junctions = self.paths_graph[self.pacman.get_last_junction()]

            for current in possible_junctions:
                if current[1] == self.pacman.get_direction():
                    end_junction = current[0]
                    break

            path = self.find_shortest_path(junction, end_junction)
            directions = []

            for i in range(len(path) - 1):
                directions.append(path[i][1])
            
            # adding final direction (opposite direction of pacman)
            if self.pacman.get_direction() == "up":
                directions.append("down")
            elif self.pacman.get_direction() == "down":
                directions.append("up")
            elif self.pacman.get_direction() == "right":
                directions.append("left")
            elif self.pacman.get_direction() == "left":
                directions.append("right")
                
            ghost.set_next_direction(directions)




    def find_shortest_path(self, start_junction, end_junction):
        """Returns the shortest path from one junction to another"""
        previous_junctions = self.dijkstras_algorithm(start_junction)[0]

        path = []
        current_junction = [end_junction, None]

        while current_junction[0] != start_junction.get_junction_number():
            path.append(current_junction)
            current_junction = previous_junctions[current_junction[0]]
        
        path.append(current_junction)
        path.reverse()

        return path
    

    def dijkstras_algorithm(self, start_junction):
        """Uses Dijstra's shortest path algorithm to find the shortest path from a junction to every other junction"""
        unvisited_junctions = list(self.junctions)
        # Removing the one-directional junctions from unvisited_junctions
        for i in range(68, 84):
            unvisited_junctions.pop(68)

        shortest_path = {}  # stores the best known cost to travel to each junction
        previous_junctions = {}  # stores the previous junctions visited to reach the end junction

        # Setting the cost to each junction as infinity
        max_value = sys.maxsize  # stores "infinity"
        
        for junction in unvisited_junctions:
            shortest_path[junction.get_junction_number()] = max_value
        
        shortest_path[start_junction.get_junction_number()] = 0   # start node has travel cost of 0
        
        # Main loop
        while unvisited_junctions:
            # finding the junction with the shortest known distance from the start node
            current_min_junction = None

            for junction in unvisited_junctions:
                if current_min_junction == None:
                    current_min_junction = junction.get_junction_number()
                elif shortest_path[junction.get_junction_number()] < shortest_path[current_min_junction]:
                    current_min_junction = junction.get_junction_number()

            # visiting current_min_junction and updating its neighbors shortest path (if new path is shorter than previous path)
            neighbors = self.paths_graph[current_min_junction]

            for neighbor in neighbors:
                # (each entry of neighbor consists of the list [junction_num, direction, weight])
                tentative_value = shortest_path[current_min_junction] + int(neighbor[2])

                # checking if the new-found path to the neighboring junction is shorter than the previously known path to this juncion
                if tentative_value < shortest_path[neighbor[0]]:
                    shortest_path[neighbor[0]] = tentative_value    
                    previous_junctions[neighbor[0]] = [current_min_junction, neighbor[1]]  # ERROR ---------------
            
            # marking the current junction as "visited"
            unvisited_junctions.remove(self.junctions[int(current_min_junction)])
    
        return previous_junctions, shortest_path

    def update_score(self):
        """Updates the score display to the user to the value in the instance variable 'score'"""
        self.score_text.config(text=("Score: " + str(self.score)))

    def update_lives(self):
        """Updates the remaining lives the player has on the canvas"""
        self.lives_label.config(text=("Lives: " + str(self.lives)))

    def update_level_label(self):
        """Updates the level label on the canvas with the value held in the 'level' instance variable"""
        self.level_label.config(text=("Level: " + str(self.level)))

    def game_end(self, is_win):
        """Ends the current game. If the parameter boolean value is True, then the current round is a win. Otherwise,
        the current round is a loss"""
        # Checking if the game ended as a win or loss

        if is_win:
            # updating the score
            self.score += Settings.SCORE_INCREASE_ON_WIN
            self.update_score()

            # incrementing the level
            self.level += 1
            self.update_level_label()

            # starting new round
            self.next_round()
        else:
            # decrementing the lives
            self.lives -= 1
            self.update_lives()
            self.window.after(500)

            if self.lives == 0:
                self.game_over()
            else:
                self.reset_object_positions()

    def game_over(self):
        """Takes the user to the game over screen"""
        # Removing all objects on the canvas
        self.canvas.delete("all")

        # Removing Label and Button objects from the world
        self.pause_play_button.destroy()
        self.options_button.destroy()
        self.save_button.destroy()
        self.leave_button.destroy()

        self.level_label.destroy()
        self.lives_label.destroy()
        self.score_text.destroy()

        if self.is_options_open:
            self.canvas.delete(self.options_background)
            self.options_header.destroy()

            self.options_left_label.destroy()
            self.options_right_label.destroy()
            self.options_up_label.destroy()
            self.options_down_label.destroy()

            self.options_left_button.destroy()
            self.options_right_button.destroy()
            self.options_up_button.destroy()
            self.options_down_button.destroy()

            self.options_left_entry.destroy()
            self.options_right_entry.destroy()
            self.options_up_entry.destroy()
            self.options_down_entry.destroy()

        self.is_leave = True

        # Displaying a game over image to the user
        game_over_image = PhotoImage(file="Game/images/game_over_image.png")
        game_over = self.canvas.create_image(800, 450, image=game_over_image)

        self.window.update()

        self.window.after(5000)

        self.canvas.delete(game_over)

        self.show_leaderboard()

    def reset_object_positions(self):
        """Puts the objects (pacman and the ghosts) back at their start positions"""
        # Placing pacman and the ghost back to their start positions
        self.pacman.set_coordinates(770, 610)  # placing pacman at its start position

        self.pinky.set_coordinates(713, 410)
        self.blinky.set_coordinates(713, 480)
        self.clyde.set_coordinates(885, 410)
        self.inky.set_coordinates(885, 480)

        # resetting the possible directions pacman and the ghosts can move in
        self.pacman.reset_valid_directions()
        self.pacman.set_can_move_left(True)
        self.pacman.set_can_move_right(True)

        for i in range(len(self.ghosts)):
            ghost = self.ghosts[i]
            ghost.reset_valid_directions()

        self.pinky.set_can_move_down(True)
        self.pinky.set_can_move_right(True)
        self.clyde.set_can_move_left(True)
        self.inky.set_can_move_left(True)

    def next_round(self):
        """Method that starts the next round. This method will place all the coins back onto the canvas and put
        pacman back at its start position"""
        # Placing pacman and the ghost back to their start positions
        self.reset_object_positions()

        # removing every coin on the canvas
        for index in range(len(self.coins)):
            coin = self.coins[index]
            self.canvas.delete(coin)

        # clearing the coins array and then adding new coins to the game
        self.coins.clear()
        self.create_coins()

        # increasing game speed (to increase difficulty)
        self.game_speed = int(self.game_speed * 0.7)

        # increasing the probability of ghosts finding direct path to the user
        self.blinky_path_find_prob *= 1.25
        self.pinky_path_find_prob *= 1.25
        self.inky_path_find_prob *= 1.125
        self.clyde_path_find_prob *= 1.125

    def game_loop(self):
        """Method that starts the game. This method will repeat the same block of code (move pacman, change pacman
         frame, etc., over and over again until the game ends"""
        if not self.is_leave:
            if not self.is_paused:
                # moving pacman and changing to its next animation frame
                self.pacman.move()
                self.pacman.next_frame()
                self.pacman.change_to_next_direction()

                # moving all the ghosts and changing them to their next animation frame
                for index in range(len(self.ghosts)):
                    ghost = self.ghosts[index]
                    ghost.move()
                    ghost.next_frame()

                    # giving a 1/1000 chance the ghost decides to change directions
                    number = random.randint(1, 1000)

                    if number == 1:
                        ghost.randomise_direction()
                        ghost.next_frame()

                # collision detections
                self.check_pacman_junction_collisions()
                self.check_ghost_junction_collisions()

                self.pacman.change_to_next_direction()  # this method call has been repeated as through testing, this
                # there is too large of a delay until this method is called again (direction pre-move stopped working)

                self.check_coin_collisions()
                self.check_out_of_maze()
                self.check_pacman_ghost_collisions()

                self.pacman.change_to_next_direction()  # this method call has been repeated as through testing, this
                # there is too large of a delay until this method is called again (direction pre-move stopped working)

                if len(self.coins) == 0:
                    self.game_end(True)

            self.window.after(self.game_speed, self.game_loop)

    def show_leaderboard(self):
        """Displays the leaderboard to the user and tries"""
        self.menu.display_leaderboard_after_game_end(self.canvas, self.score, self.level)




# USEFUL METHODS

def convert_int_to_boolean(integer):
    """Converts a int, being 0 or 1, to a boolean value, where 0 converts to False and 1 converts to True"""
    if integer == 1:
        return True
    else:
        return False