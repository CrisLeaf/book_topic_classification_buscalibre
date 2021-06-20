import requests
import pandas as pd
from bs4 import BeautifulSoup
import os.path
import re
import numpy as np
import csv

path_folder = ".../Project/"

# ------------------------------------------------------------------------------------------------
# Initial definitions

# dictionary with all books urls with topics
urls_dict = {
    "espiritualidad-y-auto-ayuda": [
        "https://www.buscalibre.cl/libros-envio-express-chile-espiritualidad-y-autoayuda_t.html",
        "https://www.buscalibre.cl/libros-envio-express-chile-espiritualidad-y-autoayuda_t.html?page=2",
        "https://www.buscalibre.cl/libros-envio-express-chile-espiritualidad-y-autoayuda_t.html?page=3"
    ],
    "1-5-anos": [
        "https://www.buscalibre.cl/libros-envio-express-chile-ninos-1-a-5-anos_t.html",
        "https://www.buscalibre.cl/libros-envio-express-chile-ninos-1-a-5-anos_t.html?page=2",
        "https://www.buscalibre.cl/libros-envio-express-chile-ninos-1-a-5-anos_t.html?page=3",
        "https://www.buscalibre.cl/libros-envio-express-chile-ninos-1-a-5-anos_t.html?page=4"
    ],
    "6-10-anos": [
        "https://www.buscalibre.cl/libros-envio-express-chile-ninos-6-a-10-anos_t.html",
        "https://www.buscalibre.cl/libros-envio-express-chile-ninos-6-a-10-anos_t.html?page=2",
        "https://www.buscalibre.cl/libros-envio-express-chile-ninos-6-a-10-anos_t.html?page=3",
        "https://www.buscalibre.cl/libros-envio-express-chile-ninos-6-a-10-anos_t.html?page=4",
        "https://www.buscalibre.cl/libros-envio-express-chile-ninos-6-a-10-anos_t.html?page=5"
    ],
    "juvenil": [
        "https://www.buscalibre.cl/libros-envio-express-chile-literatura-juvenil_t.html",
        "https://www.buscalibre.cl/libros-envio-express-chile-literatura-juvenil_t.html?page=2",
        "https://www.buscalibre.cl/libros-envio-express-chile-literatura-juvenil_t.html?page=3",
        "https://www.buscalibre.cl/libros-envio-express-chile-literatura-juvenil_t.html?page=4",
        "https://www.buscalibre.cl/libros-envio-express-chile-literatura-juvenil_t.html?page=5"
    ],
    "romántica-y-erotica": [
        "https://www.buscalibre.cl/libros-envio-express-chile-romantica-y-erotica_t.html",
        "https://www.buscalibre.cl/libros-envio-express-chile-romantica-y-erotica_t.html?page=2"
    ],
    "best-sellers-no-ficcion": [
        "https://www.buscalibre.cl/libros-envio-express-chile-best-sellers-no-ficcion_t.html",
        "https://www.buscalibre.cl/libros-envio-express-chile-best-sellers-no-ficcion_t.html?page=2",
        "https://www.buscalibre.cl/libros-envio-express-chile-best-sellers-no-ficcion_t.html?page=3",
        "https://www.buscalibre.cl/libros-envio-express-chile-best-sellers-no-ficcion_t.html?page=4",
        "https://www.buscalibre.cl/libros-envio-express-chile-best-sellers-no-ficcion_t.html?page=5",
        "https://www.buscalibre.cl/libros-envio-express-chile-best-sellers-no-ficcion_t.html?page=6"
    ],
    "best-sellers-ficcion": [
        "https://www.buscalibre.cl/libros-envio-express-chile-best-sellers-ficcion_t.html",
        "https://www.buscalibre.cl/libros-envio-express-chile-best-sellers-ficcion_t.html?page=2",
        "https://www.buscalibre.cl/libros-envio-express-chile-best-sellers-ficcion_t.html?page=3",
        "https://www.buscalibre.cl/libros-envio-express-chile-best-sellers-ficcion_t.html?page=4",
        "https://www.buscalibre.cl/libros-envio-express-chile-best-sellers-ficcion_t.html?page=5",
        "https://www.buscalibre.cl/libros-envio-express-chile-best-sellers-ficcion_t.html?page=6",
        "https://www.buscalibre.cl/libros-envio-express-chile-best-sellers-ficcion_t.html?page=7",
        "https://www.buscalibre.cl/libros-envio-express-chile-best-sellers-ficcion_t.html?page=8",
        "https://www.buscalibre.cl/libros-envio-express-chile-best-sellers-ficcion_t.html?page=9",
        "https://www.buscalibre.cl/libros-envio-express-chile-best-sellers-ficcion_t.html?page=10",
        "https://www.buscalibre.cl/libros-envio-express-chile-best-sellers-ficcion_t.html?page=11",
        "https://www.buscalibre.cl/libros-envio-express-chile-best-sellers-ficcion_t.html?page=12"
    ],
    "finanzas-y-economia": [
        "https://www.buscalibre.cl/libros-envio-express-chile-finanzas-y-economia_t.html"
    ],
    "biografias": [
        "https://www.buscalibre.cl/libros-envio-express-chile-biografias_t.html",
        "https://www.buscalibre.cl/libros-envio-express-chile-biografias_t.html?page=2"
    ],
    "cocina-y-alimentacion": [
        "https://www.buscalibre.cl/libros-envio-express-chile-cocina-y-alimentacion_t.html"
    ],
    "actualidad-y-politica": [
        "https://www.buscalibre.cl/libros-envio-express-chile-actualidad-y-politica_t.html",
        "https://www.buscalibre.cl/libros-envio-express-chile-actualidad-y-politica_t.html?page=2",
        "https://www.buscalibre.cl/libros-envio-express-chile-actualidad-y-politica_t.html?page=3"
    ],
    "ocio-y-humor": [
        "https://www.buscalibre.cl/libros-envio-express-chile-ocio-y-humor_t.html",
        "https://www.buscalibre.cl/libros-envio-express-chile-ocio-y-humor_t.html?page=2",
        "https://www.buscalibre.cl/libros-envio-express-chile-ocio-y-humor_t.html?page=3"
    ],
    "grandes-descuentos": [
        "https://www.buscalibre.cl/libros-envio-24-horas-con-descuento-cl_t.html",
        "https://www.buscalibre.cl/libros-envio-24-horas-con-descuento-cl_t.html?page=2",
        "https://www.buscalibre.cl/libros-envio-24-horas-con-descuento-cl_t.html?page=3",
        "https://www.buscalibre.cl/libros-envio-24-horas-con-descuento-cl_t.html?page=4",
        "https://www.buscalibre.cl/libros-envio-24-horas-con-descuento-cl_t.html?page=5",
        "https://www.buscalibre.cl/libros-envio-24-horas-con-descuento-cl_t.html?page=6",
        "https://www.buscalibre.cl/libros-envio-24-horas-con-descuento-cl_t.html?page=7",
        "https://www.buscalibre.cl/libros-envio-24-horas-con-descuento-cl_t.html?page=8",
        "https://www.buscalibre.cl/libros-envio-24-horas-con-descuento-cl_t.html?page=9",
        "https://www.buscalibre.cl/libros-envio-24-horas-con-descuento-cl_t.html?page=10",
        "https://www.buscalibre.cl/libros-envio-24-horas-con-descuento-cl_t.html?page=11",
        "https://www.buscalibre.cl/libros-envio-24-horas-con-descuento-cl_t.html?page=12",
        "https://www.buscalibre.cl/libros-envio-24-horas-con-descuento-cl_t.html?page=13",
        "https://www.buscalibre.cl/libros-envio-24-horas-con-descuento-cl_t.html?page=14",
        "https://www.buscalibre.cl/libros-envio-24-horas-con-descuento-cl_t.html?page=15",
        "https://www.buscalibre.cl/libros-envio-24-horas-con-descuento-cl_t.html?page=16",
        "https://www.buscalibre.cl/libros-envio-24-horas-con-descuento-cl_t.html?page=17"
    ]
}
str_regex = r"[A-Z]*[a-z]+[ñ]*[a-z]*[áéíóú]*[a-z]*[ ]?[A-Z]*[a-z]*[ñ]*[a-z]*[áéíóú]*[a-z]*[ ]?[A-Z]*[a-z]*[ñ]*[a-z]*[áéíóú]*[a-z]*[ ]?"     # for strings
num1_regex = r"[0-9]+"      # for pages
num2_regex = r"[0-9]+[0-9]+"        # for year
num9_regex = r"[0-9]+[0-9]+[0-9]+[0-9]+[0-9]+[0-9]+[0-9]+[0-9]+[0-9]+"      # for isbn
df = pd.DataFrame(columns=[
    "isbn", "name", "author", "publisher", "year", "language", "pages", "category", "format",
    "review", "price", "url", "topic"
])

