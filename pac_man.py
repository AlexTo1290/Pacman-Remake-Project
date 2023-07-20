# PAC-MAN GAME
# AUTHOR: PAK TO
# Date of last edit: 25/11/2022

# NOTE: WINDOW IS 1600X900. PLEASE SET ASPECT RATIO TO THIS BEFORE RUNNING

# This program has been developed for COMP16321 Introduction to Programming 1 Coursework 2. It is a Pac man game with a
# menu, a save and load feature, a leaderboard feature, and a change controls feature.

from tkinter import Tk, Canvas, Button, PhotoImage, Label, Entry
from collections import defaultdict
import random


class Settings:
    """Contains the settings of the game. Static variables can be adjusted to change the game."""
    WINDOW_WIDTH = 1600
    WINDOW_HEIGHT = 900
    GAME_SPEED = 30
    PACMAN_MOVE_LENGTH = 5
    GHOST_MOVE_LENGTH = 5
    SCORE_INCREASE_ON_COIN = 10
    SCORE_INCREASE_ON_WIN = 500


class Pacman:
    """Creates 'Pacman' which can move from junctoin to junction"""

    x = 770  # holds the x-coordinate of Pacman in the canvas
    y = 610  # holds the y-coordinate of Pacman in the canvas

    can_move_left = True  # holds a boolean to whether Pacman can move left
    can_move_right = True  # holds a boolean to whether Pacman can move right
    can_move_up = False  # holds a boolean to whether Pacman can move up
    can_move_down = False  # holds a boolean to whether Pacman can move down

    direction = "right"  # holds the direction of travel, initially being right
    next_direction = ""  # holds the next direction to be changed to when valid. Allows the user to choose a movement

    # ahead of time (e.g. press right arrow before a right junction. When the right junction is
    # approached, automatically turn right)

    def __init__(self, canvas):
        self.canvas = canvas

        # Creating the animation frames
        # left
        self.frame1_left = PhotoImage(file="images/Pacman/frame1_left.png")
        self.frame2_left = PhotoImage(file="images/Pacman/frame2_left.png")
        self.frame3_left = PhotoImage(file="images/Pacman/frame3_left.png")
        self.frame4_left = PhotoImage(file="images/Pacman/frame4_left.png")
        self.frame5_left = PhotoImage(file="images/Pacman/frame5_left.png")
        self.frame6_left = PhotoImage(file="images/Pacman/frame6_left.png")

        # right
        self.frame1_right = PhotoImage(file="images/Pacman/frame1_right.png")
        self.frame2_right = PhotoImage(file="images/Pacman/frame2_right.png")
        self.frame3_right = PhotoImage(file="images/Pacman/frame3_right.png")
        self.frame4_right = PhotoImage(file="images/Pacman/frame4_right.png")
        self.frame5_right = PhotoImage(file="images/Pacman/frame5_right.png")
        self.frame6_right = PhotoImage(file="images/Pacman/frame6_right.png")

        # up
        self.frame1_up = PhotoImage(file="images/Pacman/frame1_up.png")
        self.frame2_up = PhotoImage(file="images/Pacman/frame2_up.png")
        self.frame3_up = PhotoImage(file="images/Pacman/frame3_up.png")
        self.frame4_up = PhotoImage(file="images/Pacman/frame4_up.png")
        self.frame5_up = PhotoImage(file="images/Pacman/frame5_up.png")
        self.frame6_up = PhotoImage(file="images/Pacman/frame6_up.png")

        # down
        self.frame1_down = PhotoImage(file="images/Pacman/frame1_down.png")
        self.frame2_down = PhotoImage(file="images/Pacman/frame2_down.png")
        self.frame3_down = PhotoImage(file="images/Pacman/frame3_down.png")
        self.frame4_down = PhotoImage(file="images/Pacman/frame4_down.png")
        self.frame5_down = PhotoImage(file="images/Pacman/frame5_down.png")
        self.frame6_down = PhotoImage(file="images/Pacman/frame6_down.png")

        # Adding the Pacman object to the canvas
        self.pacman = canvas.create_image(self.x, self.y, image=self.frame1_left)
        self.current_frame = 1  # holds the value of the current frame of the pacman image

    def getx(self):
        """Returns the x coordinate of the pacman object"""
        return self.x

    def gety(self):
        """Returns the y coordinate of the pacman object"""
        return self.y

    def set_direction(self, direction):
        """Sets the instance variable 'direction' to the value of the parameter"""
        self.direction = direction

    def set_coordinates(self, new_x, new_y):
        """Updates the x and y instance variables to a new location and moves the Pacman object to this location"""
        # changing coordinate instance variables to the new coordinate
        self.x = new_x
        self.y = new_y

        # moving the image of pacman to the new position
        self.canvas.coords(self.pacman, new_x, new_y)

    def move(self):
        """Moves Pacman in the direction it is facing when valid"""
        if self.direction == "right":
            # checking whether moving right is actually valid
            if self.can_move_right:
                self.canvas.move(self.pacman, Settings.PACMAN_MOVE_LENGTH, 0)
                self.x += Settings.PACMAN_MOVE_LENGTH
                self.reset_valid_directions()
                self.can_move_left = True
                self.can_move_right = True

        elif self.direction == "left":
            # checking whether moving left is actually valid
            if self.can_move_left:
                self.canvas.move(self.pacman, -Settings.PACMAN_MOVE_LENGTH, 0)
                self.x -= Settings.PACMAN_MOVE_LENGTH
                self.reset_valid_directions()
                self.can_move_left = True
                self.can_move_right = True

        elif self.direction == "up":
            # checking whether moving up is actually valid
            if self.can_move_up:
                self.canvas.move(self.pacman, 0, -Settings.PACMAN_MOVE_LENGTH)
                self.y -= Settings.PACMAN_MOVE_LENGTH
                self.reset_valid_directions()
                self.can_move_down = True
                self.can_move_up = True

        elif self.direction == "down":
            # checking whether moving down is actually valid
            if self.can_move_down:
                self.canvas.move(self.pacman, 0, Settings.PACMAN_MOVE_LENGTH)
                self.y += Settings.PACMAN_MOVE_LENGTH
                self.reset_valid_directions()
                self.can_move_up = True
                self.can_move_down = True

    def get_direction(self):
        """Returns the instance variable 'direction'"""
        return self.direction

    def get_can_move_left(self):
        """Returns the instance variable 'can_move_left'"""
        return self.can_move_left

    def get_can_move_right(self):
        """Returns the instance variable 'can_move_right'"""
        return self.can_move_right

    def get_can_move_up(self):
        """Returns the instance variable 'can_move_up'"""
        return self.can_move_up

    def get_can_move_down(self):
        """Returns the instance variable can_move_down"""
        return self.can_move_down

    def change_to_next_direction(self):
        """Tries to change the direction to the direction held in next_direction. This allows for the player to
        'premove' as they can select their move before the junction, and it'll be automatically played when the
        junction is reached"""

        if self.next_direction == "left":
            if self.can_move_left:
                self.direction = "left"
                self.next_direction = ""
            else:
                self.next_direction = "left"

        elif self.next_direction == "right":
            if self.can_move_right:
                self.direction = "right"
                self.next_direction = ""
            else:
                self.next_direction = "right"

        elif self.next_direction == "up":
            if self.can_move_up:
                self.direction = "up"
                self.next_direction = ""
            else:
                self.next_direction = "up"

        elif self.next_direction == "down":
            if self.can_move_down:
                self.direction = "down"
                self.next_direction = ""
            else:
                self.next_direction = "down"

    def change_direction_left(self, event):
        """Changes the instance variable direction to left when left is valid. Otherwise, setting instance variable
        next_direction to left so that the next available left direction change will be taken"""
        if self.can_move_left:
            self.direction = "left"
        else:
            self.next_direction = "left"

    def change_direction_right(self, event):
        """Changes the instance variable direction to right when right is valid. Otherwise, setting instance variable
        next_direction to right so that the next available right direction change will be taken"""
        if self.can_move_right:
            self.direction = "right"
        else:
            self.next_direction = "right"

    def change_direction_up(self, event):
        """Changes the instance variable direction to up if up is valid. Otherwise, setting instance variable
        next_direction to up so that the next available up direction change will be taken"""
        if self.can_move_up:
            self.direction = "up"
        else:
            self.next_direction = "up"

    def change_direction_down(self, event):
        """Changes the instance variable direction to down if down is valid. Otherwise, setting instance variable
        next_direction to down so that the next available down direction change will be taken"""
        if self.can_move_down:
            self.direction = "down"
        else:
            self.next_direction = "down"

    def reset_valid_directions(self):
        """Switches all of the can_move_..., where ... is a direction, to False"""
        self.can_move_left = False
        self.can_move_right = False
        self.can_move_up = False
        self.can_move_down = False

    def set_can_move_left(self, can_move_left):
        """Changes the boolean value held in can_move_left to the parameter value"""
        self.can_move_left = can_move_left

    def set_can_move_right(self, can_move_right):
        """Changes the boolean value held in can_move_right to the parameter value"""
        self.can_move_right = can_move_right

    def set_can_move_up(self, can_move_up):
        """Changes the boolean value held in can_move_up to the parameter value"""
        self.can_move_up = can_move_up

    def set_can_move_down(self, can_move_down):
        """Changes the boolean value held in can_move_down to the parameter value"""
        self.can_move_down = can_move_down

    def get_bbox(self):
        """Returns the boundary coordinates of pacman"""
        return self.canvas.bbox(self.pacman)

    def next_frame(self):
        """Calculates the next animation frame of the Pacman object and changes to it."""
        self.current_frame += 1

        # Since last frame is frame 6, going back to frame one if incremented frame is greater than frame 6
        if self.current_frame > 6:
            self.current_frame = 1

        # Changing the image of Pacman to the new frame
        if self.current_frame == 1:
            # Checking the direction to determine which frame to use
            if self.direction == "left":
                # changing to left frame 1
                self.canvas.itemconfig(self.pacman, image=self.frame1_left)

            elif self.direction == "right":
                # changing to right frame 1
                self.canvas.itemconfig(self.pacman, image=self.frame1_right)

            elif self.direction == "up":
                # changing to up frame 1
                self.canvas.itemconfig(self.pacman, image=self.frame1_up)

            elif self.direction == "down":
                # changing to down frame 1
                self.canvas.itemconfig(self.pacman, image=self.frame1_down)

        elif self.current_frame == 2:
            if self.direction == "left":
                # changing to left frame 2
                self.canvas.itemconfig(self.pacman, image=self.frame2_left)

            elif self.direction == "right":
                # changing to right frame 2
                self.canvas.itemconfig(self.pacman, image=self.frame2_right)

            elif self.direction == "up":
                # changing to up frame 2
                self.canvas.itemconfig(self.pacman, image=self.frame2_up)

            elif self.direction == "down":
                # changing to down frame 2
                self.canvas.itemconfig(self.pacman, image=self.frame2_down)
        elif self.current_frame == 3:
            if self.direction == "left":
                # changing to left frame 3
                self.canvas.itemconfig(self.pacman, image=self.frame3_left)

            elif self.direction == "right":
                # changing to right frame 3
                self.canvas.itemconfig(self.pacman, image=self.frame3_right)

            elif self.direction == "up":
                # changing to up frame 3
                self.canvas.itemconfig(self.pacman, image=self.frame3_up)

            elif self.direction == "down":
                # changing to down frame 3
                self.canvas.itemconfig(self.pacman, image=self.frame3_down)

        elif self.current_frame == 4:
            if self.direction == "left":
                # changing to left frame 4
                self.canvas.itemconfig(self.pacman, image=self.frame4_left)

            elif self.direction == "right":
                # changing to right frame 4
                self.canvas.itemconfig(self.pacman, image=self.frame4_right)

            elif self.direction == "up":
                # changing to up frame 4
                self.canvas.itemconfig(self.pacman, image=self.frame4_up)

            elif self.direction == "down":
                # changing to down frame 4
                self.canvas.itemconfig(self.pacman, image=self.frame4_down)

        elif self.current_frame == 5:
            if self.direction == "left":
                # changing to left frame 5
                self.canvas.itemconfig(self.pacman, image=self.frame5_left)

            elif self.direction == "right":
                # changing to right frame 5
                self.canvas.itemconfig(self.pacman, image=self.frame5_right)

            elif self.direction == "up":
                # changing to up frame 5
                self.canvas.itemconfig(self.pacman, image=self.frame5_up)

            elif self.direction == "down":
                # changing to down frame 5
                self.canvas.itemconfig(self.pacman, image=self.frame5_down)
        elif self.current_frame == 6:
            if self.direction == "left":
                # changing to left frame 6
                self.canvas.itemconfig(self.pacman, image=self.frame6_left)

            elif self.direction == "right":
                # changing to right frame 6
                self.canvas.itemconfig(self.pacman, image=self.frame6_right)

            elif self.direction == "up":
                # changing to up frame 6
                self.canvas.itemconfig(self.pacman, image=self.frame6_up)

            elif self.direction == "down":
                # changing to down frame 6
                self.canvas.itemconfig(self.pacman, image=self.frame6_down)


