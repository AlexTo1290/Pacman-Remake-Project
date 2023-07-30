from tkinter import PhotoImage;
from Game.Settings import Settings

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

    # variables used for ghost path-finding (to catch Pac-man)
    # previous_junction = 0  # stores the junction Pac-man was last at
    # next_junction = 0  # store the junction Pac-man is travelling to
    last_junction = "50"


    def __init__(self, canvas):
        self.canvas = canvas

        # Creating the animation frames
        # left
        self.frame1_left = PhotoImage(file="Game/images/Pacman/frame1_left.png")
        self.frame2_left = PhotoImage(file="Game/images/Pacman/frame2_left.png")
        self.frame3_left = PhotoImage(file="Game/images/Pacman/frame3_left.png")
        self.frame4_left = PhotoImage(file="Game/images/Pacman/frame4_left.png")
        self.frame5_left = PhotoImage(file="Game/images/Pacman/frame5_left.png")
        self.frame6_left = PhotoImage(file="Game/images/Pacman/frame6_left.png")

        # right
        self.frame1_right = PhotoImage(file="Game/images/Pacman/frame1_right.png")
        self.frame2_right = PhotoImage(file="Game/images/Pacman/frame2_right.png")
        self.frame3_right = PhotoImage(file="Game/images/Pacman/frame3_right.png")
        self.frame4_right = PhotoImage(file="Game/images/Pacman/frame4_right.png")
        self.frame5_right = PhotoImage(file="Game/images/Pacman/frame5_right.png")
        self.frame6_right = PhotoImage(file="Game/images/Pacman/frame6_right.png")

        # up
        self.frame1_up = PhotoImage(file="Game/images/Pacman/frame1_up.png")
        self.frame2_up = PhotoImage(file="Game/images/Pacman/frame2_up.png")
        self.frame3_up = PhotoImage(file="Game/images/Pacman/frame3_up.png")
        self.frame4_up = PhotoImage(file="Game/images/Pacman/frame4_up.png")
        self.frame5_up = PhotoImage(file="Game/images/Pacman/frame5_up.png")
        self.frame6_up = PhotoImage(file="Game/images/Pacman/frame6_up.png")

        # down
        self.frame1_down = PhotoImage(file="Game/images/Pacman/frame1_down.png")
        self.frame2_down = PhotoImage(file="Game/images/Pacman/frame2_down.png")
        self.frame3_down = PhotoImage(file="Game/images/Pacman/frame3_down.png")
        self.frame4_down = PhotoImage(file="Game/images/Pacman/frame4_down.png")
        self.frame5_down = PhotoImage(file="Game/images/Pacman/frame5_down.png")
        self.frame6_down = PhotoImage(file="Game/images/Pacman/frame6_down.png")

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
            if self.direction != "left":
                self.direction = "left"
        else:
            self.next_direction = "left"

    def change_direction_right(self, event):
        """Changes the instance variable direction to right when right is valid. Otherwise, setting instance variable
        next_direction to right so that the next available right direction change will be taken"""
        if self.can_move_right:
            if self.direction != "right":
                self.direction = "right"
        else:
            self.next_direction = "right"

    def change_direction_up(self, event):
        """Changes the instance variable direction to up if up is valid. Otherwise, setting instance variable
        next_direction to up so that the next available up direction change will be taken"""
        if self.can_move_up:
            if self.direction != "up":
                self.direction = "up"
        else:
            self.next_direction = "up"

    def change_direction_down(self, event):
        """Changes the instance variable direction to down if down is valid. Otherwise, setting instance variable
        next_direction to down so that the next available down direction change will be taken"""
        if self.can_move_down:
            if self.direction != "down":
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
    
    def set_last_junction(self, last_junction):
        self.last_junction = last_junction
    
    def get_last_junction(self):
        return self.last_junction

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