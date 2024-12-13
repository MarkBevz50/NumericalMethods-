
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Середньоквадратичне")

        self.left_label = ctk.CTkLabel(self, text="Ліва межа")
        self.right_label = ctk.CTkLabel(self, text="Права межа")

        self.func_label = ctk.CTkLabel(self, text="Функція")
        self.number_label = ctk.CTkLabel(self, text="Кількість точок")
        self.aggregator_label = ctk.CTkLabel(self, text="Агрегатор наближення")

        self.left_entry = ctk.CTkEntry(self)
        self.right_entry = ctk.CTkEntry(self)
        self.func_entry = ctk.CTkEntry(self)
        self.number_entry = ctk.CTkEntry(self)

        # Dropdown menu for selecting approximation type
        self.aggregator_menu = ctk.CTkComboBox(self, values=["Лінійне (ax + b)", "Квадратичне (ax^2 + bx + c)", "Зворотне (a + b/x)"])

        # Grid layout setup
        self.left_label.grid(row=0, column=0, padx=5, pady=5)
        self.left_entry.grid(row=0, column=1, padx=5, pady=5)

        self.right_label.grid(row=1, column=0, padx=5, pady=5)
        self.right_entry.grid(row=1, column=1, padx=5, pady=5)

        self.func_label.grid(row=2, column=0, padx=5, pady=5)
        self.func_entry.grid(row=2, column=1, padx=5, pady=5)

        self.number_label.grid(row=3, column=0, padx=5, pady=5)
        self.number_entry.grid(row=3, column=1, padx=5, pady=5)

        self.aggregator_label.grid(row=4, column=0, padx=5, pady=5)
        self.aggregator_menu.grid(row=4, column=1, padx=5, pady=5)

        self.button = ctk.CTkButton(self, text="Показати", command=self.algo)
        self.button.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

    def fun_linear(self, x, data):
        return x[0] * data[:, 0] + x[1] - data[:, 1]

    def fun_quadratic(self, x, data):
        return x[0] * data[:, 0]**2 + x[1] * data[:, 0] + x[2] - data[:, 1]

    def fun_inverse(self, x, data):
        return x[0] + x[1] / data[:, 0] - data[:, 1]

    def algo(self):
        # Generate example data based on user input
        np.random.seed(0)
        self.x_data = np.linspace(float(self.left_entry.get()), float(self.right_entry.get()), int(self.number_entry.get()))
        self.interp_func = self.func_entry.get()

        # Parse the user-input function using SymPy
        x = sp.symbols('x')
        self.f_x = sp.sympify(self.interp_func)
        self.f_x_numeric = sp.lambdify(x, self.f_x, 'numpy')

        # Calculate y values using the user-defined function
        self.y = self.f_x_numeric(self.x_data)

        # Stack x and y data for least squares fitting
        data = np.column_stack((self.x_data, self.y))

        # Get the selected approximation type
        selected_aggregator = self.aggregator_menu.get()
        errors = []

        if selected_aggregator == "Лінійне (ax + b)":
            initial_params = np.array([1, 0])
            result = least_squares(self.fun_linear, initial_params, args=(data,), loss='linear')
            y_fit = result.x[0] * self.x_data + result.x[1]
            errors = (result.x[0] * self.x_data + result.x[1] - self.y)**2

            poly_form = "ax + b"
            params = result.x[:2]

        elif selected_aggregator == "Квадратичне (ax^2 + bx + c)":
            initial_params = np.array([1, 0, 0])
            result = least_squares(self.fun_quadratic, initial_params, args=(data,), loss='soft_l1')
            y_fit = result.x[0] * self.x_data**2 + result.x[1] * self.x_data + result.x[2]
            errors = (result.x[0] * self.x_data**2 + result.x[1] * self.x_data + result.x[2] - self.y)**2

            poly_form = "ax^2 + bx + c"
            params = result.x[:3]

        elif selected_aggregator == "Зворотне (a + b/x)":
            initial_params = np.array([1, 1])
            result = least_squares(self.fun_inverse, initial_params, args=(data,), loss='cauchy')
            y_fit = result.x[0] + result.x[1] / self.x_data
            errors = (result.x[0] + result.x[1] / self.x_data - self.y)**2

            poly_form = "a + b/x"
            params = result.x[:2]

        # Save errors to file
        with open("errors_RMS.txt", "a") as file:
            file.write(f"Function: {self.interp_func}\n")
            file.write(f"Interpolational poly: {poly_form}\n\n")
            
            # Write x values in the desired format
            file.write("x_i | ")
            file.write(" | ".join(f"{x:.2f}" for x in self.x_data))
            file.write(" |\n")

            # Write errors in the desired format
            file.write("err | ")
            file.write(" | ".join(f"{error:.2f}" for error in errors))
            file.write(" |\n")

        # Plot the results
        plt.figure(figsize=(8, 5))
        plt.plot(self.x_data, self.y, label='f(x)')
        plt.plot(self.x_data, y_fit, label='Fit', color='red')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()
        plt.title(f'Агрегатор: {selected_aggregator}')
        plt.show()

def open_method6_page():
    app = App()
    app.mainloop()
