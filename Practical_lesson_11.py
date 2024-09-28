import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Юдкин Михаил Дмитриевич Ум-242")
        self.geometry("400x300")

        self.tab_control = ttk.Notebook(self)

        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab3 = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab1, text='Калькулятор')
        self.tab_control.add(self.tab2, text='Чекбоксы')
        self.tab_control.add(self.tab3, text='Текст')

        self.tab_control.pack(expand=1, fill='both')

        self.create_calculator_tab()
        self.create_checkboxes_tab()
        self.create_text_tab()

    def create_calculator_tab(self):
        self.num1_entry = tk.Entry(self.tab1)
        self.num1_entry.pack(pady=5)

        self.operation = ttk.Combobox(self.tab1, values=["+", "-", "*", "/"])
        self.operation.pack(pady=5)

        self.num2_entry = tk.Entry(self.tab1)
        self.num2_entry.pack(pady=5)

        self.calc_button = tk.Button(self.tab1, text="Рассчитать", command=self.calculate)
        self.calc_button.pack(pady=5)

        self.result_label = tk.Label(self.tab1, text="")
        self.result_label.pack(pady=5)

    def calculate(self):
        try:
            num1 = float(self.num1_entry.get())
            num2 = float(self.num2_entry.get())
            operation = self.operation.get()

            if operation == "+":
                result = num1 + num2
            elif operation == "-":
                result = num1 - num2
            elif operation == "*":
                result = num1 * num2
            elif operation == "/":
                result = num1 / num2
            else:
                raise ValueError("Неверная операция")

            self.result_label.config(text=f"Результат: {result}")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def create_checkboxes_tab(self):
        self.var1 = tk.IntVar()
        self.var2 = tk.IntVar()
        self.var3 = tk.IntVar()

        self.check1 = tk.Checkbutton(self.tab2, text="Первый", variable=self.var1)
        self.check2 = tk.Checkbutton(self.tab2, text="Второй", variable=self.var2)
        self.check3 = tk.Checkbutton(self.tab2, text="Третий", variable=self.var3)

        self.check1.pack(pady=5)
        self.check2.pack(pady=5)
        self.check3.pack(pady=5)

        self.check_button = tk.Button(self.tab2, text="Проверить", command=self.check_selection)
        self.check_button.pack(pady=5)

    def check_selection(self):
        selections = []
        if self.var1.get():
            selections.append("первый")
        if self.var2.get():
            selections.append("второй")
        if self.var3.get():
            selections.append("третий")

        messagebox.showinfo("Результат", f'''Вы выбрали {', '.join(selections) + f' вариант{"ы" if len(selections) > 1 else ""}' if selections else 'Ничего не выбрано'}''')

    def create_text_tab(self):
        self.text_area = tk.Text(self.tab3)
        self.text_area.pack(expand=1, fill='both')

        self.menu_bar = tk.Menu(self)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label='Загрузить...', command=self.load_file)  # исправление тут
        self.menu_bar.add_cascade(label='Файл', menu=self.file_menu)
        self.config(menu=self.menu_bar)

    def load_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r', encoding="utf-8") as file:
                content = file.read()
                self.text_area.delete('1.0', tk.END)
                self.text_area.insert(tk.END, content)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
