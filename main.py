from tkinter import *
from pandas import *
from random import choice

BACKGROUND_COLOR = "#B1DDC6"
rand_word = {}
words_dic = {}

# -------------------------- GETTING WORDS ----------------------------- #
try:
    words_database = read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_database = read_csv("data/french_words.csv")
    words_dic = original_database.to_dict(orient="records")
else:
    words_dic = words_database.to_dict(orient="records")


def random_word():
    global rand_word, flip
    window.after_cancel(flip)
    rand_word = choice(words_dic)
    canvas.itemconfig(language_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=rand_word["French"], fill="black")
    canvas.itemconfig(card_bg, image=card_front)
    flip = window.after(3000, func=flip_card)


def known_card():
    words_dic.remove(rand_word)
    data = DataFrame(words_dic)
    data.to_csv("data/words_to_learn.csv", index=False)
    random_word()


# --------------------------- SWITCHING THE CARD ---------------------- #
def flip_card():
    canvas.itemconfig(language_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=rand_word["English"], fill="white")
    canvas.itemconfig(card_bg, image=card_back)


# ----------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("The other side")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)

flip = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card_bg = canvas.create_image(400, 263, image=card_front)
language_text = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))


word_text = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

yes_image = PhotoImage(file="images/right.png")
no_image = PhotoImage(file="images/wrong.png")
yes_button = Button(image=yes_image, highlightthickness=0, width=92, height=90, command=known_card)
yes_button.grid(column=0, row=1)
no_button = Button(image=no_image, highlightthickness=0, relief="flat", width=92, height=90, command=random_word)
no_button.grid(column=1, row=1)

random_word()
window.mainloop()
