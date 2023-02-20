"""
- считать параметры подключения через dotenv
- подключиться к postgresql через psycopg2
- удалить тестовую таблицу, если есть; создать новую; заполнить сгенерированными данными; считать записанное

1. Доступ к postgresql в докере через psycopg2 [Отсюда, Youtube](https://youtu.be/I1h2YaWW9PE?t=1621)
2. Параметры подключения и имя таблицы загружаются из enveroment или из внешнего конфигурационного файла .env
"""
import string
from pprint import pprint
from random import choice
import os
import psycopg2
from dotenv import load_dotenv


def generate_login(uid):
    name = choice(string.ascii_lowercase)
    surname = "".join(choice(string.ascii_lowercase) for _ in range(5))
    return f'{name}_{uid}_{surname}'


def generate_name():
    return "".join(choice(string.ascii_lowercase) for _ in range(5)).title()


if __name__ == '__main__':
    """
    Конфигурационные параметры можно установить двумя способами:
    1. Как переменные окружения через системный SET или в настройке конфигурации в Pycharm (приоритет над вторым)
    2. В файле ".env" в текущей директории по умолчанию в виде PG_PORT='5432'
    Либо не устанавливать вовсе, если присутствует значение по умолчанию 
    """
    load_dotenv()
    conn = psycopg2.connect(
        host=os.getenv('PG_HOST', 'localhost'),
        port=os.getenv('PG_PORT', '5432'),
        database=os.getenv('PG_DB'),
        user=os.getenv('PG_USER'),
        password=os.getenv('PG_PASSWORD'),
    )
    TABLE = os.getenv('PG_TABLE', 'table_from_python')
    cur = conn.cursor()
    cur.execute(f"""
    DROP TABLE IF EXISTS {TABLE};
    CREATE TABLE {TABLE} (
        uid int not null,
        login text not null,       
        person text not null
    );       
    """)

    for i in range(10):
        # TODO Оптимизировать на 1 INSERT Или не надо?
        cur.execute(f'INSERT INTO {TABLE} (uid, login, person) VALUES (%s, %s, %s);',
                    (i, generate_login(i), generate_name()))

    cur.execute(f'SELECT * FROM {TABLE};')
    sql_data = cur.fetchall()
    pprint(sql_data)

    conn.commit()
    cur.close()
    conn.close()
