from Models.Comment import Comment
from Models.Task import Task
from Models.User import User


class CommentController:

    @classmethod
    def get(cls):
        return Comment.select()

    @classmethod
    def add_comment(cls, task_id, user_id, text, is_private=False):
        try:
            task = Task.get_or_none(Task.id == task_id)
            user = User.get_or_none(User.id == user_id)

            if not task:
                return 'Заявка не найдена'
            if not user:
                return 'Пользователь не найден'

            if is_private and user.role == 'Пользователь':
                return 'Недостаточно прав'

            Comment.create(
                task_id=task_id,
                user_id=user_id,
                text=text,
                is_private=is_private
            )

            return 'Комментарий добавлен'

        except Exception as e:
            return f'Ошибка: {str(e)}'

    @classmethod
    def get_by_task(cls, task_id, current_user_id):
        user = User.get_or_none(User.id == current_user_id)
        if not user:
            return []

        query = Comment.select().where(Comment.task_id == task_id)

        if user.role == 'Пользователь':
            query = query.where(Comment.is_private == False)

        return query.order_by(Comment.created_at)

    @classmethod
    def delete(cls, comment_id, user_id):
        try:
            comment = Comment.get_or_none(Comment.id == comment_id)
            user = User.get_or_none(User.id == user_id)

            if not comment:
                return 'Комментарий не найден'
            if not user:
                return 'Пользователь не найден'

            if comment.user_id.id != user_id and user.role != 'Администратор':
                return 'Недостаточно прав'

            comment.delete_instance()
            return 'Комментарий удален'

        except Exception as e:
            return f'Ошибка: {str(e)}'

    @classmethod
    def update(cls, comment_id, user_id, new_text):
        try:
            comment = Comment.get_or_none(Comment.id == comment_id)
            user = User.get_or_none(User.id == user_id)

            if not comment:
                return 'Комментарий не найден'
            if not user:
                return 'Пользователь не найден'

            if comment.user_id.id != user_id and user.role != 'Администратор':
                return 'Недостаточно прав'

            Comment.update(text=new_text).where(Comment.id == comment_id).execute()

            return 'Комментарий обновлен'

        except Exception as e:
            return f'Ошибка: {str(e)}'

if __name__ == "__main__":

    TASK_ID = 1
    USER_ID = 1              # обычный пользователь
    SPECIALIST_ID = 2       # специалист
    ADMIN_ID = 3            # админ

    print("\n1. Добавление комментария (публичный):")
    print(CommentController.add_comment(
        TASK_ID,
        USER_ID,
        "У меня не работает программа"
    ))

    print("\n2. Добавление приватного (пользователь НЕ должен смочь):")
    print(CommentController.add_comment(
        TASK_ID,
        USER_ID,
        "Скрытый комментарий",
        True
    ))

    print("\n3. Приватный от специалиста (должен сработать):")
    print(CommentController.add_comment(
        TASK_ID,
        SPECIALIST_ID,
        "Нужно проверить сервер",
        True
    ))

    print("\n4. Получение комментариев (как пользователь — без приватных):")
    comments = CommentController.get_by_task(TASK_ID, USER_ID)
    for c in comments:
        print(f"{c.id}: {c.text} | private={c.is_private}")

    print("\n5. Получение комментариев (как специалист — все):")
    comments = CommentController.get_by_task(TASK_ID, SPECIALIST_ID)
    for c in comments:
        print(f"{c.id}: {c.text} | private={c.is_private}")

    print("\n6. Обновление комментария (своего):")
    print(CommentController.update(1, USER_ID, "Обновленный текст"))

    print("\n7. Удаление комментария (своего):")
    print(CommentController.delete(1, USER_ID))

    print("\n8. Попытка удалить чужой (должно запретить):")
    print(CommentController.delete(2, USER_ID))

    print("\n9. Удаление чужого админом:")
    print(CommentController.delete(2, ADMIN_ID))