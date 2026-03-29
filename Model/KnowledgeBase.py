from Models.Base import *

class KnowledgeBase(Base):
    id = PrimaryKeyField()
    query = CharField(max_length=255) #  в виде хэша
    response = TextField() # ответ для вопроса
    text_query = CharField() # текст вопроса для теста