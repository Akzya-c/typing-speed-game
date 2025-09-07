import tkinter as tk
from tkinter import ttk, messagebox
import random
import time

# Sentences from easy to hard
sentences = [
    ("The cat runs", "Easy"),
    ("I love to read books", "Easy"),
    ("Coding is fun", "Easy"),
    ("The quick brown fox jumps over the lazy dog", "Medium"),
    ("Practice makes perfect", "Medium"),
    ("Typing speed games improve keyboard skills", "Medium"),
    ("Python programming is both powerful and versatile", "Hard"),
    ("Knowledge doubles when you share it with others", "Hard"),
    ("Debugging code trains the mind for logical thinking", "Hard"),
    ("Mastering programming requires patience and persistence", "Hard")
]

class TypingSpeedGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Game")
        self.root.geometry("750x500")
        self.root.config(bg="#1e1e1e")  # Dark background similar to coding themes
        
        # Title
        self.title_label = tk.Label(root, text="Typing Speed Game", font=("Courier New", 32, "bold"), fg="#00ff00", bg="#1e1e1e")
        self.title_label.pack(pady=(30, 15))
        
        # Sentence to type
        self.sentence_label = tk.Label(root, text="Click Start to begin", font=("Courier New", 20), fg="#c6c6c6", bg="#1e1e1e", wraplength=700, justify="center")
        self.sentence_label.pack(pady=20)
        
        # Input box
        self.text_entry = tk.Entry(root, font=("Courier New", 20), width=40, fg="#00ff00", bg="#121212", insertbackground="#00ff00", borderwidth=2, relief="sunken")
        self.text_entry.pack(pady=10)
        self.text_entry.config(state='disabled')
        
        # Progress bar style for dark theme
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("green.Horizontal.TProgressbar", troughcolor='#121212', bordercolor='#121212', background='#00ff00', lightcolor='#00ff00', darkcolor='#00cc00')
        self.progress = ttk.Progressbar(root, style="green.Horizontal.TProgressbar", orient="horizontal", length=500, mode="determinate")
        self.progress.pack(pady=15)
        
        # Buttons
        button_frame = tk.Frame(root, bg="#1e1e1e")
        button_frame.pack(pady=15)
        
        self.start_button = tk.Button(button_frame, text="Start", font=("Courier New", 16, "bold"), fg="#121212", bg="#00ff00", padx=20, pady=8, command=self.start_game)
        self.start_button.grid(row=0, column=0, padx=20)
        
        self.reset_button = tk.Button(button_frame, text="Reset", font=("Courier New", 16, "bold"), fg="#121212", bg="#007700", padx=20, pady=8, command=self.reset_game, state='disabled')
        self.reset_button.grid(row=0, column=1, padx=20)
        
        # Result label
        self.result_label = tk.Label(root, text="", font=("Courier New", 18), fg="#00ff00", bg="#1e1e1e")
        self.result_label.pack(pady=15)
        
        self.start_time = 0
        self.current_sentence_index = 0
        self.results = []
        
        self.text_entry.bind('<KeyRelease>', self.update_progress)
    
    def start_game(self):
        self.current_sentence_index = 0
        self.results = []
        self.start_button.config(state='disabled')
        self.reset_button.config(state='normal')
        self.load_sentence()
    
    def reset_game(self):
        self.sentence_label.config(text="Click Start to begin")
        self.text_entry.delete(0, tk.END)
        self.text_entry.config(state='disabled')
        self.start_button.config(state='normal')
        self.reset_button.config(state='disabled')
        self.result_label.config(text="")
        self.progress['value'] = 0
        self.results = []
        self.current_sentence_index = 0
    
    def load_sentence(self):
        if self.current_sentence_index >= len(sentences):
            self.text_entry.config(state='disabled')
            self.show_final_score()
            return
        sentence, diff = sentences[self.current_sentence_index]
        self.sentence_label.config(text=sentence)
        self.text_entry.config(state='normal')
        self.text_entry.delete(0, tk.END)
        self.text_entry.focus()
        self.progress['value'] = 0
        self.result_label.config(text="")
        self.start_time = time.time()
        self.current_diff = diff
    
    def update_progress(self, event):
        typed_len = len(self.text_entry.get())
        total_len = len(sentences[self.current_sentence_index][0])
        progress_percent = (typed_len / total_len) * 100 if total_len > 0 else 0
        self.progress['value'] = progress_percent
        
        if typed_len >= total_len:
            self.check_typing()
    
    def check_typing(self):
        end_time = time.time()
        typed_text = self.text_entry.get()
        original_text = sentences[self.current_sentence_index][0]
        
        time_taken = end_time - self.start_time
        words = len(original_text.split())
        wpm = (words / time_taken) * 60
        
        accuracy = self.calculate_accuracy(original_text, typed_text)
        result_text = f"Sentence {self.current_sentence_index+1}/10 - Speed: {wpm:.2f} WPM | Accuracy: {accuracy:.2f}%"
        self.result_label.config(text=result_text)
        
        self.results.append((self.current_diff, accuracy, time_taken))
        
        self.current_sentence_index += 1
        self.root.after(1500, self.load_sentence)
    
    def calculate_accuracy(self, original, typed):
        original_words = original.split()
        typed_words = typed.split()
        correct = sum(o == t for o, t in zip(original_words, typed_words))
        return (correct / len(original_words)) * 100 if original_words else 0
    
    def show_final_score(self):
        avg_accuracy = sum(acc for _, acc, _ in self.results) / len(self.results) if self.results else 0
        avg_time = sum(t for _, _, t in self.results) / len(self.results) if self.results else 0
        
        score_message = f"Final Results:\nAverage Accuracy: {avg_accuracy:.2f}%\nAverage Time: {avg_time:.2f} seconds\n\nGreat job!"
        messagebox.showinfo("Game Complete!", score_message)

if __name__ == "__main__":
    root = tk.Tk()
    game = TypingSpeedGame(root)
    root.mainloop()
