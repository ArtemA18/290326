from Models.KnowledgeBase import KnowledgeBase
import hashlib


class KnowledgeBaseController:
    '''
    Контроллер базы знаний
    '''

    @classmethod
    def get(cls):
        return KnowledgeBase.select()

    @classmethod
    def add(cls, text_query, response):
        '''
        Добавление записи в базу знаний
        '''

        try:
            hash_query = hashlib.sha256(text_query.encode('utf-8')).hexdigest()

            existing = KnowledgeBase.get_or_none(KnowledgeBase.query == hash_query)

            if existing:
                return 'Такая запись уже существует'

            KnowledgeBase.create(
                query=hash_query,
                response=response,
                text_query=text_query
            )

            return 'Запись добавлена'

        except Exception as e:
            return f'Ошибка: {str(e)}'

    @classmethod
    def get_answer(cls, text_query):
        '''
        Получение ответа по запросу пользователя
        '''

        hash_query = hashlib.sha256(text_query.encode('utf-8')).hexdigest()

        result = KnowledgeBase.get_or_none(KnowledgeBase.query == hash_query)

        if result:
            return result.response
        else:
            return 'Ответ не найден в базе знаний'

    @classmethod
    def delete(cls, id):
        try:
            record = KnowledgeBase.get_or_none(KnowledgeBase.id == id)

            if not record:
                return 'Запись не найдена'

            record.delete_instance()
            return 'Запись удалена'

        except Exception as e:
            return f'Ошибка удаления: {str(e)}'

    @classmethod
    def show_hash(cls, text):
        hash_query = hashlib.sha256(text.encode('utf-8')).hexdigest()
        return hash_query

if __name__ == "__main__":

    print("\n1. Добавление записи:")
    print(KnowledgeBaseController.add(
        text_query='Что такое файл',
        response='Это именованная область диска'
    ))

    print("\n2. Повторное добавление:")
    print(KnowledgeBaseController.add(
        text_query='Что такое файл',
        response='Другой ответ'
    ))

    print("\n3. Получение ответа:")
    print(KnowledgeBaseController.get_answer('Что такое файл'))

    print("\n4. Получение несуществующего:")
    print(KnowledgeBaseController.get_answer('Что такое космос'))

    print("\n5. Список всех записей:")
    for row in KnowledgeBaseController.get():
        print(row.id, row.text_query, row.response)

    print("\n6. Удаление:")
    print(KnowledgeBaseController.delete(1))