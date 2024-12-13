import customtkinter as ctk
from GaussianMethod import GMethod
def approximation(current, prev, epsilon):
    return all(abs(current[i] - prev[i]) < epsilon for i in range(len(current)))
def make_diagonally_dominant(matrix, vector):
    n = len(matrix)

    for i in range(n):
        # Перевіряємо, чи діагональний елемент більше суми інших
        diag_element = abs(matrix[i][i])
        row_sum = sum(abs(matrix[i][j]) for j in range(n) if j != i)
        
        if diag_element < row_sum:
            # Шукаємо рядок для перестановки
            for j in range(i + 1, n):
                new_diag_element = abs(matrix[j][i])
                new_row_sum = sum(abs(matrix[j][k]) for k in range(n) if k != i)
                
                if new_diag_element > new_row_sum:
                    # Переставляємо рядки
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    vector[i], vector[j] = vector[j], vector[i]
                    break
            else:
                return False  # Якщо не вдалося знайти підходящий рядок
                
    return True  # Успішно зведено до діагонально домінантної форми

# Використовуємо функцію в основному методі
def FixedPointIter(matrix, vector, max_iter=15000, epsilon=1e-6, round_digits=4):
    # Спроба зробити матрицю діагонально домінантною
    if not is_diagonally_dominant(matrix):
        success = make_diagonally_dominant(matrix, vector)
        if not success:
            return "Не вдалося зробити матрицю діагонально домінантною. Метод може не збігатися."
    
    # Далі йде основний алгоритм
    prev = [1] * len(vector)  # Початкове наближення
    current = [0] * len(vector)
    
    iter = 0
    check = False
    converged = False

    while not check and iter < max_iter:
        for i in range(len(matrix)):
            to_store = vector[i]
            for j in range(len(matrix)):
                if j != i:
                    to_store -= matrix[i][j] * prev[j]
            current[i] = to_store / matrix[i][i]
        
        # Перевірка на збіжність
        check = approximation(current, prev, epsilon)
        
        # Додатковий захист: перевіряємо на занадто великі значення
        if any(abs(x) > 1e10 for x in current):
            return f"Результати надто великі. Останні обчислені корені: {current}"

        if check:
            converged = True
            break
        
        prev = current[::]  # Оновлюємо попередні значення
        iter += 1

    if converged:
        # Округлення кінцевих коренів
        rounded_roots = [round(x, round_digits) for x in prev]
        return f"Метод збіжний. Корені: {rounded_roots}, досягнуто за {iter + 1} ітерацій."
    else:
        # Округлення навіть у випадку незбіжності для більш читабельного результату
        rounded_roots = [round(x, round_digits) for x in prev]
        return f"Метод не збігся за {max_iter} ітерацій. Останні обчислені корені: {rounded_roots}"

def is_diagonally_dominant(matrix):
    for i in range(len(matrix)):
        if abs(matrix[i][i]) < sum(abs(matrix[i][j]) for j in range(len(matrix)) if j != i):
            return False
    return True



class FixedPointIterApp(ctk.CTkFrame):
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
def open_method2_page():
    # Створюємо нове вікно
    method2_window = ctk.CTkToplevel()
    method2_window.title("Метод Простих Ітерацій")
    method2_window.geometry("1000x1000")

    # Створюємо екземпляр класу FixedPointIterApp у новому вікні
    FixedPointIterApp(method2_window)

# Головне вікно програми
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Головне вікно")

    open_fixed_point_button = ctk.CTkButton(root, text="Відкрити метод Простих Ітерацій", command=open_method2_page)
    open_fixed_point_button.pack(pady=20)

    root.mainloop()
