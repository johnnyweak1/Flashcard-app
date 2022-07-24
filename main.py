# IMPORTS
from tkinter import *

import pandas
from pandas import *
from random import choice

# CONSTANTS
BACKGROUND_COLOR = "#B1DDC6"
word = {}
to_learn = {}

# FUNCTIONS
def new_card():
    global word, flip_timer
    screen.after_cancel(flip_timer)
    word = choice(to_learn)
    canvas.itemconfig(current_card, image=card_front)
    canvas.itemconfig(displayed_language, text="French", fill='black')
    canvas.itemconfig(displayed_word, text=f"{word['French']}", fill='black')
    flip_timer = screen.after(4000, func=flip_card)


def flip_card():
    global word
    canvas.itemconfig(current_card, image=card_back)
    canvas.itemconfig(displayed_language, text="English", fill='white')
    canvas.itemconfig(displayed_word, text=f"{word['English']}", fill='white')


def remove_record():
    global word
    to_learn.remove(word)
    to_learn_df = pandas.DataFrame(to_learn)
    to_learn_df.to_csv("data/to_learn.csv", index=False)
    new_card()

# SCREEN SETUP
screen = Tk()
screen.title("Flashy")
screen.config(background=BACKGROUND_COLOR)
screen.config(padx=50, pady=50)
flip_timer = screen.after(4000, func=flip_card)

# CANVAS SETUP
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
current_card = canvas.create_image(0, 0, anchor='nw', image=card_front)
displayed_language = canvas.create_text(400, 150, anchor='center', text="", fill="black", font=("Ariel", 40, "italic"))
displayed_word = canvas.create_text(400, 263, anchor='center', text="", fill="black", font=("trouve", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# BUTTONS
right = PhotoImage(file="images/right.png")
wrong = PhotoImage(file="images/wrong.png")
right_button = Button(image=right, highlightthickness=0, command=remove_record)
wrong_button = Button(image=wrong, highlightthickness=0, command=new_card)
right_button.grid(column=1, row=1)
wrong_button.grid(column=0, row=1)

# IMPORT CSV DATA
try:
    data = read_csv("data/to_learn.csv")
except FileNotFoundError:
    data = read_csv("data/french_words.csv")

to_learn = data.to_dict(orient="records")

# PROGRAM START
new_card()

screen.mainloop()
