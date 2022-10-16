import json
import os

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'

    offer_id = Column(Integer, primary_key=True)
    name = Column('name', String(90), nullable=False)
    artnumber = Column('artnumber', String(30), nullable=False)
    online_price = Column('online_price', String(30), nullable=False)
    store_price = Column('store_price', String(30), nullable=True)
    stock = Column('stock', String(30))

    def __repr__(self):
        return f'Product({self.offer_id=!r}, {self.artnumber=!r}, {self.name=!r}'


def migrate_data_products_to_db(session: Session, data_products: list):
    '''Add data about products to data_base in table products

    Args:
        session (Session): session to communicate with the database
        data_product (str): data about product
    '''
    products: list[Product] = []
    for product in data_products:
        product_already_exists = (
            session.query(Product).filter(Product.offer_id == product['offer_id']).first()
        )

        if product_already_exists:
            continue

        products.append(
            Product(
                offer_id=int(product['offer_id']),
                name=product['name'],
                artnumber=product['artnumber'],
                online_price=product['online_price'],
                store_price=product['store_price'],
                stock=product['stock'],
            ),
        )
    session.add_all(products)
    session.commit()


if __name__ == '__main__':
    print('Извлечение данных о товарах')
    with open('product_data.json', 'r', encoding='utf-8') as file:
        data_products = json.load(file)

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
