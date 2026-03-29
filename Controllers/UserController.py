from Models.User import User
from bcrypt import hashpw, gensalt, checkpw
# import hashlib # встроенная библиотека хеширования
class UserController:
    '''
    Класс для работы с пользователями

    '''
    @classmethod
    def get(cls):
        '''
        Вывод списка пользователей из таблицы User
        :return:
            список пользователей (объект)
        '''
        return User.select()
    @classmethod
    def registration(cls, login, password,role = 'Пользователь'):
        '''
        Регистрация пользователя
        :param login:  логин пользователя не более 10 символов, должен быть уникален
        :param password: пароль в будущем должен быть в виде HASH пароль
        :param role: роль в системе, если не указана, то: "Пользователь"
        :return:
            если ошибка - возвращаем текст ошибки
            иначе - возвращаем сообщение о созданном пользователе
        '''
        try:
            # Проверка длины логина
            if len(login) > 12:
                return 'Логин не должен превышать 12 символов'

            # Проверка существования логина
            if User.get_or_none(User.login == login):
                return 'Пользователь с таким логином уже существует'

            # Хеширование пароля с помощью bcrypt
            hash_password = hashpw(password.encode('utf-8'), gensalt())  # введённый прароль
            print(hash_password)
            User.create(
                login = login,
                password = hash_password.decode('utf-8'), # сохраняем как строку
                role = role
            )
            return f'Пользователь {login} с ролью {role} добавлен'
        except Exception as e:
            return f'Ошибка добавления пользователя: {str(e)}'


    @classmethod
    def update(cls, id, **kwargs):
        '''

        :param id: по id пользователя будет происходить изменение занчений записи в таблицы
        :param kwargs: вводится название поля и его новое занчение (например: login = "новый_логин")
                за один вызов метода можно изменить несколько полей одной записи
        :return:
            возвращаем сообщение об изменениях пользователе
            если ошибка - возвращаем текст ошибки

        '''
        try:
            for key, value in kwargs.items():# key - название столбца/поля, value - новое значение,  kwargs.items() - аргументы в виде списка словарей
                User.update({key:value}).where(User.id == id).execute()
            return f'У Пользователя изменен {kwargs} на {kwargs[key]} '
        except:
            return 'Ошибка измениния пользователя'
    @classmethod
    def update_status(cls,id):
        '''
        меняет у порльзователя статус с True на False или с False на True
        :param id: id пользователя
        :return:
            новый статус пользователя

        '''
        status = User.get_by_id(id).is_active # получаем по id пользователя его значения поля is_active (True/False)
        User.update({User.is_active:not status}).where(User.id==id).execute()
        return f'Статус пользователя стал {not status}'

    @classmethod
    def auth(cls,login,password):
        '''

        :param login:
        :param password:
        :return:
        '''

        user = User.get_or_none(User.login==login)
        if user:
            # Сравниваем введённый пароль с хешем из БД
            hash_password = user.password
            if checkpw(password.encode('utf-8'),hash_password.encode('utf-8')):
                return {
                "success": True,
                "message": "Авторизация успешна",
                "user": {
                    "id": user.id,
                    "login": user.login,
                    "role": user.role,
                    "fullname": user.fullname,
                    "is_active": user.is_active
                }
            }
            return {"success": False, "message": "Неверный логин или пароль"}
        return 'Неверный логин или пароль'

    @classmethod
    def test_hash(cls, password):
        print(f"Исходный пароль (str): {password}")
        pwd_bytes = password.encode('utf-8')
        print(f"После encode (bytes): {pwd_bytes}")

        hashed_bytes = hashpw(pwd_bytes, gensalt())
        print(f"Хеш (bytes): {hashed_bytes}")

        hashed_str = hashed_bytes.decode('utf-8')
        print(f"Хеш (str, для БД): {hashed_str}")

        # Проверка
        is_valid = checkpw(pwd_bytes, hashed_str.encode('utf-8'))
        print(f"Пароль верный? {is_valid}")







if __name__ == "__main__":
    # print(UserController.registration(login='user2', password='user'))
    # print(UserController.auth('user2','user'))

    # print(UserController.update(8,login = "admin", role = "Администратор"))

    # print(UserController.update_status(9))

    # UserController.test_hash('1234')

    for row in UserController.get():
        print(row.id, row.login, row.password, row.role, row.is_active, row.fullname)