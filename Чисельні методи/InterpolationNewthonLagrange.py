import customtkinter as CTk
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.interpolate import lagrange


class InterpolationApp(CTk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.menu()
        self.canvas = None

    def menu(self):
        frame = CTk.CTkFrame(self)
        frame.pack(pady=10)

        self.label1 = CTk.CTkLabel(frame, text="Введіть функцію:", font=("Georgia", 18))
        self.label1.grid(row=0, column=0, padx=5, pady=5)
        self.entry1 = CTk.CTkEntry(frame)
        self.entry1.grid(row=0, column=1, padx=5, pady=5)

        self.label0 = CTk.CTkLabel(frame, text="Введіть n:", font=("Georgia", 18))
        self.label0.grid(row=1, column=0, padx=5, pady=5)
        self.entry0 = CTk.CTkEntry(frame)
        self.entry0.grid(row=1, column=1, padx=5, pady=5)

        self.label2 = CTk.CTkLabel(frame, text="Введіть початок проміжку a:", font=("Georgia", 18))
        self.label2.grid(row=2, column=0, padx=5, pady=5)
        self.entry2 = CTk.CTkEntry(frame)
        self.entry2.grid(row=2, column=1, padx=5, pady=5)

        self.label3 = CTk.CTkLabel(frame, text="Введіть кінець проміжку b:", font=("Georgia", 18))
        self.label3.grid(row=3, column=0, padx=5, pady=5)
        self.entry3 = CTk.CTkEntry(frame)
        self.entry3.grid(row=3, column=1, padx=5, pady=5)

        self.button1 = CTk.CTkButton(frame, text="Побудувати графік", font=("Georgia", 18), command=self.draw_graph)
        self.button1.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def draw_graph(self):
        x = sp.symbols('x')
        y = sp.sympify(self.entry1.get())

        n = int(self.entry0.get())
        a = float(self.entry2.get())
        b = float(self.entry3.get())

        f = sp.lambdify(x, y, 'numpy')

        equal_nodes = np.linspace(a, b, n)
        chebyshev_nodes = np.polynomial.chebyshev.chebpts2(n) * (b - a) / 2 + (a + b) / 2

        equal_y_vals = f(equal_nodes)
        chebyshev_y_vals = f(chebyshev_nodes)

        newton_equal = self.newton_interpolation(equal_nodes, equal_y_vals)
        newton_chebyshev = self.newton_interpolation(chebyshev_nodes, chebyshev_y_vals)

        lagrange_equal = lagrange(equal_nodes, equal_y_vals)
        lagrange_chebyshev = lagrange(chebyshev_nodes, chebyshev_y_vals)

        x_vals = np.linspace(a, b, 500)
        y_vals = f(x_vals)
        newton_equal_vals = newton_equal(x_vals)
        newton_chebyshev_vals = newton_chebyshev(x_vals)
        lagrange_equal_vals = lagrange_equal(x_vals)
        lagrange_chebyshev_vals = lagrange_chebyshev(x_vals)

        # Midpoints for error calculation
        mid_equal_nodes = (equal_nodes[:-1] + equal_nodes[1:]) / 2
        mid_chebyshev_nodes = (chebyshev_nodes[:-1] + chebyshev_nodes[1:]) / 2

        mid_equal_y_vals = f(mid_equal_nodes)
        mid_chebyshev_y_vals = f(mid_chebyshev_nodes)

        error_newton_equal = np.abs(mid_equal_y_vals - newton_equal(mid_equal_nodes))
        error_newton_chebyshev = np.abs(mid_chebyshev_y_vals - newton_chebyshev(mid_chebyshev_nodes))
        error_lagrange_equal = np.abs(mid_equal_y_vals - lagrange_equal(mid_equal_nodes))
        error_lagrange_chebyshev = np.abs(mid_chebyshev_y_vals - lagrange_chebyshev(mid_chebyshev_nodes))

        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        fig, axes = plt.subplots(4, 2, figsize=(16, 16))

        # Поліноми Ньютона та похибка для рівновіддалених вузлів
        axes[0, 0].plot(x_vals, y_vals, label="Original Function", color="blue")
        axes[0, 0].plot(x_vals, newton_equal_vals, label="Newton Interpolation (Equally spaced)", color="orange")
        axes[0, 0].scatter(equal_nodes, equal_y_vals, color="orange", marker="o")
        axes[0, 0].set_title('Поліном Ньютона (рівновіддалені вузли)')
        axes[0, 0].legend()

        axes[0, 1].plot(mid_equal_nodes, error_newton_equal, label="Error Newton (Equally spaced)", color="orange")
        axes[0, 1].set_title('Похибка методу Ньютона (рівновіддалені вузли)')
        axes[0, 1].legend()

        # Поліноми Ньютона та похибка для вузлів Чебишева
        axes[1, 0].plot(x_vals, y_vals, label="Original Function", color="blue")
        axes[1, 0].plot(x_vals, newton_chebyshev_vals, label="Newton Interpolation (Chebyshev)", color="green")
        axes[1, 0].scatter(chebyshev_nodes, chebyshev_y_vals, color="green", marker="o")
        axes[1, 0].set_title('Поліном Ньютона (вузли Чебишева)')
        axes[1, 0].legend()

        axes[1, 1].plot(mid_chebyshev_nodes, error_newton_chebyshev, label="Error Newton (Chebyshev)", color="green")
        axes[1, 1].set_title('Похибка методу Ньютона (вузли Чебишева)')
        axes[1, 1].legend()

        # Поліноми Лагранжа та похибка для рівновіддалених вузлів
        axes[2, 0].plot(x_vals, y_vals, label="Original Function", color="blue")
        axes[2, 0].plot(x_vals, lagrange_equal_vals, label="Lagrange Interpolation (Equally spaced)", color="red")
        axes[2, 0].scatter(equal_nodes, equal_y_vals, color="red", marker="o")
        axes[2, 0].set_title('Поліном Лагранжа (рівновіддалені вузли)')
        axes[2, 0].legend()

        axes[2, 1].plot(mid_equal_nodes, error_lagrange_equal, label="Error Lagrange (Equally spaced)", color="red")
        axes[2, 1].set_title('Похибка методу Лагранжа (рівновіддалені вузли)')
        axes[2, 1].legend()

        # Поліноми Лагранжа та похибка для вузлів Чебишева
        axes[3, 0].plot(x_vals, y_vals, label="Original Function", color="blue")
        axes[3, 0].plot(x_vals, lagrange_chebyshev_vals, label="Lagrange Interpolation (Chebyshev)", color="purple")
        axes[3, 0].scatter(chebyshev_nodes, chebyshev_y_vals, color="purple", marker="o")
        axes[3, 0].set_title('Поліном Лагранжа (вузли Чебишева)')
        axes[3, 0].legend()

        axes[3, 1].plot(mid_chebyshev_nodes, error_lagrange_chebyshev, label="Error Lagrange (Chebyshev)", color="purple")
        axes[3, 1].set_title('Похибка методу Лагранжа (вузли Чебишева)')
        axes[3, 1].legend()

        plt.tight_layout()
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(pady=10)

    def newton_interpolation(self, x_nodes, y_nodes):
        n = len(x_nodes)
        divided_diff = np.zeros((n, n))
        divided_diff[:, 0] = y_nodes
        for j in range(1, n):
            for i in range(n - j):
                divided_diff[i, j] = (divided_diff[i + 1, j - 1] - divided_diff[i, j - 1]) / (x_nodes[i + j] - x_nodes[i])

        def newton_poly(x):
            result = divided_diff[0, 0]
            term = 1.0
            for j in range(1, n):
                term *= (x - x_nodes[j - 1])
                result += divided_diff[0, j] * term
            return result

        return np.vectorize(newton_poly)


def open_method4_page():
    method4_window = CTk.CTkToplevel()
    method4_window.title("Інтерполяція")
    method4_window.geometry("1100x900")
    InterpolationApp(method4_window)


if __name__ == "__main__":
    root = CTk.CTk()
    root.title("Головне вікно")
    open_method_button = CTk.CTkButton(root, text="Відкрити інтерполяцію", command=open_method4_page)
    open_method_button.pack(pady=20)
    root.mainloop()