class Ghost:
    # Instance variables
    can_move_left = True  # holds a boolean to whether Ghost can move left (image assigned to in constructor of
    # subclass)
    can_move_right = True  # holds a boolean to whether Ghost can move right (image assigned to in constructor of
    # subclass)
    can_move_up = False  # holds a boolean to whether Ghost can move up (image assigned to in constructor of
    # subclass)
    can_move_down = False  # holds a boolean to whether Ghost can move down (image assigned to in constructor of
    # subclass)

    direction_change_counter = 0  # a counter to holds the number of direction changes attempted (by Game). The
    # direction will only change when direction_change_counter is equal to Settings.GHOST_DIRECTION_CHANGE_RATE

    direction = "right"
    next_direction = ""

    current_frame = 1

    left_frame1 = None
    left_frame2 = None
    right_frame1 = None
    right_frame2 = None
    up_frame1 = None
    up_frame2 = None
    down_frame1 = None
    down_frame2 = None

    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y

        # adding the ghost to the canvas
        self.ghost = self.canvas.create_image(self.x, self.y)

    def move(self):
        """Moves Ghost in the direction it is facing when valid"""
        if self.direction == "right":
            # checking whether moving right is actually valid
            if self.can_move_right:
                self.canvas.move(self.ghost, Settings.GHOST_MOVE_LENGTH, 0)
                self.x += Settings.GHOST_MOVE_LENGTH
                self.reset_valid_directions()
                self.can_move_left = True
                self.can_move_right = True
            else:
                # the ghost is unable to move in current direction so must be going into a wall. Changing to a randome
                # valid direction
                self.randomise_direction()

        elif self.direction == "left":
            # checking whether moving left is actually valid
            if self.can_move_left:
                self.canvas.move(self.ghost, -Settings.GHOST_MOVE_LENGTH, 0)
                self.x -= Settings.GHOST_MOVE_LENGTH
                self.reset_valid_directions()
                self.can_move_left = True
                self.can_move_right = True
            else:
                # the ghost is unable to move in current direction so must be going into a wall. Changing to a randome
                # valid direction
                self.randomise_direction()

        elif self.direction == "up":
            # checking whether moving up is actually valid
            if self.can_move_up:
                self.canvas.move(self.ghost, 0, -Settings.GHOST_MOVE_LENGTH)
                self.y -= Settings.GHOST_MOVE_LENGTH
                self.reset_valid_directions()
                self.can_move_down = True
                self.can_move_up = True
            else:
                # the ghost is unable to move in current direction so must be going into a wall. Changing to a randome
                # valid direction
                self.randomise_direction()

        elif self.direction == "down":
            # checking whether moving down is actually valid
            if self.can_move_down:
                self.canvas.move(self.ghost, 0, Settings.GHOST_MOVE_LENGTH)
                self.y += Settings.GHOST_MOVE_LENGTH
                self.reset_valid_directions()
                self.can_move_up = True
                self.can_move_down = True
            else:
                # the ghost is unable to move in current direction so must be going into a wall. Changing to a randome
                # valid direction
                self.randomise_direction()

    def get_direction(self):
        """Returns the direction the ghost is travelling in"""
        return self.direction

    def set_direction(self, direction):
        """Sets the direction to the direction given in the parameter"""
        self.direction = direction

    def change_direction_left(self):
        """Changes the instance variable direction to left when left is valid. Otherwise, setting instance variable
        next_direction to left so that the next available left direction change will be taken"""
        if self.can_move_left:
            self.direction = "left"
        else:
            self.next_direction = "left"

    def change_direction_right(self):
        """Changes the instance variable direction to right when right is valid. Otherwise, setting instance variable
        next_direction to right so that the next available right direction change will be taken"""
        if self.can_move_right:
            self.direction = "right"
        else:
            self.next_direction = "right"

    def change_direction_up(self):
        """Changes the instance variable direction to up if up is valid. Otherwise, setting instance variable
        next_direction to up so that the next available up direction change will be taken"""
        if self.can_move_up:
            self.direction = "up"
        else:
            self.next_direction = "up"

    def change_direction_down(self):
        """Changes the instance variable direction to down if down is valid. Otherwise, setting instance variable
        next_direction to down so that the next available down direction change will be taken"""
        if self.can_move_down:
            self.direction = "down"
        else:
            self.next_direction = "down"

    def reset_valid_directions(self):
        """Switches all of the can_move_..., where ... is a direction, to False"""
        self.can_move_left = False
        self.can_move_right = False
        self.can_move_up = False
        self.can_move_down = False

    def randomise_direction(self):
        """Changes the Ghost's direction to a random valid direction"""
        self.direction_change_counter = 0  # resetting the direction change counter

        directions = []  # holds the possible directions that can be changed to

        # Evaluating which direction can be changed to
        if self.can_move_left:
            directions.append("left")
        if self.can_move_right:
            directions.append("right")
        if self.can_move_up:
            directions.append("up")
        if self.can_move_down:
            directions.append("down")

        # Changing direction to a random direction in "directions"
        if len(directions) != 0:
            self.direction = directions[random.randint(0, len(directions) - 1)]

    def get_can_move_left(self):
        """Returns the instance variable 'can_move_left'"""
        return self.can_move_left

    def get_can_move_right(self):
        """Returns the instance variable 'can_move_right'"""
        return self.can_move_right

    def get_can_move_up(self):
        """Returns the instance variable 'can_move_up'"""
        return self.can_move_up

    def get_can_move_down(self):
        """Returns the instance variable 'can_move_down'"""
        return self.can_move_down

    def set_can_move_left(self, can_move_left):
        """Changes the boolean value held in can_move_left to the parameter value"""
        self.can_move_left = can_move_left

    def set_can_move_right(self, can_move_right):
        """Changes the boolean value held in can_move_right to the parameter value"""
        self.can_move_right = can_move_right

    def set_can_move_up(self, can_move_up):
        """Changes the boolean value held in can_move_up to the parameter value"""
        self.can_move_up = can_move_up

    def set_can_move_down(self, can_move_down):
        """Changes the boolean value held in can_move_down to the parameter value"""
        self.can_move_down = can_move_down

    def get_bbox(self):
        """Returns the boundary coordinates of Ghost"""
        return self.canvas.bbox(self.ghost)

    def next_frame(self):
        """Changes the ghost to its next frame"""
        """Calculates the next animation frame of the Pacman object and changes to it."""
        self.current_frame += 1

        # To match pac man's animation, it is assumed that the ghost also has 6 frames. So when current_frame is greater
        # than frame 6, setting current_frame back to frame 1. First frame is when current_frame = 1, second frame is
        # when current_frame = 4
        if self.current_frame > 6:
            self.current_frame = 1

        # Changing the image Ghost to the new frame
        if self.current_frame == 1:
            # Checking the direction to determine which frame to use
            if self.direction == "left":
                # changing to left frame 1
                self.canvas.itemconfig(self.ghost, image=self.left_frame1)

            elif self.direction == "right":
                # changing to right frame 1
                self.canvas.itemconfig(self.ghost, image=self.right_frame1)

            elif self.direction == "up":
                # changing to up frame 1
                self.canvas.itemconfig(self.ghost, image=self.up_frame1)

            elif self.direction == "down":
                # changing to down frame 1
                self.canvas.itemconfig(self.ghost, image=self.down_frame1)

        elif self.current_frame == 4:
            if self.direction == "left":
                # changing to left frame 2
                self.canvas.itemconfig(self.ghost, image=self.left_frame2)

            elif self.direction == "right":
                # changing to right frame 2
                self.canvas.itemconfig(self.ghost, image=self.right_frame2)

            elif self.direction == "up":
                # changing to up frame 2
                self.canvas.itemconfig(self.ghost, image=self.up_frame2)

            elif self.direction == "down":
                # changing to down frame 2
                self.canvas.itemconfig(self.ghost, image=self.down_frame2)

    def getx(self):
        """Returns the x coordinate of the ghost"""
        return self.x

    def gety(self):
        """Returns the y coordinate of the ghost"""
        return self.y

    def set_coordinates(self, new_x, new_y):
        """Updates the x and y instance variables to a new location and moves the Pacman object to this location"""
        # changing coordinate instance variables to the new coordinate
        self.x = new_x
        self.y = new_y

        # moving the image of pacman to the new position
        self.canvas.coords(self.ghost, new_x, new_y)


