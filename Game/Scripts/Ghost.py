import random

from Game.Settings import Settings

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
    next_direction = []

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

    def calculate_shortest_path_to_player(self):
        pass

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
            self.next_direction.append("left")

    def change_direction_right(self):
        """Changes the instance variable direction to right when right is valid. Otherwise, setting instance variable
        next_direction to right so that the next available right direction change will be taken"""
        if self.can_move_right:
            self.direction = "right"
        else:
            self.next_direction.append("right")

    def change_direction_up(self):
        """Changes the instance variable direction to up if up is valid. Otherwise, setting instance variable
        next_direction to up so that the next available up direction change will be taken"""
        if self.can_move_up:
            self.direction = "up"
        else:
            self.next_direction.append("up")

    def change_direction_down(self):
        """Changes the instance variable direction to down if down is valid. Otherwise, setting instance variable
        next_direction to down so that the next available down direction change will be taken"""
        if self.can_move_down:
            self.direction = "down"
        else:
            self.next_direction.append("down")

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