from Models.Task import Task
from Models.User import User
from Models.Category import Category


class TaskController:
    '''
    Класс для работы с заявками (тикетами)

    '''

    @classmethod
    def get_all(cls, current_user=None):
        '''
        Получение всех заявок с учетом роли
        '''
        if current_user and current_user.role == 'Пользователь':
            return Task.select().where(Task.user_id == current_user.id)

        return Task.select()

    @classmethod
    def get_by_id(cls, id):
        '''
        Получение заявки по ID
        :param id: ID заявки
        :return: объект  заявки или None
        '''
        return Task.get_or_none(Task.id == id)

    @classmethod
    def get_by_user(cls, user_id):
        '''
        Получение заявок, созданных конкретным пользователем
        :param user_id: ID пользователя
        :return: список заявок пользователя
        '''
        return Task.select().where(Task.user_id == user_id)

    @classmethod
    def get_by_specialist(cls, specialist_id):
        '''
        Получение заявок, назначенных конкретному специалисту
        :param specialist_id: ID специалиста
        :return: список заявок специалиста
        '''
        return Task.select().where(Task.speciality_id == specialist_id)

    @classmethod
    def get_active(cls):
        '''
        Получение активных заявок (статус не "Выполнена")
        :return: список активных заявок
        '''
        return Task.select().where(Task.status != 'Закрыта')

    @classmethod
    def create(cls, topic, description, user_id, category_id, priority='Средний', status='Новая', file_path=None):
        '''
        Создание новой заявки (для пользователя)
        :param topic: тема заявки
        :param description: описание проблемы
        :param user_id: ID пользователя, создающего заявку
        :param category_id: ID категории
        :param priority: приоритет (Низкий, Средний, Высокий)
        :param status: статус (Новая, В работе, Выполнена)
        :param file_path: путь к прикрепленному файлу (опционально)
        :return: сообщение об успехе или ошибке
        '''
        try:
            # Проверяем существование пользователя и категории
            user = User.get_or_none(User.id == user_id)
            category = Category.get_or_none(Category.id == category_id)

            if not user:
                return 'Пользователь не найден'
            if not category:
                return 'Категория не найдена'

            Task.create(
                topic=topic,
                description=description,
                user_id=user_id,
                category_id=category_id,
                priority=priority,
                status=status,
                path=file_path or '',
                speciality_id=None
            )

            return f'Заявка "{topic}" успешно создана'

        except Exception as e:
            return f'Ошибка создания заявки: {str(e)}'

    @classmethod
    def update(cls, id, **kwargs):
        '''
        Обновление заявки
        :param id: ID заявки
        :param kwargs: поля для обновления
        :return: сообщение об успехе или ошибке
        '''
        try:
            task = Task.get_or_none(Task.id == id)
            if not task:
                return 'Заявка не найдена'

            Task.update(**kwargs).where(Task.id == id).execute()
            return f'Заявка с ID {id} обновлена'

        except Exception as e:
            return f'Ошибка обновления: {str(e)}'

    @classmethod
    def delete(cls, id):
        '''
        Удаление заявки
        :param id: ID заявки
        :return: сообщение об успехе или ошибке
        '''
        try:
            task = Task.get_or_none(Task.id == id)

            if not task:
                return 'Заявка не найдена'

            task.delete_instance()
            return f'Заявка {id} удалена'

        except Exception as e:
            return f'Ошибка удаления: {str(e)}'

    @classmethod
    def change_status(cls, id, new_status, user_id):
        '''
        Изменение статуса заявки (для специалиста)
        :param id: ID заявки
        :param new_status: новый статус (Новая, В работе, Выполнена, Ожидает ответа пользователя, Отклонена)
        :param user_id: ID пользователя изменяющего статус
        :return: сообщение об успехе или ошибке
        '''
        try:
            task = Task.get_or_none(Task.id == id)
            user = User.get_or_none(User.id == user_id)

            if not task:
                return 'Заявка не найдена'
            if not user:
                return 'Пользователь не найден'

            # RBAC
            if user.role not in ['Специалист', 'Администратор']:
                return 'Недостаточно прав'

            # Логика переходов
            transitions = {
                'Новая': ['В работе', 'Отклонена'],
                'В работе': ['Выполнена', 'Ожидает ответа пользователя'],
                'Ожидает ответа пользователя': ['В работе'],
                'Выполнена': ['Закрыта'],
                'Отклонена': [],
                'Закрыта': []
            }

            if new_status not in transitions.get(task.status, []):
                return f'Нельзя сменить статус с "{task.status}" на "{new_status}"'

            Task.update(status=new_status).where(Task.id == id).execute()

            return f'Статус изменен на "{new_status}"'

        except Exception as e:
            return f'Ошибка смены статуса: {str(e)}'

    @classmethod
    def assign_specialist(cls, id, specialist_id, admin_id):
        '''
        Назначение специалиста на заявку
        :param id: ID заявки
        :param specialist_id: ID специалиста
        :param admin_id: ID администратора
        :return: сообщение об успехе или ошибке
        '''
        try:
            task = Task.get_or_none(Task.id == id)
            specialist = User.get_or_none(User.id == specialist_id)
            admin = User.get_or_none(User.id == admin_id)

            if not task:
                return 'Заявка не найдена'
            if not specialist:
                return 'Специалист не найден'
            if admin.role != 'Администратор':
                return 'Только админ может назначать'

            Task.update(speciality_id=specialist_id).where(Task.id == id).execute()

            return f'Специалист назначен на заявку "{task.topic}"'

        except Exception as e:
            return f'Ошибка назначения: {str(e)}'

    @classmethod
    def take_to_work(cls, id, specialist_id):
        '''
        Взятие заявки в работу специалистом
        :param id: ID заявки
        :param specialist_id: ID специалиста
        :return: сообщение об успехе или ошибке
        '''
        try:
            task = Task.get_or_none(Task.id == id)
            specialist = User.get_or_none(User.id == specialist_id)

            if not task:
                return 'Заявка не найдена'
            if specialist.role != 'Специалист':
                return 'Недостаточно прав'

            Task.update(
                speciality_id=specialist_id,
                status='В работе'
            ).where(Task.id == id).execute()

            return f'Заявка "{task.topic}" взята в работу'

        except Exception as e:
            return f'Ошибка: {str(e)}'

    @classmethod
    def filter_tasks(cls, status=None, priority=None, category_id=None, user_id=None, specialist_id=None):
        '''
        Фильтрация заявок по различным параметрам (для ленты специалиста)
        :param status: статус заявки
        :param priority: приоритет
        :param category_id: ID категории
        :param user_id: ID пользователя
        :param specialist_id: ID специалиста
        :return: отфильтрованный список заявок
        '''
        query = Task.select()

        if status:
            query = query.where(Task.status == status)
        if priority:
            query = query.where(Task.priority == priority)
        if category_id:
            query = query.where(Task.category_id == category_id)
        if user_id:
            query = query.where(Task.user_id == user_id)
        if specialist_id:
            query = query.where(Task.speciality_id == specialist_id)

        return query

    @classmethod
    def get_statistics(cls):
        '''
        Получение статистики по заявкам
        :return: словарь со статистикой
        '''
        total = Task.select().count()
        new = Task.select().where(Task.status == 'Новая').count()
        in_progress = Task.select().where(Task.status == 'В работе').count()
        completed = Task.select().where(Task.status == 'Выполнена').count()
        closed = Task.select().where(Task.status == 'Закрыта').count()

        return {
            'total': total,
            'new': new,
            'in_progress': in_progress,
            'completed': completed,
            'closed': closed
        }