class Pinky(Ghost):

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)

        # Setting the image for this ghost
        self.left_frame1 = PhotoImage(file="images/Ghost/pink_left_frame1.png")
        self.left_frame2 = PhotoImage(file="images/Ghost/pink_left_frame2.png")

        self.right_frame1 = PhotoImage(file="images/Ghost/pink_right_frame1.png")
        self.right_frame2 = PhotoImage(file="images/Ghost/pink_right_frame2.png")

        self.up_frame1 = PhotoImage(file="images/Ghost/pink_up_frame1.png")
        self.up_frame2 = PhotoImage(file="images/Ghost/pink_up_frame2.png")

        self.down_frame1 = PhotoImage(file="images/Ghost/pink_down_frame1.png")
        self.down_frame2 = PhotoImage(file="images/Ghost/pink_down_frame2.png")

        # making Ghost face in the right direction (to begin with)
        self.canvas.itemconfig(self.ghost, image=self.right_frame1)
        self.canvas.coords(self.ghost, self.x, self.y)


class Blinky(Ghost):

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)

        # Setting the image for this ghost
        self.left_frame1 = PhotoImage(file="images/Ghost/red_left_frame1.png")
        self.left_frame2 = PhotoImage(file="images/Ghost/red_left_frame2.png")

        self.right_frame1 = PhotoImage(file="images/Ghost/red_right_frame1.png")
        self.right_frame2 = PhotoImage(file="images/Ghost/red_right_frame2.png")

        self.up_frame1 = PhotoImage(file="images/Ghost/red_up_frame1.png")
        self.up_frame2 = PhotoImage(file="images/Ghost/red_up_frame2.png")

        self.down_frame1 = PhotoImage(file="images/Ghost/red_down_frame1.png")
        self.down_frame2 = PhotoImage(file="images/Ghost/red_down_frame2.png")

        # making Ghost face in the right direction (to begin with)
        self.canvas.itemconfig(self.ghost, image=self.right_frame1)


