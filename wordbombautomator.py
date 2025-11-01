import random
import pyautogui
import keyboard
import time
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import sys
class WordBomber:
    
    def __init__(self, root):
        self.root = root
        self.root.title("WorDumb (Makes you dumb for using this shit.)")
        self.root.geometry("350x220")
        self.root.resizable(False, False)

        self.used_words = []

        self.build_ui()


    

    def build_ui(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid()

        ttk.Label(main_frame, text="Enter Word:").grid(row=0, column=0, sticky="w")
        self.entry = ttk.Entry(main_frame, width=28)
        self.entry.grid(row=0, column=1, pady=5)
        self.entry.bind("<Return>", lambda e: self.on_search())

        ttk.Label(main_frame, text="Interval (sec):").grid(row=1, column=0, sticky="w")
        self.txt_interval = ttk.Entry(main_frame, width=10)
        self.txt_interval.insert(0, "0.1")
        self.txt_interval.grid(row=1, column=1, pady=5, sticky="w")

        self.humanize_var = tk.IntVar()
        
        humanize_check = ttk.Checkbutton(main_frame, text="Humanize", variable=self.humanize_var, command=self.toggle_humanize)
        humanize_check.grid(row=2, column=0, columnspan=2, pady=(10,0), sticky="w")

        self.humanize_frame = ttk.Frame(main_frame)
        ttk.Label(self.humanize_frame, text="Humanize Range (0.1-0.3):").grid(row=0, column=0, sticky="w")
        self.humanize_entry = ttk.Entry(self.humanize_frame, width=10)
        self.humanize_entry.insert(0, "0.1")
        self.humanize_entry.grid(row=0, column=1, padx=5)
        self.humanize_frame.grid_remove()

        self.mode_var = tk.StringVar(value="genius")
        ttk.Radiobutton(main_frame, text="Genius Mode", variable=self.mode_var, value="genius").grid(row=4, column=0, sticky="w", pady=(10,0))
        ttk.Radiobutton(main_frame, text="Simple Mode", variable=self.mode_var, value="simple").grid(row=4, column=1, sticky="w", pady=(10,0))
        
        ttk.Button(main_frame, text="Search", command=self.on_search).grid(row=6, column=0, columnspan=2, pady=15)

    def toggle_humanize(self):
        if self.humanize_var.get():
            self.humanize_frame.grid(row=3, column=0, columnspan=2, pady=(5,0), sticky="w")
            self.txt_interval.grid_remove()
        else:
            self.humanize_frame.grid_remove()
            self.txt_interval.grid(row=1, column=1, pady=5, sticky="w")


    def toggle_mode(self):
        mode = self.mode_var.get()
        if mode == "genius":
            ...
        elif mode == "simple":
            ...

    def type_word(self, word):
        pyautogui.moveTo(657, 200)
        pyautogui.click()
  

        base_delay = float(self.txt_interval.get())
        max_human = float(self.humanize_entry.get()) if self.humanize_var.get() else 0

        for letter in word.strip():
            if not letter.isalpha():
                continue

            key = letter.lower()
            keyboard.press(key)
            time.sleep(random.uniform(0.01, 0.03))
            keyboard.release(key)

            if self.humanize_var.get() and random.random() < 0.05:
                mistakes = random.randint(1, 2)
                for _ in range(mistakes):
                    wrong_key = random.choice('abcdefghijklmnopqrstuvwxyz')
                    keyboard.press_and_release(wrong_key)
                    time.sleep(random.uniform(0.05, 0.1))
                for _ in range(mistakes):
                    keyboard.press_and_release('backspace')
                    time.sleep(random.uniform(0.04, 0.09))


            delay = base_delay
            if self.humanize_var.get():
                delay += random.uniform(0.01, max_human)
                if random.random() < 0.08:
                    delay += random.uniform(0.2, 0.5)

            print(f"{key} = {delay:.3f}")
            time.sleep(delay)

        keyboard.press_and_release('enter')
        time.sleep(0.05)
        
    def resource_path(rel_path):
        if getattr(sys, '_MEIPASS', None):
            return Path(sys._MEIPASS) / rel_path
        return Path(rel_path)

    def on_search(self):
        query = self.entry.get().strip()
        if not query:
            return
        
        files = sorted(WordBomber.resource_path("words").glob('words*.txt'))

        selected_word = None
        seen = set() 

        mode = self.mode_var.get() 
        for file in files:
            if not file.exists():
                continue
            with file.open(encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line_clean = line.strip()
                    if not line_clean or line_clean in seen or line_clean in self.used_words:
                        continue
                    if query.lower() in line_clean.lower():
                        seen.add(line_clean)
                        if selected_word is None:
                            selected_word = line_clean
                        else:
                            if mode == "genius":
                                # pick the longest match
                                if len(line_clean) > len(selected_word):
                                    selected_word = line_clean
                            elif mode == "simple":
                                # pick the shortest match
                                if len(line_clean) < len(selected_word) and len(line_clean) > 5:
                                    selected_word = line_clean

        if not selected_word:
           
            return

        self.used_words.append(selected_word)
        self.type_word(selected_word)
        keyboard.send('alt+tab')


