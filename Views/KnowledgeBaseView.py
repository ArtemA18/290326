
from tkinter import *
from tkinter import ttk
from Controllers.KnowledgeBaseController import KnowledgeBaseController


class KnowledgeBaseView(Toplevel):
    def __init__(self):
        super().__init__()

        self.title('База знаний')
        self.geometry('600x400')

        # Поле ввода
        self.entry = Entry(self, width=50)
        self.entry.pack(pady=10)

        Button(self, text="Найти", command=self.search).pack()

        # Результат
        self.result = Label(self, text="")
        self.result.pack(pady=10)

        # Список
        self.tree = ttk.Treeview(self, columns=("ID", "Запрос", "Ответ"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Запрос", text="Запрос")
        self.tree.heading("Ответ", text="Ответ")
        self.tree.pack(fill=BOTH, expand=True)

        Button(self, text="Обновить", command=self.load_data).pack(pady=5)

        self.load_data()

    def search(self):
        text = self.entry.get()
        result = KnowledgeBaseController.get_answer(text)
        self.result.config(text=result)

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for kb in KnowledgeBaseController.get():
            self.tree.insert("", END, values=(kb.id, kb.text_query, kb.response))
