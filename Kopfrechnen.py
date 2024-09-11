#       Schreibe ein Programm, das dem Benutzer fünf Rechenaufgaben stellt.
#
#       Welche Operatoren (+, -, *, %, /) jeweils benutzt werden,
#       soll per Zufall ermittel werden.
#       Jede Zahl und jedes Ergebnis der Rechenaufgaben muss eine ganze,
#       positive Zahl unter hundert sein.
#
#       Wenn der Benutzer seine Ergebnisse absendet,
#       soll ausgegeben werden, wieviele Ergebnisse richtig waren
#       und wie lange der Benutzer gebraucht hat.

import random
import operator
import time
import tkinter as tk

operators = [operator.add, operator.sub, operator.mul, operator.mod, operator.truediv]
operation_symbols = {
    operator.add: '+',
    operator.sub: '-',
    operator.mul: '*',
    operator.mod: '%',
    operator.truediv: '/'
}

def generate_problem(chosen_operator, level):
    if level == "Einfach":
        num_range = 10
    elif level == "Mittel":
        num_range = 100
    else:  # Schwer
        num_range = 1000

    while True:
        num1 = random.randint(0, num_range)
        if chosen_operator == operator.truediv:
            num2 = random.randint(1, num_range)
        else:
            num2 = random.randint(0, num_range)

        if num1 < num2 and (chosen_operator == operator.sub or chosen_operator == operator.truediv):
            continue

        try:
            result = chosen_operator(num1, num2)
        except ZeroDivisionError:
            continue

        if isinstance(result, float) and not result.is_integer():
            continue

        if 1 <= result < 1000:
            break

    operation_symbol = operation_symbols[chosen_operator]
    aufgabe = f"{num1} {operation_symbol} {num2}"
    return aufgabe, int(result)

class MathQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Quiz")

        self.level = tk.StringVar(value="Einfach")
        self.create_widgets()

    def create_widgets(self):
        self.label_intro = tk.Label(self.root, text="Wählen Sie die Schwierigkeitsstufe:", font=('Arial', 14))
        self.label_intro.pack(pady=10)

        self.radio_easy = tk.Radiobutton(self.root, text="Einfach", variable=self.level, value="Einfach", font=('Arial', 12))
        self.radio_easy.pack()
        
        self.radio_medium = tk.Radiobutton(self.root, text="Mittel", variable=self.level, value="Mittel", font=('Arial', 12))
        self.radio_medium.pack()
        
        self.radio_hard = tk.Radiobutton(self.root, text="Schwer", variable=self.level, value="Schwer", font=('Arial', 12))
        self.radio_hard.pack()

        self.button_start = tk.Button(self.root, text="Quiz Starten", command=self.start_quiz, font=('Arial', 14))
        self.button_start.pack(pady=20)

    def start_quiz(self):
        self.label_intro.pack_forget()
        self.radio_easy.pack_forget()
        self.radio_medium.pack_forget()
        self.radio_hard.pack_forget()
        self.button_start.pack_forget()

        # Reset previous results if they exist
        if hasattr(self, 'label_result'):
            self.label_result.pack_forget()
            del self.label_result
        if hasattr(self, 'button_restart'):
            self.button_restart.pack_forget()
            del self.button_restart
        if hasattr(self, 'button_quit'):
            self.button_quit.pack_forget()
            del self.button_quit

        self.current_task_index = 0
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.start_time = time.time()

        self.label_task = tk.Label(self.root, text="Bitte lösen Sie die Aufgabe:", font=('Arial', 14))
        self.label_task.pack(pady=10)
        
        self.task_var = tk.StringVar()
        self.label_problem = tk.Label(self.root, textvariable=self.task_var, font=('Arial', 18))
        self.label_problem.pack(pady=10)
        
        self.entry_answer = tk.Entry(self.root, font=('Arial', 14))
        self.entry_answer.pack(pady=10)
        
        self.button_submit = tk.Button(self.root, text="Antwort Überprüfen", command=self.check_answer, font=('Arial', 14))
        self.button_submit.pack(pady=10)
        
        self.label_feedback = tk.Label(self.root, font=('Arial', 14))
        self.label_feedback.pack(pady=10)
        
        self.next_task()
    
    def next_task(self):
        level = self.level.get()
        if (level == "Einfach" and self.incorrect_answers < 5) or \
           (level == "Mittel" and self.incorrect_answers < 3) or \
           (level == "Schwer" and self.incorrect_answers < 1):
            chosen_operator = random.choice(operators)
            self.current_task, self.current_result = generate_problem(chosen_operator, level)
            self.task_var.set(self.current_task)
            self.entry_answer.delete(0, tk.END)
            self.label_feedback.config(text="")
        else:
            self.end_quiz()
    
    def check_answer(self):
        try:
            user_answer = int(self.entry_answer.get())
            if user_answer == self.current_result:
                self.label_feedback.config(text="Richtig!", fg="green")
                self.correct_answers += 1
            else:
                self.label_feedback.config(text=f"Falsch! Die richtige Antwort ist {self.current_result}.", fg="red")
                self.incorrect_answers += 1
        except ValueError:
            self.label_feedback.config(text="Bitte geben Sie eine gültige Zahl ein.", fg="red")
            self.incorrect_answers += 1
        
        self.root.after(2000, self.next_task)
    
    def end_quiz(self):
        end_time = time.time()
        time_taken = end_time - self.start_time
        result_message = (f"Sie haben {self.correct_answers} Aufgaben richtig gelöst.\n"
                          f"Sie haben {time_taken:.2f} Sekunden gebraucht.")
        
        self.label_result = tk.Label(self.root, text=result_message, font=('Arial', 14))
        self.label_result.pack(pady=20)
        
        self.button_restart = tk.Button(self.root, text="Neu starten", command=self.restart_quiz, font=('Arial', 14))
        self.button_restart.pack(pady=10)
        
        self.button_quit = tk.Button(self.root, text="Beenden", command=self.root.destroy, font=('Arial', 14))
        self.button_quit.pack(pady=10)
    
    def restart_quiz(self):
        if hasattr(self, 'label_result'):
            self.label_result.pack_forget()
            del self.label_result
        if hasattr(self, 'button_restart'):
            self.button_restart.pack_forget()
            del self.button_restart
        if hasattr(self, 'button_quit'):
            self.button_quit.pack_forget()
            del self.button_quit
        
        self.start_quiz()

if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuizApp(root)
    root.mainloop()


    
        

    
    
