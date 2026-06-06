import random
import tkinter as tk

from tkinter import ttk, font

from vocabulary_quiz_app.quiz_logic import Word, check_answer, draw_word


easy_words = [
    Word("apple", "사과"),
    Word("book", "책"),
    Word("chair", "의자"),
    Word("door", "문"),
    Word("water", "물"),
]

normal_words = [
    Word("flower", "꽃"),
    Word("friend", "친구"),
    Word("music", "음악"),
    Word("school", "학교"),
    Word("summer", "여름"),
]

hard_words = [
    Word("knowledge", "지식"),
    Word("environment", "환경"),
    Word("responsibility", "책임"),
    Word("opportunity", "기회"),
    Word("imagination", "상상력"),
]


class DifficultyVocabularyQuizApp:
    def __init__(self, root):
        self.root = root
        self.rng = random.Random()

        self.current_word = None
        self.words = easy_words
        self.score = 0
        self.total = 0
        self.checked = False

        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="NanumGothic", size=12)

        self.root.title("Vocabulary Quiz - Difficulty")
        self.root.geometry("440x330")
        self.root.resizable(False, False)

        self.difficulty_var = tk.StringVar()
        self.difficulty_var.set("쉬움")

        self.word_var = tk.StringVar()
        self.word_var.set("단어를 불러오는 중...")

        self.feedback_var = tk.StringVar()
        self.feedback_var.set("")

        self.score_var = tk.StringVar()
        self.score_var.set("Score: 0/0")

        ttk.Label(self.root, text="단어 난이도").pack(pady=(16, 4))

        self.difficulty_box = ttk.Combobox(
            self.root,
            textvariable=self.difficulty_var,
            values=["쉬움", "보통", "어려움"],
            state="readonly",
            width=14,
        )
        self.difficulty_box.pack()
        self.difficulty_box.bind("<<ComboboxSelected>>", self.change_difficulty)

        ttk.Label(self.root, text="영단어").pack(pady=(18, 4))
        ttk.Label(self.root, textvariable=self.word_var, font=("NanumGothic", 24)).pack()

        self.answer_entry = ttk.Entry(self.root, font=("NanumGothic", 14))
        self.answer_entry.pack(pady=12, ipadx=6, ipady=4)
        self.answer_entry.bind("<Return>", self.check_answer_button)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=6)

        self.check_button = ttk.Button(
            button_frame,
            text="채점",
            command=self.check_answer_button,
        )
        self.check_button.pack(side=tk.LEFT, padx=6)

        self.next_button = ttk.Button(
            button_frame,
            text="다음",
            command=self.next_word,
        )
        self.next_button.pack(side=tk.LEFT, padx=6)

        ttk.Label(self.root, textvariable=self.feedback_var).pack(pady=8)
        ttk.Label(self.root, textvariable=self.score_var).pack()

        self.next_word()

    def change_difficulty(self, event=None):
        difficulty = self.difficulty_var.get()

        if difficulty == "쉬움":
            self.words = easy_words
        elif difficulty == "보통":
            self.words = normal_words
        else:
            self.words = hard_words

        self.score = 0
        self.total = 0
        self.score_var.set("Score: 0/0")
        self.next_word()

    def next_word(self):
        self.current_word = draw_word(self.words, self.rng)
        self.word_var.set(self.current_word.term)
        self.answer_entry.delete(0, tk.END)
        self.feedback_var.set("")
        self.checked = False
        self.check_button.state(["!disabled"])
        self.answer_entry.focus()

    def check_answer_button(self, event=None):
        if self.current_word is None:
            return

        if self.checked:
            return

        self.checked = True
        self.total = self.total + 1

        user_answer = self.answer_entry.get()

        if check_answer(self.current_word, user_answer):
            self.score = self.score + 1
            self.feedback_var.set("정답입니다!")
        else:
            answer_text = "오답입니다. 정답: " + self.current_word.meaning
            self.feedback_var.set(answer_text)

        score_text = "Score: " + str(self.score) + "/" + str(self.total)
        self.score_var.set(score_text)
        self.check_button.state(["disabled"])


def main():
    root = tk.Tk()
    DifficultyVocabularyQuizApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
