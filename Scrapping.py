import requests
import pandas as pd
from bs4 import BeautifulSoup
import os.path
import re
import numpy as np

# Niños 1 a 5 años
urls = [
    "https://www.buscalibre.cl/libros-envio-express-chile-ninos-1-a-5-anos_t.html",
    "https://www.buscalibre.cl/libros-envio-express-chile-ninos-1-a-5-anos_t.html?page=2",
    "https://www.buscalibre.cl/libros-envio-express-chile-ninos-1-a-5-anos_t.html?page=3",
    "https://www.buscalibre.cl/libros-envio-express-chile-ninos-1-a-5-anos_t.html?page=4"
]
save_path = "C:/Users/Cristobal-PC/Documents/Python/Projects/Project1/1-a-5-anos"

df = pd.DataFrame(columns=[
    "isbn", "name", "author", "publisher", "year", "language", "pages", "category", "format",
    "review", "price", "url"
])
error_images = []

for url in urls:
    # sale page soup
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    productos = soup.find_all("div", class_="producto")

    # get the book links for an specific page
    links = []
    for i in productos:
        links.append(i.find("a", href=True)["href"])

    # iterate over each book
    for item in range(len(links)):
        # get the soup for a single book
        link = links[item]
        page_book = requests.get(link)
        soup = BeautifulSoup(page_book.content, "html.parser")

        # gather the data of the book
        info_box = soup.find("div", class_="ficha")
        sub_boxes = info_box.find_all(class_="box")
        str_regex = r"[A-Z]*[a-z]+[ñ]*[a-z]*[áéíóú]*[a-z]*[ ]?[A-Z]*[a-z]*[ñ]*[a-z]*[áéíóú]*[a-z]*[ ]?[A-Z]*[a-z]*[ñ]*[a-z]*[áéíóú]*[a-z]*[ ]?"
        for i in range(0, len(sub_boxes), 2):
            if "Formato" in sub_boxes[i].text:
                try:
                    format = re.findall(str_regex, sub_boxes[i+1].text)[0]
                except:
                    format = np.nan
            if "Autor" in sub_boxes[i].text:
                try:
                    author = re.findall(str_regex, sub_boxes[i+1].text)[0]
                except:
                    author = np.nan
            if "Editorial" in sub_boxes[i].text:
                try:
                    publisher = re.findall(str_regex, sub_boxes[i+1].text)[0]
                except:
                    publisher = np.nan
            if "Categoría" in sub_boxes[i].text:
                try:
                    category = re.findall(str_regex, sub_boxes[i+1].text)[0]
                except:
                    category = np.nan
            if "Año" in sub_boxes[i].text:
                try:
                    year = int(re.findall(r"[0-9]+[0-9]+", sub_boxes[i+1].text)[0])
                except:
                    year = np.nan
            if "Idioma" in sub_boxes[i].text:
                try:
                    language = re.findall(str_regex, sub_boxes[i+1].text)[0]
                except:
                    language = np.nan
            if "N° páginas" in sub_boxes[i].text:
                try:
                    pages = int(re.findall(r"[0-9]+", sub_boxes[i+1].text)[0])
                except:
                    pages = np.nan
            if "Isbn" in sub_boxes[i].text:
                try:
                    isbn = int(re.findall(
                        r"[0-9]+[0-9]+[0-9]+[0-9]+[0-9]+[0-9]+[0-9]+[0-9]+[0-9]+",
                        sub_boxes[i+1].text
                    )[0])
                except:
                    isbn = np.nan

        book_name = soup.find("h1")
        try:
            name = book_name.text.replace(u"\xa0", u" ")
        except:
            name = np.nan

        book_review = soup.find("div", class_="descripcionBreve")
        try:
            review = book_review.find("p").text.replace("\n", " ").replace('"', '')
        except:
            review = np.nan

        book_price = soup.find("div", class_="info-libro")
        try:
            price = int(book_price.find("p").text.replace("$", "").replace(".", "").replace(" ", ""))
        except:
            price = np.nan


        # concat the data to a pandas dataframe
        d = {
            "isbn": isbn,
            "name": name,
            "author": author,
            "publisher": publisher,
            "year": year,
            "language": language,
            "pages": pages,
            "category": category,
            "format": format,
            "review": review,
            "price":price,
            "url": url
        }
        df_row = pd.DataFrame(data=d, index=[item])
        df = pd.concat([df, df_row])

        # create the book image
        image = soup.find("div", class_="imagen")
        try:
            response = requests.get(image.find("img")["data-src"])
            complete_name = os.path.join(save_path, str(isbn)+".jpg")
            file = open(complete_name, "wb")
            file.write(response.content)
            file.close()
        except:
            response = requests.get(image.find("img")["src"])
            complete_name = os.path.join(save_path, str(isbn)+".jpg")
            file = open(complete_name, "wb")
            file.write(response.content)
            file.close()
