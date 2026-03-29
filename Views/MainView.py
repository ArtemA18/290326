from tkinter import *
from Views.KnowledgeBaseView import KnowledgeBaseView
from Views.CreateTaskView import CreateTaskView


class MainView(Tk):
    def __init__(self):
        super().__init__()

        self.title("HelpDesk")
        self.geometry("400x300")

        Button(self, text="Создать заявку", command=self.open_task).pack(pady=10)
        Button(self, text="База знаний", command=self.open_kb).pack(pady=10)

    def open_task(self):
        CreateTaskView()

    def open_kb(self):
        KnowledgeBaseView()


if __name__ == "__main__":
    app = MainView()
    app.mainloop()