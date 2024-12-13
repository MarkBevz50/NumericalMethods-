import customtkinter as ctk
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal, InvalidOperation

# Функція для обчислення кореня методом Ньютона
def newton_method(equation, guess, epsilon):
    x = sp.symbols('x')
    f = sp.sympify(equation)
    f_prime = sp.diff(f, x)
    
    current_guess = guess
    while True:
        next_guess = current_guess - f.subs(x, current_guess) / f_prime.subs(x, current_guess)
        if abs(next_guess - current_guess) < epsilon:
            return next_guess
        current_guess = next_guess

# Функція для обчислення кореня методом простих ітерацій
def simple_iteration_method(g_function, guess, epsilon):
    x = sp.symbols('x')
    g = sp.sympify(g_function)
    
    current_guess = guess
    while True:
        next_guess = g.subs(x, current_guess)
        if abs(next_guess - current_guess) < epsilon:
            return next_guess
        current_guess = next_guess

# Клас для інтерфейсу роботи з нелінійними рівняннями
class NonLinearApp(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.widgets = []
        self.menu()

    def menu(self):
        frame = ctk.CTkFrame(self)
        
        # Введення рівняння
        equation_label = ctk.CTkLabel(frame, text="Рівняння:")
        self.entry_equation = ctk.CTkEntry(frame)
        equation_label.grid(row=0, column=0, padx=5, pady=5)
        self.entry_equation.grid(row=0, column=1, padx=5, pady=5)
        
        # Введення функції g(x)
        g_function_label = ctk.CTkLabel(frame, text="Функція g(x):")
        self.entry_g_function = ctk.CTkEntry(frame)
        g_function_label.grid(row=1, column=0, padx=5, pady=5)
        self.entry_g_function.grid(row=1, column=1, padx=5, pady=5)
        
        # Введення початкового значення
        guess_label = ctk.CTkLabel(frame, text="Початкове значення:")
        self.entry_guess = ctk.CTkEntry(frame)
        guess_label.grid(row=2, column=0, padx=5, pady=5)
        self.entry_guess.grid(row=2, column=1, padx=5, pady=5)
        
        # Введення точності (epsilon)
        epsilon_label = ctk.CTkLabel(frame, text="Точність (ε):")
        self.entry_epsilon = ctk.CTkEntry(frame)
        epsilon_label.grid(row=3, column=0, padx=5, pady=5)
        self.entry_epsilon.grid(row=3, column=1, padx=5, pady=5)
        
        # Вибір методу
        method_label = ctk.CTkLabel(frame, text="Оберіть метод:")
        self.method_combobox = ctk.CTkComboBox(frame, values=["Метод Ньютона", "Метод Простих Ітерацій"])
        self.method_combobox.set("Метод Ньютона")
        method_label.grid(row=4, column=0, padx=5, pady=5)
        self.method_combobox.grid(row=4, column=1, padx=5, pady=5)
        
        # Кнопка для обчислення кореня
        calculate_button = ctk.CTkButton(frame, text="Знайти розв'язок", command=self.calculate_root)
        calculate_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        
        # Кнопка для побудови графіку
        plot_button = ctk.CTkButton(frame, text="Накреслити графік", command=self.plot_graph)
        plot_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
        
        # Виведення результатів
        self.result_label = ctk.CTkLabel(frame, text="")
        self.result_label.grid(row=7, column=0, columnspan=2, padx=5, pady=5)
        
        frame.pack(pady=10)

    def calculate_root(self):
        # Отримуємо дані з полів введення
        equation = self.entry_equation.get()
        g_function = self.entry_g_function.get()
        try:
            guess = Decimal(self.entry_guess.get())
            epsilon = Decimal(self.entry_epsilon.get())
        except InvalidOperation:
            self.result_label.configure(text="Помилка: введено неправильні значення!")
            return

        method = self.method_combobox.get()

        try:
            if method == "Метод Ньютона":
                result = newton_method(equation, guess, epsilon)
            elif method == "Метод Простих Ітерацій":
                result = simple_iteration_method(g_function, guess, epsilon)
            self.result_label.configure(text=f"Розв'язок: {result}")
        except Exception as e:
            self.result_label.configure(text=f"Помилка обчислення: {str(e)}")

    def plot_graph(self):
        # Виведення графіку функції
        equation = self.entry_equation.get()
        x = sp.symbols('x')
        f = sp.sympify(equation)

        x_vals = np.linspace(-10, 10, 400)
        y_vals = [f.subs(x, val) for val in x_vals]
        
        plt.plot(x_vals, y_vals, label=f"{equation}")
        plt.axhline(0, color='gray', lw=0.5)
        plt.axvline(0, color='gray', lw=0.5)
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.title("Графік функції")
        plt.legend()
        plt.grid(True)
        plt.show()

# Функція для відкриття вікна з нелінійними рівняннями
def open_method3_page():
    method3_window = ctk.CTkToplevel()
    method3_window.title("Нелінійні рівняння")
    method3_window.geometry("600x400")

    NonLinearApp(method3_window)

# Головне вікно програми
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Головне вікно")
    
    open_method_button = ctk.CTkButton(root, text="Відкрити метод Нелінійних рівнянь", command=open_method3_page)
    open_method_button.pack(pady=20)
    
    root.mainloop()
