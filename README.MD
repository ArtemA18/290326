# Информационная система «Техническая поддержка» (HelpDesk)

## 1. Описание проекта
Система предназначена для автоматизации работы службы технической поддержки.

Функционал:
- регистрация и авторизация пользователей
- создание заявок
- назначение специалистов
- изменение статусов заявок
- добавление комментариев
- фильтрация и поиск заявок

------

## 2. Технологии
- Python
- Peewee
- MySQL
- PyMySQL
- bcrypt

------

## 3. Структура проекта
```
HelpDesk/
|-- Connection/
|   |--connect.py               # Подключение к Базе данных MySQL
|--Controllers/
|   |--UserController.py        # Контроллер для работы с пользователем
|   |--CategoryController.py    # Контроллер для работы с категориями
|   |--TaskController.py        # Контроллер для работы с комментариями
|   |--CommentController.py     # Контроллер для работы с заявками
|--Models/
|   |--Base.py                  # Базовый родительский класс для всех моделей
|   |--User.py                  # Класс пользователей
|   |--Task.py                  # Класс заявок
|   |--Category.py              # Класс категорий заявок
|   |--Comment.py               # Класс комментариев
...
```
---

## 4. База данных

### User
- id
- login (уникальный)
- password (hash)
- role:
  - Пользователь
  - Специалист
  - Администратор
- is_active
- fullname

---

### Task
- id
- topic
- description
- path (файл)
- priority:
  - Низкий
  - Средний
  - Высокий
- status:
  - Новая
  - В работе
  - Выполнена
- user_id
- speciality_id
- category_id

---

### Category
- id
- name

---

### Comment
- id
- task_id
- user_id
- text
- is_private
- created_at

---

## 5. Основной функционал

### Пользователи
- регистрация
- авторизация
- роли (RBAC)

---

### Заявки
- создание, редактирование, удаление
- статусы:
`Новая → В работе → Выполнена → Закрыта`
- назначение специалиста
- фильтрация
- статистика

---

### Комментарии
- добавление
- редактирование
- удаление
- приватные комментарии

---

## 6. Примеры использования

### Пользователь
```python
from Controllers.UserController import UserController

UserController.registration(login='user', password='1234')

print(UserController.auth('user', '1234'))
```

### Заявка
```python
from Controllers.TaskController import TaskController

TaskController.create(
    topic="Не работает ",
    description="Нет доступа",
    user_id=1,
    category_id=1
)
```

### Комментарий
```python
from Controllers.CommentController import CommentController

CommentController.add_comment(
    task_id=1,
    user_id=1,
    text="Проблема сохраняется"
)
```

---

## 7. Установка
### 1. Установка зависимости:
```bash
pip install -r requirements.txt
```

### 2. Настроить подключение к БД:
```
Connection/connect.py
```

### 3. Создать таблицы:
```bash
python Models/create_table.py
```

---

## 8. Тестирование
Каждый контроллер содержит блок:
```python
if __name__ == "__main__":
```
Позволяющий протестировать:
- создание данных
- обновление
- удаление 
- проверку прав доступа

---

## 9. Особенности реализации
- Пароли хранятся в виде хеша (bcrypt)
- Используется ролевая модель доступа (RBAC)
- Реализован жизненный цикл заявок
- Поддерживаются приватные комментарии

---

## Статус проекта

Проект реализован в рамках учебной практики.

Основной функционал backend-части полностью готов.

---

## Лицензия

Учебный проект