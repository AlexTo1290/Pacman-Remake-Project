from .Ghost import Ghost
from tkinter import PhotoImage


class Blinky(Ghost):

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)

        # Setting the image for this ghost
        self.left_frame1 = PhotoImage(file="Game/images/Ghost/red_left_frame1.png")
        self.left_frame2 = PhotoImage(file="Game/images/Ghost/red_left_frame2.png")

        self.right_frame1 = PhotoImage(file="Game/images/Ghost/red_right_frame1.png")
        self.right_frame2 = PhotoImage(file="Game/images/Ghost/red_right_frame2.png")

        self.up_frame1 = PhotoImage(file="Game/images/Ghost/red_up_frame1.png")
        self.up_frame2 = PhotoImage(file="Game/images/Ghost/red_up_frame2.png")

        self.down_frame1 = PhotoImage(file="Game/images/Ghost/red_down_frame1.png")
        self.down_frame2 = PhotoImage(file="Game/images/Ghost/red_down_frame2.png")

        # making Ghost face in the right direction (to begin with)
        self.canvas.itemconfig(self.ghost, image=self.right_frame1)