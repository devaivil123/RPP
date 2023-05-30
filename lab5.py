
import sqlite3
import random

# Создает таблицу пользователей базы данных
def create_users_table():
    #переменная, которая коннектится к базе данных, если такой базы нет, она ее создаст и законектится к ней
    conn = sqlite3.connect('users.db')
    #принимает в себя код sql
    c = conn.cursor()
    #записывает код sql
    c.execute('''create table users(
                 user_id integer primary key,
                 user_name text,
                 user_email text)''')
    conn.commit()
    conn.close()

# Функция добавления пользователя в таблицу в БД
def insert_user(user_name, user_email):

    # Создание соединения с базой данных
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Добавление нового пользователя
    c.execute("insert into users (user_name, user_email) values (?, ?)", (user_name, user_email))

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()

# Функция вывода всех пользователей в таблице
def get_all_users():

    # Создание соединения с базой данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Получение всех пользователей
    cursor.execute("select * from users")
    users = cursor.fetchall()

    # Закрытие соединения
    conn.close()

    return users

def get_user_by_id(user_id):

    # Создание соединения с базой данных
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Получения данных пользователя по user_id
    c.execute("select * from users where user_id = ?", (user_id,))
    user = c.fetchone()

    # Закрытие соединения
    conn.close()
    return user

def delete_user_by_id(user_id):

    # Создание соединения с базой данных
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Удаление пользвателя из БД
    c.execute("delete from users where user_id = ?", (user_id,))
    conn.commit()

    # Закрытие соединения
    conn.close()

# Функция удаления таблицы ---------- от себя
def drop_table_user():
    #Создание соединения с базой данных
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Удаление пользвателя из БД
    c.execute("drop table users")
    conn.commit()

    # Закрытие соединения
    conn.close()


# Функция main(), которая выполняет все функции последовательно
def main():

    # Создаем таблицу пользователей
    create_users_table()
    print("Таблица users создана!")

    # Добавляем пользователей в таблицу
    insert_user('Артур', 'artur.gips@mail.ru')
    insert_user('Саша',  'timoshenskiy.sasha02@mail.ru')
    insert_user('Женя',  'kartigo02@mail.ru')
    insert_user('Ваня',  'vanysha.vanya@mail.ru')

    # Получаем всех пользователей и выводим их в консоль
    # переменная юзерс которой присваевается функция
    users = get_all_users()
    print("Все пользователи: ")
    #цикл, который выводит все записи из таблицы
    for user in users:
        print(user)

    # Получаем пользователя по id и выводим его в консоль
    # user_id принимает в себя случайное число 1-4
    user_id = random.choice([1, 2, 3, 4])
   # user_id принимает в себя выбранное случайное число
    user = get_user_by_id(user_id)
    print(f"Выбран пользователь для удаления: {user_id}: {user}")


    # Удаляем случайного пользователя по id
    if user_id == random.choice([1, 2, 3, 4]):
        delete_user_by_id(user_id)

    # Получаем всех пользователей после удаления и выводим их в консоль
    users = get_all_users()
    print("Список пользователей после удаления: ")
    for user in users:
        print(user)

if __name__ == "__main__":
    main()
