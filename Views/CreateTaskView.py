from tkinter import *
from Controllers.TaskController import TaskController


class CreateTaskView(Toplevel):
    def __init__(self):
        super().__init__()

        self.title("Создать заявку")
        self.geometry("400x300")

        Label(self, text="Тема").pack()
        self.topic = Entry(self)
        self.topic.pack()

        Label(self, text="Описание").pack()
        self.desc = Entry(self)
        self.desc.pack()

        Button(self, text="Создать", command=self.create_task).pack(pady=10)

    def create_task(self):
        result = TaskController.create(
            topic=self.topic.get(),
            description=self.desc.get(),
            user_id=1,
            category_id=1
        )

        print(result)