class Inky(Ghost):

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)

        # Setting the image for this ghost
        self.left_frame1 = PhotoImage(file="images/Ghost/blue_left_frame1.png")
        self.left_frame2 = PhotoImage(file="images/Ghost/blue_left_frame2.png")

        self.right_frame1 = PhotoImage(file="images/Ghost/blue_right_frame1.png")
        self.right_frame2 = PhotoImage(file="images/Ghost/blue_right_frame2.png")

        self.up_frame1 = PhotoImage(file="images/Ghost/blue_up_frame1.png")
        self.up_frame2 = PhotoImage(file="images/Ghost/blue_up_frame2.png")

        self.down_frame1 = PhotoImage(file="images/Ghost/blue_down_frame1.png")
        self.down_frame2 = PhotoImage(file="images/Ghost/blue_down_frame2.png")

        # making Ghost face in the right direction (to begin with)
        self.canvas.itemconfig(self.ghost, image=self.right_frame1)


class Clyde(Ghost):

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)

        # Setting the image for this ghost
        self.left_frame1 = PhotoImage(file="images/Ghost/orange_left_frame1.png")
        self.left_frame2 = PhotoImage(file="images/Ghost/orange_left_frame2.png")

        self.right_frame1 = PhotoImage(file="images/Ghost/orange_right_frame1.png")
        self.right_frame2 = PhotoImage(file="images/Ghost/orange_right_frame2.png")

        self.up_frame1 = PhotoImage(file="images/Ghost/orange_up_frame1.png")
        self.up_frame2 = PhotoImage(file="images/Ghost/orange_up_frame2.png")

        self._down_frame1 = PhotoImage(file="images/Ghost/orange_down_frame1.png")
        self.down_frame2 = PhotoImage(file="images/Ghost/orange_down_frame2.png")

        # making Ghost face in the right direction (to begin with)
        self.canvas.itemconfig(self.ghost, image=self.right_frame1)


