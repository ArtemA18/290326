from Models.Category import Category


class CategoryController:
    '''
    Класс для работы с категориями (справочник)
    Реализация CRUD операций
    '''

    @classmethod
    def get(cls, active_only=True):
        '''
        Получение списка категорий
        :param active_only: если True - возвращаем только активные категории (если будет поле is_active)
        :return: список категорий (объект запроса)
        '''
        # В текущей модели нет поля is_active, но можно добавить позже
        return Category.select()

    @classmethod
    def get_by_id(cls, id):
        '''
        Получение категории по ID
        :param id: ID категории
        :return: объект категории или None
        '''
        return Category.get_or_none(Category.id == id)

    @classmethod
    def create(cls, name):
        '''
        Создание новой категории
        :param name: название категории
        :return: сообщение об успехе или ошибке
        '''
        try:
            # Проверка на дубликат
            if Category.get_or_none(Category.name == name):
                return 'Категория уже существует'

            Category.create(name=name)
            return f'Категория "{name}" создана'

        except Exception as e:
            return f'Ошибка создания: {str(e)}'

    @classmethod
    def update(cls, id, **kwargs):
        '''
        Обновление категории
        :param id: ID категории
        :param kwargs: поля для обновления (например: name="Новое название")
        :return: сообщение об успехе или ошибке
        '''
        try:
            category = Category.get_or_none(Category.id == id)

            if not category:
                return 'Категория не найдена'

            Category.update(**kwargs).where(Category.id == id).execute()

            return f'Категория {id} обновлена'

        except Exception as e:
            return f'Ошибка обновления: {str(e)}'

    @classmethod
    def delete(cls, id):
        '''
        Удаление категории
        :param id: ID категории
        :return: сообщение об успехе или ошибке
        '''
        try:
            category = Category.get_or_none(Category.id == id)

            if not category:
                return 'Категория не найдена'

            category.delete_instance()
            return f'Категория {id} удалена'

        except Exception as e:
            return f'Ошибка удаления: {str(e)}'


if __name__ == "__main__":

    print("\n1. Создание категории:")
    print(CategoryController.create("ПО и программы"))

    print("\n2. Повторное создание (должно не дать):")
    print(CategoryController.create("ПО и программы"))

    print("\n3. Получение всех категорий:")
    for c in CategoryController.get():
        print(f"{c.id}: {c.name}")

    print("\n4. Получение по ID:")
    cat = CategoryController.get_by_id(1)
    if cat:
        print(cat.name)

    print("\n5. Обновление:")
    print(CategoryController.update(1, name="Обновленная категория"))

    print("\n6. Удаление:")
    print(CategoryController.delete(1))