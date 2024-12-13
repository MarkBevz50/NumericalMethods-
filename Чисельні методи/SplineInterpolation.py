import customtkinter as CTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

CTk.set_appearance_mode("dark")
CTk.set_default_color_theme("blue")

class SplineApp(CTk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Labels and Entries
        self.label1 = CTk.CTkLabel(master=self, text="Ліва межа інтерполяції a: ", font=("Times New Roman", 20))
        self.label1.grid(row=1, column=1, padx=9, pady=15)
        self.entry1 = CTk.CTkEntry(master=self, width=200)
        self.entry1.grid(row=1, column=2, padx=5, pady=15)

        self.label0 = CTk.CTkLabel(master=self, text="Права межа інтерполяції b: ", font=("Times New Roman", 20))
        self.label0.grid(row=1, column=3, padx=9, pady=15)
        self.entry0 = CTk.CTkEntry(master=self, width=200)
        self.entry0.grid(row=1, column=4, padx=5, pady=15)

        self.label2 = CTk.CTkLabel(master=self, text="Крок h: ", font=("Times New Roman", 20))
        self.label2.grid(row=2, column=1, padx=9, pady=15)
        self.entry2 = CTk.CTkEntry(master=self, width=200)
        self.entry2.grid(row=2, column=2, padx=5, pady=15)

        self.button1 = CTk.CTkButton(master=self, text=" Лінійний ", font=("Times New Roman", 20), command=self.linear_spline)
        self.button1.grid(row=2, column=3, pady=15)

        self.button2 = CTk.CTkButton(master=self, text=" Кубічний ", font=("Times New Roman", 20), command=self.cubic_spline)
        self.button2.grid(row=2, column=4, pady=15)

        self.frame1 = CTk.CTkFrame(master=self, width=500, height=400)
        self.frame1.grid(row=5, columnspan=3, padx=20, pady=15)

        self.frame2 = CTk.CTkFrame(master=self, width=500, height=400)
        self.frame2.grid(row=5, column=3, columnspan=3, padx=20, pady=15)

    def linear_spline(self):
        a = float(self.entry1.get())
        b = float(self.entry0.get())
        h = float(self.entry2.get())

        # Очищення фрейму перед малюванням
        self.clear_frame(self.frame1)
        self.linear_spline_interpolate(a, b, h)

    def cubic_spline(self):
        a = float(self.entry1.get())
        b = float(self.entry0.get())
        h = float(self.entry2.get())

        # Очищення фрейму перед малюванням
        self.clear_frame(self.frame2)
        self.cubic_spline_interpolate(a, b, h)

    def clear_frame(self, frame):
        """ Очищає всі елементи вказаного фрейму. """
        for widget in frame.winfo_children():
            widget.destroy()

    def linear_spline_interpolate(self, a, b, h): 
        number_of_starts = int((b - a) / h) + 2 

        fig, ax = plt.subplots(figsize=(8, 8)) 
        ax.set_title('Графік лінійного бета-сплайна') 
        
        for i in range(number_of_starts): 
            start = a + h * (i - 1) 
            x_values = np.linspace(start, start + 2 * h, 100) 
            x_values = [x for x in x_values if a <= x <= b] 

            y_values = [] 
            x_k = [start, start + h, start + 2 * h] 

            for x in x_values: 
                y_value = 0 
                if x_k[0] <= x < x_k[1]: 
                    y_value = 1 / h + (x - x_k[1]) / (h ** 2) 
                elif x_k[1] <= x <= x_k[2]: 
                    y_value = 1 / h - (x - x_k[1]) / (h ** 2) 

                y_values.append(y_value) 
             
            ax.plot(x_values, y_values, color='blue') 
        
        ax.plot([a, b], [0, 0], color='purple') 
        ax.scatter([a], [0], label=f"Ліва межа інтерполяції(a = {a})", color='brown') 
        ax.scatter([b], [0], label=f"Права межа інтерполяції(b = {b})", color='brown') 
        ax.legend(loc='upper right') 
        ax.grid() 

        self.display_canvas(fig, self.frame1)

    def cubic_spline_interpolate(self, a, b, h): 
        number_of_starts = int((b - a) / h) + 4 

        fig, ax = plt.subplots(figsize=(8, 8)) 
        ax.set_title('Графік кубічного бета-сплайна') 

        for i in range(number_of_starts): 
            start = a + h * (i - 3) 
            x_values = np.linspace(start, start + 4.0 * h, 1000) 
            x_values = [x for x in x_values if a <= x <= b] 
            y_values = [] 
            x_k = [start, start + h, start + 2 * h, start + 3 * h, start + 4 * h]  

            for x in x_values: 
                y_value = 0 
                if x_k[0] <= x <= x_k[1]: 
                    y_value = 1 / (6 * h ** 4) * ((x - (x_k[0])) ** 3) 
                elif x_k[1] <= x <= x_k[2]: 
                    y_value = (1 / (6 * h) + (1 / (2 * h ** 2)) * (x - x_k[1]) + 
                                (1 / (2 * h ** 3)) * (x - x_k[1]) ** 2 - (1 / (2 * h ** 4)) * (x - x_k[1]) ** 3) 
                elif x_k[2] <= x <= x_k[3]: 
                    y_value = (1 / (6 * h) + (1 / (2 * h ** 2)) * (x_k[3] - x) + 
                                (1 / (2 * h ** 3)) * (x_k[3] - x) ** 2 - (1 / (2 * h ** 4)) * (x_k[3] - x) ** 3) 
                elif x_k[3] <= x <= x_k[4]: 
                    y_value = (1 / (6 * h ** 4) * ((x_k[4] - x) ** 3)) 

                y_values.append(y_value) 

            ax.plot(x_values, y_values, color='green') 
        
        ax.plot([a, b], [0, 0], color='orange') 
        ax.scatter([a], [0], label=f"Ліва межа інтерполяції(a = {a})", color='brown') 
        ax.scatter([b], [0], label=f"Права межа інтерполяції(b = {b})", color='brown') 
        ax.legend(loc='upper right') 
        ax.grid() 

        self.display_canvas(fig, self.frame2)

    def display_canvas(self, fig, frame):
        """ Додає графік до фрейму Tkinter. """
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


def open_method5_page():
    method5_window = CTk.CTkToplevel()
    method5_window.title("Сплайни")
    method5_window.geometry("1100x600")
    SplineApp(method5_window)


if __name__ == "__main__":
    root = CTk.CTk()
    root.title("Головне вікно")
    open_method5_button = CTk.CTkButton(root, text="Відкрити Сплайни", command=open_method5_page)
    open_method5_button.pack(pady=20)
    root.mainloop()
