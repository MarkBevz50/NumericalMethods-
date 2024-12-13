import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox

def read_error_data(filename):
    """
    Функція для зчитування даних похибки з файлу.
    """
    try:
        with open(filename, "r") as file:
            lines = file.readlines()

        # Зчитуємо x-значення (перший рядок) та похибки (другий рядок)
        x_values = list(map(float, lines[0].split()))
        errors = list(map(float, lines[1].split()))
        return x_values, errors
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося зчитати файл: {e}")
        return None, None

def plot_error(x_values, errors):
    """
    Функція для побудови графіка похибки.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, errors, label="Похибка", linestyle="-", color="green", marker="o")
    plt.xlabel("x")
    plt.ylabel("Похибка")
    plt.title("Графік похибки")
    plt.legend()
    plt.grid()
    plt.show()

def browse_file():
    """
    Вибір файлу через діалогове вікно.
    """
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if filename:
        file_entry.delete(0, "end")
        file_entry.insert(0, filename)

def on_plot_click():
    """
    Обробник події натискання кнопки "Намалювати".
    """
    filename = file_entry.get()
    try:
        n_points = int(points_entry.get())
    except ValueError:
        messagebox.showerror("Помилка", "Кількість точок має бути цілим числом!")
        return

    if not filename:
        messagebox.showerror("Помилка", "Будь ласка, виберіть файл!")
        return

    # Зчитуємо дані
    x_values, errors = read_error_data(filename)
    if x_values is None or errors is None:
        return

    # Перевіряємо кількість точок
    if n_points > len(x_values) or n_points > len(errors):
        messagebox.showerror("Помилка", "Кількість точок перевищує кількість даних у файлі!")
        return

    # Обрізаємо дані до заданої кількості точок
    x_values = x_values[:n_points]
    errors = errors[:n_points]

    # Малюємо графік
    plot_error(x_values, errors)

# Створення графічного інтерфейсу
root = Tk()
root.title("Графік похибки")

# Поле для введення файлу
Label(root, text="Назва файлу:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
file_entry = Entry(root, width=40)
file_entry.grid(row=0, column=1, padx=10, pady=5)
Button(root, text="Огляд...", command=browse_file).grid(row=0, column=2, padx=10, pady=5)

# Поле для введення кількості точок
Label(root, text="Кількість точок:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
points_entry = Entry(root, width=10)
points_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

# Кнопка для побудови графіка
Button(root, text="Намалювати", command=on_plot_click).grid(row=2, column=1, pady=20)

# Запуск інтерфейсу
 
def open_drawerror():
    root.mainloop()