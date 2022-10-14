import asyncio
import json
import re

import aiohttp

from bs4 import BeautifulSoup


async def parse_categoria_products(url_categoria: str) -> None:
    """Parsing data about product from site azbykamebeli.ru
    and save data in json file 'product_data.json'

    Args:
        url_categoria (str): category catalog page URL
    """
    product_data = []
    async with aiohttp.ClientSession() as session:
        number_pages = await get_number_pages(url_categoria, session)
        for page in range(1, number_pages + 1):
            url_page = url_categoria + f"?{page=}"
            async with session.get(url_page) as resoponse:
                html_categoria = await resoponse.text()
                append_products_data(product_data, html_categoria)
                print(len(product_data))

    with open("product_data.json", "w", encoding="utf-8") as file:
        json.dump(product_data, file, indent=4, ensure_ascii=False)


async def get_number_pages(url_categoria: str, session: aiohttp.ClientSession) -> int:
    """Get the number of pages with products in a given category.

    Args:
        url_categoria (str): category catalog page URL
        session (aiohttp.ClientSession): session for get requests

    Returns:
        int: number pages
    """
    async with session.get(url_categoria) as resoponse:
        html_categoria = await resoponse.text()
        soup = BeautifulSoup(html_categoria, "lxml")
        pagination = soup.find("ul", class_="pagination").find_all("a", class_="page-link")
        number_pages = int(pagination[-2].text)
        return number_pages


def append_products_data(product_data: list, html_categoria: str) -> None:
    """Append product data from html_categoria in list product_data.

    Args:
        product_data (list): Append data in this list
        html_categoria (str): Get product data from this page of catalog
    """
    soup = BeautifulSoup(html_categoria, "lxml")
    products = soup.find_all(
        "div",
        class_="items-list__item d-flex align-items-end flex-column with-wrap",
    )

    for product in products:
        href = product.find("a").get("href")
        name = (product.find("span", itemprop="name").text,)
        artnumber = product.find("small", class_="text-muted f-XS").text
        online_price = product.find("div", class_="online-price").text

        store_price = product.find("a", class_="store-price fake-link")
        if store_price:
            store_price = store_price.text

        stock = product.find(
            "small",
            class_=re.compile("f-XS d-inline-block badge badge-pill"),
        ).text

        offer_id = get_offer_id(href)

        product_data.append(
            {
                "href": href,
                "name": name[0],
                "artnumber": artnumber,
                "online_price": online_price,
                "store_price": store_price,
                "stock": stock,
                "offer_id": offer_id,
            }
        )


def get_offer_id(href_product: str) -> str:
    """Get offer id from product`s href

    Args:
        href_product (str): hypertext reference on product

    Returns:
        str: product offer id
    """

    return href_product.split("offerId=")[-1]


if __name__ == "__main__":
    categoria_url = "https://azbykamebeli.ru/catalog/0000057/"
    asyncio.run(parse_categoria_products(categoria_url))
