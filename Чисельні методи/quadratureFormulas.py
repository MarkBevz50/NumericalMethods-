import customtkinter as ctk
from sympy import symbols, sympify

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Квадратурні формули")
        self.geometry("400x400")  # Set window size

        # Параметри графічного інтерфейсу
        self.label_function = ctk.CTkLabel(self, text="Підінтегральна функція:")
        self.entry_function = ctk.CTkEntry(self)

        self.label_lower_limit = ctk.CTkLabel(self, text="Нижня межа:")
        self.entry_lower_limit = ctk.CTkEntry(self)

        self.label_upper_limit = ctk.CTkLabel(self, text="Верхня межа:")
        self.entry_upper_limit = ctk.CTkEntry(self)

        self.label_accuracy = ctk.CTkLabel(self, text="Точність (епсилон):")
        self.entry_accuracy = ctk.CTkEntry(self)

        self.calculate_button = ctk.CTkButton(
            self, text="Обрахувати значення", command=self.calculate
        )

        # Поля для результатів кожного методу
        self.label_rectangle = ctk.CTkLabel(self, text="Метод прямокутників:")
        self.result_rectangle = ctk.CTkEntry(self, width=200)

        self.label_trapezoid = ctk.CTkLabel(self, text="Метод трапецій:")
        self.result_trapezoid = ctk.CTkEntry(self, width=200)

        self.label_simpson = ctk.CTkLabel(self, text="Метод Сімпсона:")
        self.result_simpson = ctk.CTkEntry(self, width=200)

        self.label_gauss = ctk.CTkLabel(self, text="Формула Гауса:")
        self.result_gauss = ctk.CTkEntry(self, width=200)

        # Встановлення компонентів
        self.setup_ui()
        self.function = None

    def setup_ui(self):
        # Розташування компонентів
        self.label_function.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_function.grid(row=0, column=1, padx=10, pady=5)

        self.label_lower_limit.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_lower_limit.grid(row=1, column=1, padx=10, pady=5)

        self.label_upper_limit.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_upper_limit.grid(row=2, column=1, padx=10, pady=5)

        self.label_accuracy.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.entry_accuracy.grid(row=3, column=1, padx=10, pady=5)

        self.calculate_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Розташування полів результатів
        self.label_rectangle.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.result_rectangle.grid(row=5, column=1, padx=10, pady=5)

        self.label_trapezoid.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.result_trapezoid.grid(row=6, column=1, padx=10, pady=5)

        self.label_simpson.grid(row=7, column=0, padx=10, pady=5, sticky="w")
        self.result_simpson.grid(row=7, column=1, padx=10, pady=5)

        self.label_gauss.grid(row=8, column=0, padx=10, pady=5, sticky="w")
        self.result_gauss.grid(row=8, column=1, padx=10, pady=5)

    def calculate(self):
        try:
            # Читання значень
            a = float(self.entry_lower_limit.get())
            b = float(self.entry_upper_limit.get())
            e = float(self.entry_accuracy.get())

            function_str = self.entry_function.get()
            self.function = sympify(function_str)

            # Розрахунок кожного методу
            rectangle_result = self.rectint(self.func, a, b, e)
            trapezoid_result = self.trapint(self.func, a, b, e)
            simpson_result = self.simpsons(self.func, a, b, e)
            gauss_result = self.gauss_quadrature_integration(self.func, a, b, nodes=4)

            # Відображення результатів
            self.result_rectangle.insert(0, f"{rectangle_result:.15f}")
            self.result_trapezoid.insert(0, f"{trapezoid_result:.15f}")
            self.result_simpson.insert(0, f"{simpson_result:.15f}")
            self.result_gauss.insert(0, f"{gauss_result:.15f}")

        except Exception as error:
            self.result_rectangle.insert(0, f"Помилка: {error}")
            self.result_trapezoid.delete(0, "end")
            self.result_simpson.delete(0, "end")
            self.result_gauss.delete(0, "end")

    def func(self, x_value):
        x = symbols('x')
        return self.function.subs(x, x_value)

    @staticmethod
    def rectint(f, a, b, e):
        n_intervals = 10
        while True:
            dx = (b - a) / n_intervals
            area_n = sum(f(a + (i + 0.5) * dx) * dx for i in range(n_intervals))

            n_intervals *= 2
            dx = (b - a) / n_intervals
            area_2n = sum(f(a + (i + 0.5) * dx) * dx for i in range(n_intervals))

            error = abs(area_2n - area_n) / 3
            if error < e:
                return area_2n

    @staticmethod
    def trapint(f, a, b, e):
        n_intervals = 10
        while True:
            dx = (b - a) / n_intervals
            area_n = sum((f(a + i * dx) + f(a + (i + 1) * dx)) * dx / 2 for i in range(n_intervals))

            n_intervals *= 2
            dx = (b - a) / n_intervals
            area_2n = sum((f(a + i * dx) + f(a + (i + 1) * dx)) * dx / 2 for i in range(n_intervals))

            error = abs(area_2n - area_n) / 3
            if error < e:
                return area_2n

    @staticmethod
    def simpsons(f, a, b, e):
        n_intervals = 10
        while True:
            if n_intervals % 2 == 1:
                n_intervals += 1
            dx = (b - a) / n_intervals

            area_n = f(a) + f(b)
            area_n += sum((4 if i % 2 != 0 else 2) * f(a + i * dx) for i in range(1, n_intervals))
            area_n *= dx / 3

            n_intervals *= 2
            if n_intervals % 2 == 1:
                n_intervals += 1
            dx = (b - a) / n_intervals

            area_2n = f(a) + f(b)
            area_2n += sum((4 if i % 2 != 0 else 2) * f(a + i * dx) for i in range(1, n_intervals))
            area_2n *= dx / 3

            error = abs(area_2n - area_n) / 15
            if error < e:
                return area_2n

    def gauss_quadrature_integration(self, f, a, b, nodes):
        if nodes == 4:
            z_arr = [-0.86113631, -0.33998104, 0.33998104, 0.86113631]
            A_arr = [0.34785485, 0.65214515, 0.65214515, 0.34785485]
        elif nodes == 8:
            z_arr = [-0.18343464, 0.18343464, -0.52553241, 0.52553241, -0.79666648, 0.79666648, -0.96028986, 0.96028986]
            A_arr = [0.36268378, 0.36268378, 0.31370665, 0.31370665, 0.22238103, 0.22238103, 0.10122854, 0.10122854]
        else:
            return None

        x_arr = [(a + b) / 2 + z * (b - a) / 2 for z in z_arr]
        return (b - a) / 2 * sum(A * f(x) for x, A in zip(x_arr, A_arr))

def open_method7_page():
    app = App()
    app.mainloop()

# Створення та запуск додатку
app = App()
app.mainloop()
