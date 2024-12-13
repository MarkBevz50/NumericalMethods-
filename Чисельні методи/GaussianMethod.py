import customtkinter as ctk

def GMethod(matrix, vect, precision=10):
    def custom_round(value):
        rounded_value = round(value, precision)
        if abs(rounded_value - value) < 1e-9:  # Поріг для заокруглення до цілого
            return rounded_value
        return value

    result = []
    for i in range(len(vect)):
        result.append(0.0)

    # Прямий хід методу Гауса
    for i in range(len(matrix)):
        coef = matrix[i][i]
        for j in range(i, len(matrix)):
            matrix[i][j] /= coef
            matrix[i][j] = custom_round(matrix[i][j])  # Заокруглення елементів матриці
        vect[i] /= coef
        vect[i] = custom_round(vect[i])  # Заокруглення вектора
        for k in range(i + 1, len(matrix)):
            ratio = matrix[k][i] / matrix[i][i]
            for l in range(i, len(matrix)):
                matrix[k][l] -= ratio * matrix[i][l]
                matrix[k][l] = custom_round(matrix[k][l])  # Заокруглення після віднімання
            vect[k] -= ratio * vect[i]
            vect[k] = custom_round(vect[k])  # Заокруглення вектора після віднімання

    # Зворотний хід методу Гауса
    for i in range(len(matrix) - 1, -1, -1):
        to_store = vect[i]
        for j in range(len(matrix) - 1, i, -1):
            to_store -= matrix[i][j] * result[j]
            to_store = custom_round(to_store)  # Заокруглення після віднімання
        result[i] = to_store / matrix[i][i]
        result[i] = custom_round(result[i])  # Заокруглення остаточного результату
    return result


class GaussApp(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.menu()

    @staticmethod
    def _clear(*args):
        for arg in args:
            arg.destroy()

    def menu(self):
        frame = ctk.CTkFrame(self)
        rows_label = ctk.CTkLabel(frame, text="Введіть кількість змінних: ")
        rows_entry = ctk.CTkEntry(frame)
        continue_button = ctk.CTkButton(frame, text="Продовжити", command=lambda: (self.solve(int(rows_entry.get())), self._clear(frame)))

        frame.pack(pady=10)
        rows_label.grid(row=0, column=0, padx=3, pady=3)
        rows_entry.grid(row=0, column=1, padx=3, pady=3)
        continue_button.grid(row=1, column=0, columnspan=2, padx=3, pady=3)

    def solve(self, n):
        def solution(matrix, vector):
            res = GMethod(matrix, vector)
            result.configure(text=f"Результат: {res}")

        frame = ctk.CTkFrame(self)
        frame.pack(pady=10)
        entries_matr = [[ctk.CTkEntry(frame, width=50) for _ in range(n)] for _ in range(n)]
        entries_vect = [ctk.CTkEntry(frame, width=50) for _ in range(n)]

        # Додаємо назви змінних (x1, x2, x3...) перед кожним стовпцем
        for j in range(n):
            ctk.CTkLabel(frame, text=f"x{j+1}").grid(row=0, column=2*j, padx=2, pady=2)

        # Виводимо матрицю та плюси між клітинками
        for i in range(n):
            for j in range(n):
                entries_matr[i][j].grid(row=i+1, column=2*j, padx=2, pady=2)  # +1 до рядка через лейбли
                if j < n-1:  # Додаємо плюс, якщо це не останній елемент
                    ctk.CTkLabel(frame, text="+").grid(row=i+1, column=2*j+1, padx=2, pady=2)
            ctk.CTkLabel(frame, text=" = ").grid(row=i+1, column=2*n, padx=2, pady=2)
            entries_vect[i].grid(row=i+1, column=2*n + 1, padx=2, pady=2)

        resolve_button = ctk.CTkButton(self, text="Розв'язати", command=lambda:
                        (solution([[float(entries_matr[i][j].get()) for j in range(n)] for i in range(n)],
                                  [float(entries_vect[i].get()) for i in range(n)])))
        resolve_button.pack(pady=10)

        back_button = ctk.CTkButton(self, text="Повернутись", command=lambda: (self._clear(frame, resolve_button, result, back_button), self.menu()))
        back_button.pack(pady=10)

        result = ctk.CTkLabel(self, text="")
        result.pack(padx=2, pady=2)

# Функція для відкриття вікна чисельного методу
def open_method1_page():
    # Створюємо нове вікно
    method1_window = ctk.CTkToplevel()
    method1_window.title("Метод Гауса")
    method1_window.geometry("1000x1000")

    # Створюємо екземпляр класу GaussApp у новому вікні
    GaussApp(method1_window)

# Головне вікно програми
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Головне вікно")

    open_gauss_button = ctk.CTkButton(root, text="Відкрити метод Гауса", command=open_method1_page)
    open_gauss_button.pack(pady=20)

    root.mainloop()
