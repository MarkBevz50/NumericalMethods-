import customtkinter as ctk
from sympy import symbols, Function,parse_expr, sympify
import matplotlib.pyplot as plt

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.widgets =[]
        self.x_values = []
        self.y_values = []

        self.title("Задача Коші")
        self.resizable(False, False)
        self.right_part = ctk.CTkLabel(self,text="Права частина: ")
        self.right_part_entry = ctk.CTkEntry(self)
        self.widgets.append((self.right_part,self.right_part_entry))

        self.start_condition_x = ctk.CTkLabel(self, text="Початкове значення х0: ")
        self.start_condition_x_entry = ctk.CTkEntry(self)
        self.widgets.append((self.start_condition_x, self.start_condition_x_entry))

        self.start_condition_y = ctk.CTkLabel(self, text="Початкове значення y0: ")
        self.start_condition_y_entry = ctk.CTkEntry(self)
        self.widgets.append((self.start_condition_y, self.start_condition_y_entry))

        self.accuracy = ctk.CTkLabel(self, text="Точність: ")
        self.accuracy_entry = ctk.CTkEntry(self)
        self.widgets.append((self.accuracy, self.accuracy_entry))

        self.a = ctk.CTkLabel(self, text="Межа: ")
        self.a_entry = ctk.CTkEntry(self)
        self.widgets.append((self.a, self.a_entry))

        self.accurate_func = ctk.CTkLabel(self, text="Точний розв'язок: ")
        self.accurate_func_entry = ctk.CTkEntry(self)
        self.widgets.append((self.accurate_func, self.accurate_func_entry))

        self.method_combobox = ctk.CTkComboBox(self, values=["Метод Ейлера", "Метод Рунге-Кутта"])
        self.method_combobox.set("Метод Ейлера")
        self.button = ctk.CTkButton(self, text="Накреслити", command=self.plot)

        self.function = None

        self.interface()

    def interface(self):
        r = 0
        for widget in self.widgets:
            widget[0].grid(row=r, column=0, padx=5,pady=5)
            widget[1].grid(row=r, column=1, padx=5, pady=5)
            r+=1

        self.method_combobox.grid(row=r,column=0,columnspan=2, padx=5, pady=5)
        r+=1
        self.button.grid(row=r,column=0,columnspan=2, padx=5, pady=5)

    def euler(self, x,y,b,h):
        self.x_values = []
        self.y_values = []

        self.x_values.append(x)
        self.y_values.append(y)

        step1 = 0.01
        step2 = 0.005
        # Iterating till the point at which we
        # need approximation
        while x < b:
            y = y + h * self.func(x, y)
            x = x + h
            self.x_values.append(x)
            self.y_values.append(y)

            step1 = step2
            step2/=2

    def rungeKutta(self, x, y, b, h):
        """
        Метод Рунге-Кутта 2-го порядку.
        """
        self.x_values = []
        self.y_values = []

        self.x_values.append(x)
        self.y_values.append(y)

        while x < b:
            # Обчислюємо коефіцієнти
            k1 = h * self.func(x, y)
            k2 = h * self.func(x + 0.5 * h, y + 0.5 * k1)

            # Оновлюємо y і x
            y = y + k2
            x = x + h

            # Зберігаємо значення
            self.x_values.append(x)
            self.y_values.append(y)

    def func(self,x_value,y_value):
        x = symbols("x")
        y = symbols("y")
        result = self.function.subs([(x, x_value), (y, y_value)])
        return result

    def accurate_value_y(self):
        function_str=self.accurate_func_entry.get()
        function = sympify(function_str)
        x = symbols("x")
        y_values = []
        for x_value in self.x_values:
            y =  function.subs(x,x_value)
            y_values.append(y)
        return y_values

    def plot(self):
        function_str=self.right_part_entry.get()
        self.function = sympify(function_str)

        x = float(self.start_condition_x_entry.get())
        y= float(self.start_condition_y_entry.get())
        h= float(self.accuracy_entry.get())
        b= float(self.a_entry.get())

        if self.method_combobox.get() == "Метод Рунге-Кутта":
            self.rungeKutta(x,y,b,h)
            plt.plot(self.x_values,self.y_values, label='Рунге-Кутти')

        elif self.method_combobox.get() == "Метод Ейлера":
            self.euler(x,y,b,h)
            plt.plot(self.x_values,self.y_values, label="Ейлера", color='red')

        y_values = self.accurate_value_y()
        plt.plot(self.x_values,y_values, label="Точний графік", color='purple')
        leg = plt.legend(loc='upper center')
        plt.show()

def open_method8_page():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    app = App()
    app.mainloop()
