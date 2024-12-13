import numpy as np
import matplotlib.pyplot as plt
import customtkinter as ctk
from sympy import symbols, sympify
from GaussianMethod import GMethod


class BoundaryValueProblemSolver(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Крайова задача другого порядку")
        self.geometry("1000x900")
        self.resizable(False, False)

        # Введення коефіцієнтів рівняння
        ctk.CTkLabel(self, text="Коефіцієнти рівняння").grid(row=0, column=0, columnspan=2, pady=10)

        self.p_x_label = ctk.CTkLabel(self, text="p(x):")
        self.p_x_label.grid(row=1, column=0, padx=5, pady=5)
        self.p_x_entry = ctk.CTkEntry(self)
        self.p_x_entry.grid(row=1, column=1, padx=5, pady=5)

        self.q_x_label = ctk.CTkLabel(self, text="q(x):")
        self.q_x_label.grid(row=2, column=0, padx=5, pady=5)
        self.q_x_entry = ctk.CTkEntry(self)
        self.q_x_entry.grid(row=2, column=1, padx=5, pady=5)

        self.f_x_label = ctk.CTkLabel(self, text="f(x):")
        self.f_x_label.grid(row=3, column=0, padx=5, pady=5)
        self.f_x_entry = ctk.CTkEntry(self)
        self.f_x_entry.grid(row=3, column=1, padx=5, pady=5)

        # Введення граничних умов
        ctk.CTkLabel(self, text="Граничні умови").grid(row=4, column=0, columnspan=2, pady=10)

        self.alpha0_label = ctk.CTkLabel(self, text="α₀:")
        self.alpha0_label.grid(row=5, column=0, padx=5, pady=5)
        self.alpha0_entry = ctk.CTkEntry(self)
        self.alpha0_entry.grid(row=5, column=1, padx=5, pady=5)

        self.beta0_label = ctk.CTkLabel(self, text="β₀:")
        self.beta0_label.grid(row=6, column=0, padx=5, pady=5)
        self.beta0_entry = ctk.CTkEntry(self)
        self.beta0_entry.grid(row=6, column=1, padx=5, pady=5)

        self.gamma0_label = ctk.CTkLabel(self, text="γ₀:")
        self.gamma0_label.grid(row=7, column=0, padx=5, pady=5)
        self.gamma0_entry = ctk.CTkEntry(self)
        self.gamma0_entry.grid(row=7, column=1, padx=5, pady=5)

        self.alpha1_label = ctk.CTkLabel(self, text="α₁:")
        self.alpha1_label.grid(row=8, column=0, padx=5, pady=5)
        self.alpha1_entry = ctk.CTkEntry(self)
        self.alpha1_entry.grid(row=8, column=1, padx=5, pady=5)

        self.beta1_label = ctk.CTkLabel(self, text="β₁:")
        self.beta1_label.grid(row=9, column=0, padx=5, pady=5)
        self.beta1_entry = ctk.CTkEntry(self)
        self.beta1_entry.grid(row=9, column=1, padx=5, pady=5)

        self.gamma1_label = ctk.CTkLabel(self, text="γ₁:")
        self.gamma1_label.grid(row=10, column=0, padx=5, pady=5)
        self.gamma1_entry = ctk.CTkEntry(self)
        self.gamma1_entry.grid(row=10, column=1, padx=5, pady=5)

        # Введення точного розв’язку
        self.accurate_func_label = ctk.CTkLabel(self, text="Точний розв’язок (y(x)):")
        self.accurate_func_label.grid(row=11, column=0, padx=5, pady=5)
        self.accurate_func_entry = ctk.CTkEntry(self)
        self.accurate_func_entry.grid(row=11, column=1, padx=5, pady=5)

        # Введення параметрів для графіка
        ctk.CTkLabel(self, text="Параметри графіка").grid(row=12, column=0, columnspan=2, pady=10)

        self.a_label = ctk.CTkLabel(self, text="a:")
        self.a_label.grid(row=13, column=0, padx=5, pady=5)
        self.a_entry = ctk.CTkEntry(self)
        self.a_entry.grid(row=13, column=1, padx=5, pady=5)

        self.b_label = ctk.CTkLabel(self, text="b:")
        self.b_label.grid(row=14, column=0, padx=5, pady=5)
        self.b_entry = ctk.CTkEntry(self)
        self.b_entry.grid(row=14, column=1, padx=5, pady=5)

        self.h_label = ctk.CTkLabel(self, text="h:")
        self.h_label.grid(row=15, column=0, padx=5, pady=5)
        self.h_entry = ctk.CTkEntry(self)
        self.h_entry.grid(row=15, column=1, padx=5, pady=5)

        # Кнопка для запуску обчислень
        self.solve_button = ctk.CTkButton(self, text="Розв’язати", command=self.solve)
        self.solve_button.grid(row=16, column=0, columnspan=2, pady=20)

    def linear_bvp_solver(self, a, b, h, alpha0, beta0, gamma0, alpha1, beta1, gamma1):
        n = int((b - a) / h) + 1
        x_values = np.linspace(a, b, n)

        matrix = np.zeros((n, n))
        vect = np.zeros(n)

        for i in range(1, n - 1):
            xi = x_values[i]
            matrix[i, i - 1] = 1 / h**2 - self.p_function.evalf(subs={"x": xi}) / (2 * h)
            matrix[i, i] = -2 / h**2 + self.q_function.evalf(subs={"x": xi})
            matrix[i, i + 1] = 1 / h**2 + self.p_function.evalf(subs={"x": xi}) / (2 * h)
            vect[i] = self.f_function.evalf(subs={"x": xi})

        matrix[0, 0] = alpha0 - beta0 / h
        matrix[0, 1] = beta0 / h
        vect[0] = gamma0

        matrix[-1, -1] = alpha1 + beta1 / h
        matrix[-1, -2] = -beta1 / h
        vect[-1] = gamma1

        solution = GMethod(matrix.tolist(), vect.tolist())
        return x_values, solution


    def solve(self):
        try:
            # Зчитування значень з інтерфейсу
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            h = float(self.h_entry.get())

            alpha0 = float(self.alpha0_entry.get())
            beta0 = float(self.beta0_entry.get())
            gamma0 = float(self.gamma0_entry.get())
            alpha1 = float(self.alpha1_entry.get())
            beta1 = float(self.beta1_entry.get())
            gamma1 = float(self.gamma1_entry.get())

            self.p_function = sympify(self.p_x_entry.get())
            self.q_function = sympify(self.q_x_entry.get())
            self.f_function = sympify(self.f_x_entry.get())

            # Зчитування та підготовка точного розв’язку
            accurate_func_str = self.accurate_func_entry.get()
            if accurate_func_str:
                accurate_func = sympify(accurate_func_str)
            else:
                accurate_func = None

            # Розв'язання чисельної задачі
            x, y_numeric = self.linear_bvp_solver(a, b, h, alpha0, beta0, gamma0, alpha1, beta1, gamma1)

            # Обчислення точного розв’язку (якщо задано)
            if accurate_func:
                y_accurate = [accurate_func.evalf(subs={"x": xi}) for xi in x]
                errors = [abs(y_num - y_acc) for y_num, y_acc in zip(y_numeric, y_accurate)]
            else:
                y_accurate = None
                errors = None

            # Побудова графіка чисельного розв’язку
            plt.figure(figsize=(10, 6))
            plt.plot(x, y_numeric, label="Чисельний розв’язок", linestyle="-", color="blue")

            # Побудова графіка точного розв’язку (якщо заданий)
            if y_accurate:
                plt.plot(x, y_accurate, label="Точний розв’язок", linestyle="--", color="red")

            # Додавання підписів і легенди
            plt.xlabel("x")
            plt.ylabel("y")
            plt.title("Розв’язок крайової задачі")
            plt.legend()
            plt.grid()
            plt.show()

            # Побудова графіка похибки (якщо заданий точний розв’язок)
            if errors:
                plt.figure(figsize=(10, 6))
                plt.plot(x, errors, label="Похибка", linestyle="-", color="green")
                plt.xlabel("x")
                plt.ylabel("Похибка")
                plt.title("Графік похибки")
                plt.legend()
                plt.grid()
                plt.show()

            # Запис похибок у файл
            if errors:
                with open("errorsBoundaries.txt", "a") as file:
                    # Запис заголовків
                    file.write("x values:\\n")
                    file.write(" ".join(map(lambda v: str(round(v, 3)), np.ravel(x))) + "\\n")
                    file.write("Errors:\\n")
                    file.write(" ".join(map(lambda v: str(round(v, 3)), np.ravel(errors))) + "\\n")
                    file.write("---" * 20 + "\\n")
                print("Результати записано у файл 'errorsBoundaries.txt'")

        except Exception as e:
            print(f"Помилка: {e}")

def open_method9_page():
    app = BoundaryValueProblemSolver()
    app.mainloop()

if __name__ == "__main__":
    app = BoundaryValueProblemSolver()
    app.mainloop()
