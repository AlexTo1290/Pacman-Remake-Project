from tkinter import PhotoImage

class Junction:

    def __init__(self, canvas, junction_number, x, y):
        self.text = None
        self.canvas = canvas
        self.junction_number = junction_number
        self.x = x
        self.y = y

        # Setting the image for the junction
        self.image = PhotoImage(file="Game/images/junction_image_invisible.png")

        # Adding the junction to the canvas at its particular location
        self.junction = canvas.create_image(x, y, image=self.image)

    def show(self):
        """Makes the junction object in the maze visible"""
        self.image = PhotoImage(file="Game/images/junction_image.png")
        self.canvas.itemconfig(self.junction, image=self.image)

        # Writing the junction number onto the junction image
        self.text = self.canvas.create_text(self.x, self.y, text=self.junction_number, font=("Arial", 15, "bold"))

    def hide(self):
        """Makes the junction object in the maze invisible"""
        self.image = PhotoImage(file="Game/images/junction_image_invisible.png")

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
