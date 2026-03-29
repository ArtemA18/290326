from Models.Base import *
from Models.Category import Category
from Models.Comment import Comment
from Models.KnowledgeBase import KnowledgeBase
from Models.Task import Task
from Models.User import User

connect().create_tables(
    [
        User,
        Task,
        Category,
        KnowledgeBase,
        Comment
    ]
)