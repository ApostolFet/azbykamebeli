import asyncio
import json
import os

from data_base import Base, migrate_data_products_to_db

from parse import parse_categoria_products

from sqlalchemy import create_engine
from sqlalchemy.orm import Session


def main():
    categoria_url = "https://azbykamebeli.ru/catalog/0000057/"
    asyncio.run(parse_categoria_products(categoria_url))
    with open('product_data.json', 'r', encoding='utf-8') as file:
        data_products = json.load(file)

    user = os.getenv('pguser')
    password = os.getenv('pgpassword')
    data_base = os.getenv('postgres_db')

    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@localhost/{data_base}")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        migrate_data_products_to_db(session, data_products)


if __name__ == '__main__':
    main()
