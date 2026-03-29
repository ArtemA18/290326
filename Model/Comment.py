from Models.Base import *
from peewee import *
from datetime import datetime
from Models.Task import Task
from Models.User import User


class Comment(Base):
    id = AutoField()

    task_id = ForeignKeyField(Task)
    user_id = ForeignKeyField(User)

    text = TextField()
    is_private = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.now)