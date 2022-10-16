import asyncio
import json
import os

from data_base import Base, migrate_data_products_to_db

from parse import parse_categoria_products

from sqlalchemy import create_engine
from sqlalchemy.orm import Session


def main():
    '''
    Launching the parsing of data about goods from the site
    and sending the received information to the database
    '''
    print('Скрипт запушен')
    categoria_url = 'https://azbykamebeli.ru/catalog/0000057/'

    print(f'Получение данных с сайта по адресу:{categoria_url}')
    asyncio.run(parse_categoria_products(categoria_url))

    with open('product_data.json', 'r', encoding='utf-8') as file:
        data_products = json.load(file)
    print(f'Парсинг завершен. Всего получено {len(data_products)} товаров')

    print('Получение переменных окружения для подключения к базе данных')
    user = os.getenv('pguser')
    password = os.getenv('pgpassword')
    data_base = os.getenv('postgres_db')

    print('Подключение к базе данных, инициализация таблиц')
    connect_url = f'postgresql+psycopg2://{user}:{password}@localhost/{data_base}'
    engine = create_engine(connect_url)
    Base.metadata.create_all(engine)

    print('Отправляем информацию о товарах в базу данных')
    with Session(engine) as session:
        migrate_data_products_to_db(session, data_products)

    print('Программа успешно завершилась')


if __name__ == '__main__':
    main()
