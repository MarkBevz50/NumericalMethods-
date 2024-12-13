import customtkinter as ctk
from GaussianMethod import open_method1_page  # Імпортуємо функцію з файла чисельного методу
from FixedPointIterMethod import open_method2_page
from NewthonMethod import open_method3_page
from InterpolationNewthonLagrange import open_method4_page
from SplineInterpolation import open_method5_page
from RootMeanSquare import open_method6_page 
from quadratureFormulas import open_method7_page
from CauchyProblem import open_method8_page
from BoundaryProblem import open_method9_page
from DrawError import open_drawerror

class NumericalMethodsApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Чисельні методи")
        self.geometry("600x700")
        self.menu()  # Викликаємо головне меню під час запуску
        
    # Функція для головного меню
    def menu(self):
        frame = ctk.CTkFrame(self)
        frame.pack(pady=50, padx=50, fill="x")
        
        # Створюємо випадайки для кожної лабораторної
        methods = {
            "Лабораторна 1": ["Метод Гауса", "Метод простих ітерацій"],
            "Лабораторна 2": ["Метод Ньютона та простих ітерацій"],
            "Лабораторна 3": ["Інтерполяція поліномами Лагранжа та Ньютона"],
            "Лабораторна 4": ["Сплайн-інтерполяція"],
            "Лабораторна 5": ["Найкраще середньоквадратичне наближення"],
            "Лабораторна 6": ["Квадратурні формули"],
            "Лабораторна 7": ["Задача Коші"],
            "Лабораторна 8": ["Крайова задача"]
        }

        # Створюємо функцію для навігації до вибраного методу
        def navigate_to_method(method_name):
            if method_name == "Метод Гауса":
                open_method1_page()
            if method_name == "Метод простих ітерацій":
                open_method2_page()
            if method_name == "Метод Ньютона та простих ітерацій":
                open_method3_page()
            if method_name == "Інтерполяція поліномами Лагранжа та Ньютона":
                open_method4_page()
            if method_name == "Сплайн-інтерполяція":
                open_method5_page()
            if method_name == "Найкраще середньоквадратичне наближення":
                open_method6_page()
            if method_name == "Квадратурні формули":
                open_method7_page()
            if method_name == "Задача Коші":
                open_method8_page()
            if method_name == "Крайова задача":
                open_method9_page()
                open_drawerror()
            else:
                print(f"Method '{method_name}' не реалізований")

        # Створюємо випадайку та кнопку для кожної лабораторної
        for lab, methods_list in methods.items():
            lab_frame = ctk.CTkFrame(frame)
            lab_frame.pack(pady=10, fill="x")

            lab_label = ctk.CTkLabel(lab_frame, text=lab)
            lab_label.grid(row=0, column=0, padx=5, pady=5)

            method_combobox = ctk.CTkComboBox(lab_frame, values=methods_list)
            method_combobox.grid(row=0, column=1, padx=5, pady=5)
            method_combobox.set("Оберіть метод")

            # Кнопка для переходу з кольором і округленими краями
            continue_button = ctk.CTkButton(lab_frame, text="Перейти", 
                                            command=lambda m=method_combobox: navigate_to_method(m.get()),
                                            corner_radius=20,  # Округлені краї
                                            fg_color="green",  # Основний колір кнопки
                                            hover_color="darkgreen")  # Колір при наведенні
            continue_button.grid(row=0, column=2, padx=5, pady=5)
    
    # Функція для очищення кадру (як приклад, під час переходу між сторінками)
    def _clear(self, *widgets):
        for widget in widgets:
            widget.destroy()


# Створюємо та запускаємо застосунок
app = NumericalMethodsApp()
app.mainloop()
