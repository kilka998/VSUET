import json
import tkinter as tk
from tkinter import ttk, messagebox


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Юдкин Михаил Дмитриевич Ум-242. Задание 12.2")
        self.geometry("400x300")

        self.tab_control = ttk.Notebook(self)

        self.tab1 = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab1, text='Выгрузка из github информации')

        self.tab_control.pack(expand=1, fill='both')

        self.github_tab()

    def github_tab(self):
        self.path_to_github = tk.Entry(self.tab1)
        self.path_to_github.pack(pady=5)

        self.calc_button = tk.Button(self.tab1, text="Выгрузить данные из github", command=self.get_github_info)
        self.calc_button.pack(pady=5)

        self.result_label = tk.Label(self.tab1, text="", justify="left")
        self.result_label.pack(pady=5)

    def request_in_github(self, path: str = "", url: str = "") -> dict:
        import requests

        if not url:
            url = f'https://api.github.com/repos/{path}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError("Ошибка при запросе в github")

    def convert_user_data(self, user_info: dict, repo_name: str) -> str:
        data = {
            'company': user_info.get('company'),
            'created_at': user_info.get('created_at'),
            'email': user_info.get('email'),
            'id': user_info.get('id'),
            'name': user_info.get('login'),
            'url': user_info.get('url')
        }
        self.upload_to_file(data, repo_name)
        return '{\n' + ',\n'.join([f'"{key}": "{value}"' for key, value in data.items()]) + '\n}'

    def upload_to_file(self, data: dict, repo_name: str):
        file_name = f"{repo_name.replace('/', '_')}.json"

        with open(f'result_12_2/{file_name}.json', 'w') as file:
            json.dump(data, file, indent=4)

        messagebox.showinfo("Успех", f"Информация сохранена в файл {file_name}.json.")

    def get_github_info(self):
        try:
            repo_name = self.path_to_github.get()
            github_info = self.request_in_github(repo_name)
            user_url = github_info['owner']['url']
            user_info = self.request_in_github(url=user_url)
            result = self.convert_user_data(user_info, repo_name=repo_name)
            print(result)
            self.result_label.config(text=f"Результат: \n{result}")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


if __name__ == "__main__":
    app = Application()
    app.mainloop()
