import random
import tkinter as tk  # GUI Library
from tkinter import messagebox
import nltk  # English words from dictionary library
from nltk.corpus import words

# Download the English words dataset from nltk
nltk.download("words")
english_words = set(words.words())


# converts it into lowercase
def is_valid_word(word):
    return word.lower() in english_words


def ai_guess():
    global attempts
    # possible letters include whole abc
    possible_letters = [letter for letter in "abcdefghijklmnopqrstuvwxyz" if letter not in guessed_letters]

    # If the AI has not made any correct guesses yet it randomly selects a letter.
    if not guessed_letters:
        ai_letter = random.choice(possible_letters)
    else:
        # If there are only 1 or 2 letters left to guess use a more exhaustive search
        if len(word_to_guess) - len(guessed_letters) <= 2:
            ai_letter = exhaustive_search(word_to_guess, guessed_letters, possible_letters)
        else:
            # Otherwise use the binary search approach to find the best letter to guess.
            ai_letter = binary_search(word_to_guess, guessed_letters, possible_letters)

        # If the binary search didn't find a suitable letter, use heuristic approach
        if not ai_letter:
            ai_letter = heuristic_guess(possible_letters)

    guessed_letters.append(ai_letter)
    # if correct word is guessed generate a message along with the word else generate the incorrect word message
    if ai_letter in word_to_guess:
        status_label.config(text=f"AI guessed '{ai_letter}' and found a correct letter!")
    else:
        status_label.config(text=f"AI guessed '{ai_letter}' and found a wrong letter!")
        attempts += 1

    draw_hangman()  # draws hangman as function is called
    display_word()  # displays the words found
    attempts_label.config(text=f"Attempts left: {8 - attempts}")  # deducts wrong attempts
    check_game_status()
    # if word has not been correctly guessed then adds 3 seconds delay and starts again by calling ai_guess function
    if " _ " in word_display.get() and attempts < 8:
        root.after(3000, ai_guess)  # Delay 3 second before the next AI guess


# binary search algorithm to guess the word
def binary_search(word, guessed_letters, possible_letters):
    left = 0
    right = len(possible_letters) - 1

    while left <= right:
        mid = (left + right) // 2
        guess = possible_letters[mid]

        # Check if the letter is already guessed or not.
        if guess in guessed_letters:
            return possible_letters[mid + 1] if mid + 1 <= right else possible_letters[mid - 1]

        # Check if the guessed letter is in the word.
        if guess in word:
            return guess
        elif guess < word[0]:
            left = mid + 1
        else:
            right = mid - 1

    return possible_letters[0]  # If no match is found, return the first letter.


# gneerates a score of for every letter based on its frequency
def heuristic_guess(possible_letters):
    # Use heuristic approach to calculate the score for each possible letter based on English character frequencies
    # English character frequencies to use in the heuristic function
    # Link: https://en.wikipedia.org/wiki/Letter_frequency
    english_frequencies = {
        'e': 0.12702, 't': 0.09056, 'a': 0.08167, 'o': 0.07507, 'i': 0.06966,
        'n': 0.06749, 's': 0.06327, 'h': 0.06094, 'r': 0.05987, 'd': 0.04253,
        'l': 0.04025, 'c': 0.02782, 'u': 0.02758, 'm': 0.02406, 'w': 0.02360,
        'f': 0.02228, 'g': 0.02015, 'y': 0.01974, 'p': 0.01929, 'b': 0.01492,
        'v': 0.00978, 'k': 0.00772, 'j': 0.00153, 'x': 0.00150, 'q': 0.00095,
        'z': 0.00074
    }

    # Calculate the score for each possible letter based on its frequency
    scores = {letter: english_frequencies.get(letter, 0) for letter in possible_letters}

    # Choose the letter with the highest score as the guess
    best_letter = max(scores, key=scores.get)
    return scores[best_letter]


# this function best works when the AI has guessed 80%-90% of the word
def exhaustive_search(word, guessed_letters, possible_letters):
    # Exhaustive search to find the remaining letters

    remaining_letters = [letter for letter in word if letter not in guessed_letters] #
    best_letter = None
    max_score = -1.0  # Initialize as the minimum score possible

    for letter in remaining_letters:
        # Calculate the score for each possible remaining letter based on its frequency
        score = heuristic_guess([letter])
        if score > max_score:
            max_score = score
            best_letter = letter

    return best_letter


# method to call ai_guess method
def start_ai_guess():
    ai_guess()


# initial game menu
def start_game():
    global word_to_guess, guessed_letters, attempts
    word_to_guess = user_input.get().lower()
    if not word_to_guess.isalpha():
        messagebox.showwarning("Invalid Input!!", "Please enter a valid word (only alphabetic characters).")
        return
    if not word_to_guess:
        messagebox.showwarning("Invalid Input!!", "Please enter a word.")
        return

    guessed_letters = []
    attempts = 0

    user_input.config(state=tk.DISABLED)
    start_button.config(state=tk.DISABLED)
    start_ai_guess()


# display word function
def display_word():
    display = ""
    for letter in word_to_guess:
        if letter in guessed_letters:
            display += letter
        else:
            display += " _ "
    word_display.set(display)


# draws hangman on incorrect attempt
def draw_hangman():
    hangman_parts = [
        "  O  ",
        " /|\ ",
        " /|\ ",
    ]
    for i in range(len(hangman_draw)):
        if i < attempts:
            canvas.itemconfig(hangman_draw[i], text=hangman_parts[i])
        else:
            canvas.itemconfig(hangman_draw[i], text="")


# checks whether game has been finished or not
def check_game_status():
    if " _ " not in word_display.get():
        messagebox.showinfo("Victory is mine!", "Better Luck next time.")
        root.destroy()

    if attempts == 8:
        messagebox.showinfo("Game Over", "You're a worthy opponent")
        root.destroy()


# all the code for the GUI of the this game
root = tk.Tk()
root.title("Hangman Game - Play against AI")

word_to_guess = ""
guessed_letters = []
attempts = 0

canvas = tk.Canvas(root, width=200, height=200)
canvas.pack()

# Create the hangman parts (head, body, legs)
hangman_draw = []
for i in range(3):
    hangman_part = canvas.create_text(100, 70 + 30 * i, text="", font=("Arial", 16))
    hangman_draw.append(hangman_part)


word_display = tk.StringVar()
display_word()
status_label = tk.Label(root, text="HANGMAN", font=("Times New Roman", 28))
status_label.pack(pady=5)
status_label = tk.Label(root, text="It's YOU vs ME!! Be my guest and prove to me that you're a worthy opponent.", font=("Times New Roman", 12))
status_label.pack(pady=5)
word_label = tk.Label(root, textvariable=word_display, font=("Times New Roman", 20))
word_label.pack(pady=10)

attempts_label = tk.Label(root, text="Attempts left: 8", font=("Times New Roman", 12))
attempts_label.pack(pady=5)

status_label = tk.Label(root, text="Welcome! Enter a word for me to guess.", font=("Times New Roman", 12))
status_label.pack(pady=5)

user_input = tk.Entry(root, width=20, font=("Times New Roman", 12))
user_input.pack(pady=5)

start_button = tk.Button(root, text="Let's begin our journey!!", command=start_game)
start_button.pack(pady=5)

root.mainloop()
