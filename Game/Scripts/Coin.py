from tkinter import PhotoImage

class Coin:

    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = int(x)
        self.y = int(y)

        # Creating the image of the coin
        self.image = PhotoImage(file="Game/images/coin_image.png")

        # Placing the image of the coin into the (x,y) coordinates
        self.add_to_canvas()

    def getx(self):
        """Returns x coordinates of the coin object"""
        return self.x

    def gety(self):
        """Returns y coordinates of the coin object"""
        return self.y
    
    def add_to_canvas(self):
        """Placing the image of the coin into the (x,y) coordinates"""
        self.coin = self.canvas.create_image(self.x, self.y, image=self.image)

    def leave_canvas(self):
        """Removes the coin object from the canvas"""
        self.canvas.delete(self.coin)