if __name__ == "__main__":

    USER_ID = 1
    SPECIALIST_ID = 2
    ADMIN_ID = 3
    CATEGORY_ID = 1

    print("\n1. Создание заявки:")
    result = TaskController.create(
        topic="Не работает интернет",
        description="Нет доступа к сети",
        user_id=USER_ID,
        category_id=CATEGORY_ID,
        priority="Высокий"
    )
    print(result)

    print("\n2. Получение всех заявок:")
    tasks = TaskController.get_all()
    for t in tasks:
        print(f"{t.id}: {t.topic} ({t.status})")

    print("\n3. Получение заявки по ID:")
    task = TaskController.get_by_id(1)
    print(task)

    print("\n4. Обновление заявки:")
    print(TaskController.update(1, topic="Обновленная тема"))

    print("\n5. Назначение специалиста (админ):")
    print(TaskController.assign_specialist(1, SPECIALIST_ID, ADMIN_ID))

    print("\n6. Взятие в работу:")
    print(TaskController.take_to_work(1, SPECIALIST_ID))

    print("\n7. Смена статуса:")
    print(TaskController.change_status(1, "Выполнена", SPECIALIST_ID))

    print("\n8. Фильтрация (В работе):")
    for t in TaskController.filter_tasks(status="В работе"):
        print(f"{t.id}: {t.topic}")

    print("\n9. Статистика:")
    stats = TaskController.get_statistics()
    print(stats)

    print("\n10. Удаление заявки:")
    print(TaskController.delete(1))