# Gathering functions
def str_feature_gather(feature, boxes):
    output = np.nan
    for i in range(0, len(boxes), 2):
        if feature in boxes[i].text:
            try:
                output = re.findall(str_regex, boxes[i+1].text)[0]
            except:
                pass
            break
    return output

def num1_feature_gather(feature, boxes):
    output = np.nan
    for i in range(0, len(boxes), 2):
        if feature in boxes[i].text:
            try:
                output = re.findall(num1_regex, boxes[i+1].text)[0]
            except:
                pass
            break
    return output

def num2_feature_gather(feature, boxes):
    output = np.nan
    for i in range(0, len(boxes), 2):
        if feature in boxes[i].text:
            try:
                output = re.findall(num2_regex, boxes[i+1].text)[0]
            except:
                pass
            break
    return output

def num9_feature_gather(feature, boxes):
    output = np.nan
    for i in range(0, len(boxes), 2):
        if feature in boxes[i].text:
            try:
                output = re.findall(num9_regex, boxes[i+1].text)[0]
            except:
                pass
            break
    return output

df_index = 0

# ------------------------------------------------------------------------------------------------
# Data Scrap

# Iterate over topics
for key, url_list in urls_dict.items():
    # Create and save directory
    save_path = path_folder + str(key)
    os.mkdir(save_path)

    # Iterate over each page of an specific topic
    for url in url_list:
        # Sale page soup
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        productos = soup.find_all("div", class_="producto")

        # Get the book links for an specific page
        links = [i.find("a", href=True)["href"] for i in productos]
        
        # Iterate over each book of an specific page
        for link in links:
            # There are some books with no information, so we need the try command
            try:
                # Get the soup for a single book
                book_page = requests.get(link)
                soup = BeautifulSoup(book_page.content, "html.parser")

                # Gather the data of the book from the info boxes
                info_box = soup.find("div", class_="ficha")
                sub_boxes = info_box.find_all(class_="box")

                format = str_feature_gather("Formato", sub_boxes)
                author = str_feature_gather("Autor", sub_boxes)
                publisher = str_feature_gather("Editorial", sub_boxes)
                category = str_feature_gather("Categoría", sub_boxes)
                language = str_feature_gather("Idioma", sub_boxes)
                pages = num1_feature_gather("N° páginas", sub_boxes)
                year = num2_feature_gather("Año", sub_boxes)
                isbn = num9_feature_gather("Isbn", sub_boxes)

                # Gather the data of the book from the book description
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

                # Concat the data to a pandas dataframe
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
                    "url": link,
                    "topic": str(key)
                }
                df_row = pd.DataFrame(data=d, index=[df_index])
                df = pd.concat([df, df_row])
                df_index += 1

                # Download the book frontpage image (if it's exists)
                image = soup.find("div", class_="imagen")
                try:
                    response = requests.get(image.find("img")["data-src"])
                    complete_name = os.path.join(save_path, str(isbn)+".jpg")
                    with open(complete_name, "wb") as file:
                        file.write(response.content)
                except:
                    response = requests.get(image.find("img")["src"])
                    complete_name = os.path.join(save_path, str(isbn)+".jpg")
                    with open(complete_name, "wb") as file:
                        file.write(response.content)

            except:
                pass

# CSV write
csv_path = path_folder + "buscalibre_data.csv"
df.to_csv(csv_path, index=False)
