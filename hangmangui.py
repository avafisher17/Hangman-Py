import tkinter as tk
from tkinter import ttk
import random


class HangmanGame:

    def __init__(self):
        self.logic = HangmanLogic()

        # Main Window
        self.main_window = tk.Tk()
        self.main_window.title("*HANGMAN*")
        self.main_window.geometry("400x650")

        # Title Card Frame
        self.title_card_frame = ttk.Frame(self.main_window, padding="10 10 10 0")
        self.title_card_frame.pack(fill=tk.BOTH, expand=True)

        title = "--- * H * A * N * G * M * A * N * ---"
        tagline = ">>> Spell it or he'll swing! <<<"
        line1 = "Guess a letter to try and figure out the word"
        line2 = "7 incorrect guesses, and it's all over for poor Hangman!"

        tk.Label(self.title_card_frame, text=title, font=12).pack()
        tk.Label(self.title_card_frame, text=tagline, font=12).pack(pady=(0, 10))
        tk.Label(self.title_card_frame, text=line1).pack()
        tk.Label(self.title_card_frame, text=line2).pack()

        # Divider Frame
        divider = tk.Frame(self.main_window, height=2, bd=1, relief='sunken')
        divider.pack(fill='x', padx=25, pady=5)

        # Answer Dashes Frame
        self.answer_frame = ttk.Frame(self.main_window, padding="10 10 10 0")
        self.answer_frame.pack(fill=tk.BOTH, expand=True)

        self.answer = self.logic.choose_answer()
        self.answer_dashes = self.logic.answer_dashes(self.answer)
        self.guesses = []
        self.misses_left = 7

        self.answer_display = tk.StringVar()
        self.answer_display.set(" ".join(self.answer_dashes))

        tk.Label(self.answer_frame, text="Here is your word:").pack(pady=(0,10))
        answer_display_label = tk.Label(self.answer_frame, textvariable= self.answer_display, font=12, relief="raised")
        answer_display_label.pack(ipadx=10,ipady=10)

        # Game Message Frame
        self.message_frame = ttk.Frame(self.main_window, padding="10 10 10 0")
        self.message_frame.pack(fill=tk.BOTH, expand=True)

        self.message = tk.StringVar()
        self.message.set("Good Luck!")

        self.message_label = tk.Label(self.message_frame, textvariable=self.message)
        self.message_label.pack()

        # ASCII Art Frame
        self.art_frame = ttk.Frame(self.main_window, padding="10 0 10 0")
        self.art_frame.pack(fill=tk.BOTH, expand=True)

        self.gallows1 = "_______"
        self.gallows2 = "|/     |"
        self.gallows3 = tk.StringVar()
        self.gallows4 = tk.StringVar()
        self.gallows5 = tk.StringVar()
        self.gallows6 = tk.StringVar()
        self.gallows7 = "|       "
        self.gallows8 = "_|_       "

        self.gallows3.set("|       ")
        self.gallows4.set("|       ")
        self.gallows5.set("|       ")
        self.gallows6.set("|       ")

        tk.Label(self.art_frame, text=self.gallows1, font="Courier").pack()
        tk.Label(self.art_frame, text=self.gallows2, font="Courier").pack()
        self.gallows3_label = tk.Label(self.art_frame, textvariable=self.gallows3, font="Courier")
        self.gallows3_label.pack()
        self.gallows4_label = tk.Label(self.art_frame, textvariable=self.gallows4, font="Courier")
        self.gallows4_label.pack()
        self.gallows5_label = tk.Label(self.art_frame, textvariable=self.gallows5, font="Courier")
        self.gallows5_label.pack()
        self.gallows6_label = tk.Label(self.art_frame, textvariable=self.gallows6, font="Courier")
        self.gallows6_label.pack()
        tk.Label(self.art_frame, text=self.gallows7, font="Courier").pack()
        tk.Label(self.art_frame, text=self.gallows8, font="Courier").pack(pady=(0,10))


        # Guess Frame
        self.guess_frame = ttk.Frame(self.main_window, padding="10 10 25 10")
        self.guess_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.guess_frame, text="What is your guess?").pack(side="left", fill=tk.X, expand=True)
        self.entry = tk.Entry(self.guess_frame, width=20)
        self.entry.pack(side="left", padx=(0,10))

        # Submit Button
        self.submit_button = tk.Button(self.guess_frame, text="Guess", command=self.on_guess)
        self.submit_button.pack(side="right", ipadx=10,ipady=5, padx=(10,0))

        self.entry.bind("<Return>", lambda event: self.on_guess())
        self.submit_button.focus_set()

        #Display Guesses Frame
        self.display_guesses = ttk.Frame(self.main_window, padding="10 10 10 10")
        self.display_guesses.pack(fill=tk.BOTH, expand=True)

        self.guess_display = tk.StringVar()
        self.guess_display.set(self.guesses)

        tk.Label(self.display_guesses, text="You've tried...").pack(pady=(0,10))
        self.guess_display_label = tk.Label(self.display_guesses, textvariable=self.guess_display, font=11, relief="solid", wraplength=300)
        self.guess_display_label.pack(ipadx=10,ipady=10)

        # Main Loop
        self.main_window.mainloop()

    def on_guess(self):
        # Runs when "Submit" button is clicked
        guess = self.entry.get().lower()
        special_characters = ['~', '`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', '{', '[',
                              '}', '}',
                              '|', '\\', ':', ';', '\"', '\'', ',', '<', '.', '>', '?', '/', ' ']
        # Whole word guesses
        if len(guess) > 1:
            if guess == self.answer:
                outcome = "Yeehaw! That's it!"
                self.message.set(outcome)
                for index, letter in enumerate(self.answer):
                        self.answer_dashes[index] = letter
                self.answer_display.set(" ".join(self.answer_dashes))
            elif guess in self.guesses:
                outcome = "You already guessed that word! Try again"
                self.message.set(outcome)
            else:
                self.misses_left -= 1
                self.update_guesses(guess)
                outcome = "Sorry, your guess wasn't quite right!"
                self.message.set(outcome)
        # Single letter guesses
        elif len(guess) == 1:
            if guess.isdigit():
                outcome = "This word doesn't contain any numbers! Try again"
                self.message.set(outcome)
            elif guess in special_characters:
                outcome = "This word doesn't contain any special characters! Try again"
                self.message.set(outcome)
            elif guess in self.guesses:
                outcome = "You already guessed that letter! Try again"
                self.message.set(outcome)
            elif guess not in self.guesses:
                if guess in self.answer:
                    for index, letter in enumerate(self.answer):
                        if letter == guess:
                            self.answer_dashes[index] = guess
                            self.answer_display.set(" ".join(self.answer_dashes))
                    self.update_guesses(guess)
                    outcome = "Gotcha! You guessed one of the letters!"
                    self.message.set(outcome)
                if guess not in self.answer:
                    self.misses_left += -1
                    self.update_guesses(guess)
                    outcome = "Oops! That letter's not in this word!"
                    self.message.set(outcome)
            else:
                outcome = "That guess wasn't quite right. Take another shot!"
                self.message.set(outcome)
        if "_" not in self.answer_dashes:
            outcome = "Look at that! You did it!"
            self.message.set(outcome)
            self.update_guesses(guess)
            self.submit_button.config(command=lambda: None)
            self.entry.unbind("<Return>")
            self.success_screen()
        if self.misses_left == 0:
            outcome = "Oh no! Poor Hangman!"
            self.message.set(outcome)
            self.update_guesses(guess)
            self.art_screen(self.misses_left)
            self.submit_button.config(command=lambda: None)
            self.entry.unbind("<Return>")
            self.defeat_screen()
        self.art_screen(self.misses_left)
        self.entry.delete(0, tk.END)

    def update_guesses(self, guess):
        self.guesses.append(guess)
        self.guesses.append("/")
        self.guess_display.set(self.guesses)

    def art_screen(self, misses_left):
        if misses_left == 6:
            self.gallows3.set("|      0")
        elif misses_left == 5:
            self.gallows4.set("|      |")
        elif misses_left == 4:
            self.gallows4.set("|     \\|")
        elif misses_left == 3:
            self.gallows4.set(" |     \\|/")
        elif misses_left == 2:
            self.gallows5.set("|      |")
        elif misses_left == 1:
            self.gallows6.set("|     / ")
        elif misses_left == 0:
            self.gallows6.set(" |     / \\")

    def defeat_screen(self):
        # Runs when misses_left reaches 0
        defeat_window = tk.Toplevel(self.main_window)
        defeat_window.title("*DEFEAT*")
        defeat_window.geometry("400x550")

        # Defeat Frame
        defeat_frame = ttk.Frame(defeat_window, padding="10 10 10 10")
        defeat_frame.pack(fill=tk.BOTH, expand=True)

        title = "--- * D * E * F * E * A * T * ---"
        tagline = ">>> It's all over for poor Hangman! <<<"
        line1 = "The word you were looking for was"
        answer_reveal = tk.StringVar()
        answer_reveal.set(self.answer)
        line2 = "Better luck next time!"

        tk.Label(defeat_frame, text=title, font=12).pack()
        tk.Label(defeat_frame, text=tagline, font=12).pack(pady=(0, 10))
        tk.Label(defeat_frame, text=line1).pack(pady=(0, 10))
        answer_reveal_label = tk.Label(defeat_frame, textvariable=answer_reveal, font=11, relief="raised")
        answer_reveal_label.pack(ipadx=10, ipady=10, pady=(0, 10))
        tk.Label(defeat_frame, text=self.gallows1, font="Courier").pack()
        tk.Label(defeat_frame, text=self.gallows2, font="Courier").pack()
        tk.Label(defeat_frame, textvariable=self.gallows3, font="Courier").pack()
        tk.Label(defeat_frame, textvariable=self.gallows4, font="Courier").pack()
        tk.Label(defeat_frame, textvariable=self.gallows5, font="Courier").pack()
        tk.Label(defeat_frame, textvariable=self.gallows6, font="Courier").pack()
        tk.Label(defeat_frame, text=self.gallows7, font="Courier").pack()
        tk.Label(defeat_frame, text=self.gallows8, font="Courier").pack(pady=(0, 20))
        tk.Label(defeat_frame, text=line2).pack(pady=(0, 10))

        # Buttons Frame
        defeat_buttons_frame = ttk.Frame(defeat_window, padding="50 10 50 50")
        defeat_buttons_frame.pack(fill=tk.BOTH, expand=True)

        repeat_button = tk.Button(defeat_buttons_frame, text="Play Again", command=lambda: (defeat_window.destroy(), self.on_reset()))
        repeat_button.pack(side="left", ipadx=10,ipady=5)
        quit_button = tk.Button(defeat_buttons_frame, text="Quit", command=lambda: (defeat_window.destroy(), self.main_window.destroy()))
        quit_button.pack(side="right", ipadx=10,ipady=5)

    def success_screen(self):
        # Runs when correct word is guessed
        success_window = tk.Toplevel(self.main_window)
        success_window.title("*SUCCESS*")
        success_window.geometry("400x500")

        # Success Frame
        success_frame = ttk.Frame(success_window, padding="40 10 40 10")
        success_frame.pack(fill=tk.BOTH, expand=True)

        title = "--- * S * U * C * C * E * S * S * ---"
        tagline = ">>> You saved the Hangman! <<<"
        line1 = "You correctly guessed the word"
        answer_reveal = tk.StringVar()
        answer_reveal.set(" ".join(self.answer_dashes))
        line2 = tk.StringVar()
        if self.misses_left > 1:
            line2.set(f"with {self.misses_left} misses left!")
        else:
            line2.set(f"with a single miss left!")

        gallows1 = "_______  "
        gallows2 = "|/     |  "
        gallows3 = "|         "
        gallows4 = "|         "
        gallows5 = "|       0 "
        gallows6 = "|      \\|/"
        gallows7 = "|       | "
        gallows8 = " _|_     / \\  "

        line3 = tk.StringVar()
        if self.misses_left == 7:
            line3.set("Wow! A perfect run!")
        elif self.misses_left > 4:
            line3.set("You're pretty good at this!")
        elif self.misses_left == 4:
            line3.set("Good job!")
        elif self.misses_left > 1:
            line3.set("Whew! That was close!")
        else:
            line3.set("Just in the nick of time!")

        tk.Label(success_frame, text=title, font=12).pack()
        tk.Label(success_frame, text=tagline, font=12).pack(pady=(0, 10))
        tk.Label(success_frame, text=line1).pack(pady=(0, 10))
        answer_reveal_label = tk.Label(success_frame, textvariable=answer_reveal, font=11, relief="raised")
        answer_reveal_label.pack(ipadx=10, ipady=10, pady=(0, 10))
        line2_label = tk.Label(success_frame, textvariable=line2)
        line2_label.pack(pady=(0,10))
        tk.Label(success_frame, text=gallows1, font="Courier").pack()
        tk.Label(success_frame, text=gallows2, font="Courier").pack()
        tk.Label(success_frame, text=gallows3, font="Courier").pack()
        tk.Label(success_frame, text=gallows4, font="Courier").pack()
        tk.Label(success_frame, text=gallows5, font="Courier").pack()
        tk.Label(success_frame, text=gallows6, font="Courier").pack()
        tk.Label(success_frame, text=gallows7, font="Courier").pack()
        tk.Label(success_frame, text=gallows8, font="Courier").pack(pady=(0,10))
        line3_label = tk.Label(success_frame, textvariable=line3)
        line3_label.pack(pady=(0, 10))

        # Buttons Frame
        success_buttons_frame = ttk.Frame(success_window, padding="50 10 50 50")
        success_buttons_frame.pack(fill=tk.BOTH, expand=True)

        repeat_button = tk.Button(success_frame, text="Play Again", command=lambda: (success_window.destroy(), self.on_reset()))
        repeat_button.pack(side="left", ipadx=10, ipady=5)
        quit_button = tk.Button(success_frame, text="Quit", command=lambda: (success_window.destroy(), self.main_window.destroy()))
        quit_button.pack(side="right", ipadx=10, ipady=5)

    def on_reset(self):
        self.answer = self.logic.choose_answer()
        self.answer_dashes = self.logic.answer_dashes(self.answer)
        self.guesses = []
        self.misses_left = 7
        self.answer_display.set(" ".join(self.answer_dashes))
        self.message.set("Good Luck!")
        self.guess_display.set(self.guesses)
        self.gallows3.set("|       ")
        self.gallows4.set("|       ")
        self.gallows5.set("|       ")
        self.gallows6.set("|       ")
        self.submit_button.config(command=self.on_guess)
        self.entry.bind("<Return>", lambda event: self.on_guess())



class HangmanLogic:

    @staticmethod
    def choose_answer():
        with open("wordlist.txt", "r") as word_choice:
            possible_answers_list = []
            for word in word_choice:
                possible_answer = word.rstrip("\n")
                possible_answers_list.append(possible_answer)
            answer = random.choice(possible_answers_list)
            return answer

    @staticmethod
    def answer_dashes(answer):
        return ["_"] * len(answer)



game = HangmanGame()