class Junction:

    def __init__(self, canvas, junction_number, x, y):
        self.text = None
        self.canvas = canvas
        self.junction_number = junction_number
        self.x = x
        self.y = y

        # Setting the image for the junction
        self.image = PhotoImage(file="images/junction_image_invisible.png")

        # Adding the junction to the canvas at its particular location
        self.junction = canvas.create_image(x, y, image=self.image)

    def show(self):
        """Makes the junction object in the maze visible"""
        self.image = PhotoImage(file="images/junction_image.png")
        self.canvas.itemconfig(self.junction, image=self.image)

        # Writing the junction number onto the junction image
        self.text = self.canvas.create_text(self.x, self.y, text=self.junction_number, font=("Arial", 15, "bold"))

    def hide(self):
        """Makes the junction object in the maze invisible"""
        self.image = PhotoImage(file="images/junction_image_invisible.png")

        # Removing the junction number from the canvas
        self.canvas.delete(self.text)

    def getx(self):
        """Returns the x coordinate of the junction"""
        return self.x

    def gety(self):
        """Returns the y coordinate of the junction"""
        return self.y

    def get_junction_number(self):
        """Returns the junction number"""
        return self.junction_number


class Coin:

    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = int(x)
        self.y = int(y)

        # Creating the image of the coin
        self.image = PhotoImage(file="images/coin_image.png")

        # Placing the image of the coin into the (x,y) coordinates
        self.coin = self.canvas.create_image(x, y, image=self.image)

    def getx(self):
        """Returns x coordinates of the coin object"""
        return self.x

    def gety(self):
        """Returns y coordinates of the coin object"""
        return self.y

    def leave_canvas(self):
        """Removes the coin object from the canvas"""
        self.canvas.delete(self.coin)


