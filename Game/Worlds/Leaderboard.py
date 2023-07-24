from tkinter import Tk, PhotoImage, Label, Entry, Button

import Game

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
        self.menu_button_image = PhotoImage(file="Game/images/menu_button_image.png")
        self.new_game_button_image = PhotoImage(file="Game/images/new_game_button_image.png")

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
        file = open("Game/Text-Files/leaderboard.txt", "r")

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
        file = open("Game/Text-Files/leaderboard.txt", "w")

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
        file = open("Game/Text-Files/leaderboard.txt", "r")

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