class Main:
    """Sets up the window and initiates the program"""
    def __init__(self):
        # creating the window
        self.window = Tk()
        self.window.geometry(str(Settings.WINDOW_WIDTH) + "x" + str(Settings.WINDOW_HEIGHT))
        self.window.title("Pac-man")
        self.window.attributes("-fullscreen", True)   # uncommnet to make full screen

        # creating the menu
        menu = Menu(self.window)

        self.window.mainloop()


class Menu:
    """Creates the menu of the game"""
    def __init__(self, window):
        # Instance variables
        self.window = window
        # Setting menu background
        self.background = PhotoImage(file="images/menu_background.png")

        # Creating the canvas
        self.canvas = Canvas(self.window, width=1600, height=900, background="#141414")
        self.canvas.create_image(800, 450, image=self.background)

        # Adding buttons to the menu
        self.start_game_image = PhotoImage(file="images/new_game_button.png")
        self.load_game_image = PhotoImage(file="images/load_game_button.png")
        self.leaderboard_image = PhotoImage(file="images/leaderboard_button.png")
        self.exit_image = PhotoImage(file="images/exit_button.png")

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

    def exit_game(self):
        """Closes the window - terminates the program"""
        self.window.destroy()

class Game:
    """Creates the main pacman game"""
    def __init__(self, window, menu, canvas, is_new_game):
        # Initialising instance variables
        self.window = window
        self.menu = menu

        self.junctions = []  # holds a list of the junction objects
        self.paths_graph = defaultdict(list)  # holds a dictionary representing the graph of junctions
        # connected by paths
        self.coins = []
        self.ghosts = []
        self.score = 0
        self.level = 1
        self.lives = 3  # holds num of lives. Will decrement after every collision with a ghost
        self.is_paused = False
        self.is_leave = False
        self.game_speed = Settings.GAME_SPEED

        # creating the canvas
        self.background = PhotoImage(file="images/pac_man_background.png")
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
        self.pause_play_button_image = PhotoImage(file="images/pause_play_button_image.png")
        self.save_button_image = PhotoImage(file="images/save_game_button_image.png")
        self.options_button_image = PhotoImage(file="images/options_button_image.png")
        self.leave_button_image = PhotoImage(file="images/leave_button_image.png")

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

        self.canvas.bind_all("<Button-1>", lambda event: event.widget.focus_set())
        self.canvas.focus_set()

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
        file = open("save/game_state.txt", "w")

        file.write(str(self.score) + "\n")  # writing score to file
        file.write(str(self.level) + "\n")  # writing current level to file
        file.write(str(self.lives) + "\n")  # writing remaining lives to file

        file.close()

        # writing pacman state to file
        file = open("save/pacman.txt", "w")

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
        file = open("save/pinky.txt", "w")
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
        file = open("save/inky.txt", "w")
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
        file = open("save/blinky.txt", "w")
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
        file = open("save/clyde.txt", "w")
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
        file = open("save/coins.txt", "w")

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
            file = open("save/game_state.txt", "r")
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
            file = open("save/pacman.txt", "r")

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
            file = open("save/pinky.txt", "r")

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
            file = open("save/clyde.txt", "r")

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
            file = open("save/inky.txt", "r")

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
            file = open("save/blinky.txt", "r")

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
            file = open("save/coins.txt", "r")

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
        file = open("junction_locations.txt", "r")

        for line in file:
            current_line = line.split(",")
            junction_number = current_line[0]
            x = int(current_line[1])
            y = int(current_line[2])

            junction = Junction(self.canvas, junction_number, x, y)
            self.junctions.append(junction)
            # junction.show()    # uncomment this line to display the junctions

    def create_paths(self):
        """Creates all the paths from junction to junction appending each path to the instance variables paths_graph"""
        file = open("paths.txt", "r")

        for line in file:
            line = line[:-1]  # removing the last two chars as these are the "\n" line break char
            current_line = line.split(",")

            start = current_line[0]
            end = current_line[1]
            direction = current_line[2]

            path = [end, direction]

            self.paths_graph[start].append(path)

    def create_coins(self):
        """Adds all the coins onto the canvas"""
        file = open("coin_locations.txt", "r")

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

                    # getting directions from new path and allowing pacman to move in these new directions only
                    for j in range(len(paths)):
                        current_direction = paths[j][1]

                        # updating the direction pacman can move in
                        if current_direction == "left":
                            ghost.set_can_move_left(True)
                        elif current_direction == "right":
                            ghost.set_can_move_right(True)
                        elif current_direction == "up":
                            ghost.set_can_move_up(True)
                        elif current_direction == "down":
                            ghost.set_can_move_down(True)

                        # giving a 2/3 chance of a random direction change of the ghost
                        if random.randint(1, 3) == 1:
                            ghost.randomise_direction()

                        # checking if this junction is the entrance of the ghost spawn box (junction 74). If it is,
                        # then forcing the ghost to move up and out of the box
                        if junction.get_junction_number() == 74:
                            ghost.change_direction_up()  # changing the ghost's direction to up

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

    def update_score(self):
        """Updates the score display to the user to the value in the instance variable 'score'"""
        self.score_text.config(text=("Score: " + str(self.score)))

    def update_lives(self):
        """Updates the remaining lives the player has on the canvas"""
        self.lives_label.config(text=("Lives: " + str(self.lives)))

    def update_level(self):
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
            self.update_level()

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
        game_over_image = PhotoImage(file="images/game_over_image.png")
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
        self.game_speed = int(self.game_speed * 0.6)

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
        leaderboard = Leaderboard(self.window, self.menu, self.canvas, self.score, self.level)


class Leaderboard:
    """Displays the leaderboard screen to the user"""
    def __init__(self, window, menu, canvas, score=None, level=None):
        self.window = window
        self.menu = menu
        self.canvas = canvas

        # Labels
        self.title = Label(self.window, fg="white", bg="#141414", font=("Arial", "60", "bold underline"), text="Leaderboard")
        self.title.place(x=560, y=70, anchor="w")

        self.rank_labels = []
        self.score_labels = []  # holds all the labels of highscores
        self.name_labels = []
        self.your_score = None
        self.score_separator = canvas.create_line(100, 650, 1500, 650, width=5, fill="white")

        # checking if the score and level parameters were given and setting them as instance variables if given
        if score and level:
            self.score = score
            self.level = level

        # Creating a second window to request the user for their name if score and level were given as parameters
        if score and level:
            self.get_name_window = Tk()
            self.get_name_window.geometry("600x90")
            self.get_name_window.title("Save your score!")

            self.name_entry = Entry(self.get_name_window, bd=10, selectborderwidth=5, fg="black",
                                    font=("Arial", "20", "bold"))
            self.name_request_label = Label(self.get_name_window, font=("Arial", "20"),
                                            text="Enter name:")
            self.name_submit_button = Button(self.get_name_window, command=self.update_leaderboard,
                                             width=10, text="Submit")

            self.name_request_label.grid(column=0, row=0, padx=5, pady=5)
            self.name_entry.grid(column=1, row=0, padx=5, pady=5)
            self.name_submit_button.grid(column=2, row=0)

        # Displaying the leaderboard to the player
        self.show_leaderboard()

        # Placing buttons to return to menu and to start a new game
        self.menu_button_image = PhotoImage(file="images/menu_button_image.png")
        self.new_game_button_image = PhotoImage(file="images/new_game_button_image.png")

        self.menu_button = Button(self.window, image=self.menu_button_image, command=self.
                                  return_to_menu)
        self.new_game_button = Button(self.window, image=self.new_game_button_image, command=self.
                                      new_game)

        self.menu_button.place(x=400, y=720)
        self.new_game_button.place(x=1000, y=720)

    def return_to_menu(self):
        """Removes all on-screen objects for the leaderboard and then returns them back to the menu"""
        # Removing all objects off the window before creating a new game
        self.canvas.delete("all")
        self.menu_button.destroy()
        self.new_game_button.destroy()

        # removing labels
        for i in range(len(self.rank_labels)):
            self.rank_labels[i].destroy()

        for i in range(len(self.score_labels)):
            self.score_labels[i].destroy()

        for i in range(len(self.name_labels)):
            self.name_labels[i].destroy()

        self.title.destroy()    # removes the title from the window

        # returning user back to menu
        self.menu.display_menu()

    def new_game(self):
        """Removes all on-screen objects for the leaderboard and then starts a new game"""
        # Removing all objects off the window before creating a new game
        self.canvas.delete("all")
        self.menu_button.destroy()
        self.new_game_button.destroy()

        # removing labels
        for i in range(len(self.rank_labels)):
            self.rank_labels[i].destroy()

        for i in range(len(self.score_labels)):
            self.score_labels[i].destroy()

        for i in range(len(self.name_labels)):
            self.name_labels[i].destroy()

        self.title.destroy()    # removes the title from the window

        # starting new game
        game = Game(self.window, self.menu, self.canvas, True)

    def update_leaderboard(self):
        """Updates the leaderboard with the new score"""
        scores = []  # used to store all the highscores found in the leaderboard file

        # getting the highscores from the leaderboard.txt file
        file = open("leaderboard.txt", "r")

        for line in file:
            scores.append(line[:-1].split(","))

        # checking if the player is placed on the leaderboard
        temp_scores = []  # will store the modified version of scores
        index = 0
        is_score_added = False
        rank_of_score = "-"  # '-' indicates the player is not given a rank on the leaderboard

        # inserting player's score into the leaderboard (or not if they aren't in the top 8)
        while index < len(scores):
            if self.score > int(scores[index][0]) and not is_score_added:
                # writing player's score
                highscore = [str(self.score), self.name_entry.get()]
                temp_scores.append(highscore)
                temp_scores.append(scores[index])

                rank_of_score = str(index + 1)
                is_score_added = True
            else:
                temp_scores.append(scores[index])
            index += 1

        # removing the worst score size of leaderboard is now greater than 8
        if len(temp_scores) > 8:
            temp_scores.pop(len(temp_scores) - 1)

        # setting the scores equal to the new updates scores
        scores = temp_scores.copy()

        # writing new scores to leaderboards.txt file one by one
        file = open("leaderboard.txt", "w")

        for i in range(len(scores)):
            file.write(scores[i][0] + "," + scores[i][1] + "\n")

        file.close()

        # Removing previous view of the leaderboard
        for i in range(len(self.rank_labels)):
            label = self.rank_labels[i]
            label.destroy()

        for i in range(len(self.score_labels)):
            label = self.score_labels[i]
            label.destroy()

        for i in range(len(self.name_labels)):
            label = self.name_labels[i]
            label.destroy()

        self.rank_labels.clear()
        self.score_labels.clear()
        self.name_labels.clear()

        self.show_leaderboard()  # displaying the new updated leaderboard

        # Showing player's score and rank below the line separator
        rank_label = Label(self.window, fg="white", bg="#141414", font=("Arial", "35", "bold underline"),
                           text=rank_of_score)
        rank_label.place(x=70, y=700, anchor="w")
        self.rank_labels.append(rank_label)

        score_label = Label(self.window, fg="white", bg="#141414", font=("Arial", "35", "bold underline"),
                            text=self.score)
        score_label.place(x=700, y=700, anchor="w")
        self.score_labels.append(score_label)

        name_label = Label(self.window, fg="white", bg="#141414", font=("Arial", "35", "bold underline"),
                           text=self.name_entry.get())
        name_label.place(x=1300, y=700, anchor="w")
        self.name_labels.append(name_label)

        self.get_name_window.destroy()  # closes the get_name window

    def show_leaderboard(self):
        """Reads the scores in leaderboards.txt and displays them to the user"""
        # Removing previous view of the leaderboard
        for i in range(len(self.rank_labels)):
            label = self.rank_labels[i]
            label.destroy()

        for i in range(len(self.score_labels)):
            label = self.rank_labels[i]
            label.destroy()

        for i in range(len(self.name_labels)):
            label = self.name_labels[i]
            label.destroy()

        # Creating new leaderboard view
        rank_column = ["RANK"]
        score_column = ["SCORE"]
        name_column = ["NAME"]

        # Getting the saved leaderboard and loading the data into the above arrays
        file = open("leaderboard.txt", "r")

        rank_counter = 1
        for line in file:
            current_line = line[:-1].split(",")
            rank_column.append(rank_counter)
            score_column.append(current_line[0])
            name_column.append(current_line[1])

            rank_counter += 1
        file.close()

        # Displaying the Rank numbers on the canvas
        rank_label = Label(self.window, fg="white", bg="#141414", font=("Arial", "30", "bold underline"),
                           text=rank_column[0])
        rank_label.place(x=70, y=200, anchor="w")
        self.rank_labels.append(rank_label)

        for i in range(1, len(rank_column)):
            label = Label(self.window, fg="white", bg="#141414", font=("Arial", "30", "bold"), text=rank_column[i])
            label.place(x=70, y=(200 + (i * 50)), anchor="w")
            self.rank_labels.append(label)

        # Displaying the Score numbers on the canvas
        score_label = Label(self.window, fg="white", bg="#141414", font=("Arial", "30", "bold underline"),
                            text=score_column[0])
        score_label.place(x=700, y=200, anchor="w")
        self.score_labels.append(score_label)

        for i in range(1, len(score_column)):
            label = Label(self.window, fg="white", bg="#141414", font=("Arial", "30", "bold"), text=score_column[i])
            label.place(x=700, y=(200 + (i * 50)), anchor="w")
            self.score_labels.append(label)

        # Displaying the Names on the canvas
        name_label = Label(self.window, fg="white", bg="#141414", font=("Arial", "30", "bold underline"),
                           text=name_column[0])
        name_label.place(x=1300, y=200, anchor="w")
        self.name_labels.append(name_label)

        for i in range(1, len(name_column)):
            label = Label(self.window, fg="white", bg="#141414", font=("Arial", "30", "bold"), text=name_column[i])
            label.place(x=1300, y=(200 + (i * 50)), anchor="w")
            self.name_labels.append(label)


# GLOBAL METHODS
def convert_int_to_boolean(integer):
    """Converts a int, being 0 or 1, to a boolean value, where 0 converts to False and 1 converts to True"""
    if integer == 1:
        return True
    else:
        return False

# START OF PROGRAM
main = Main()
