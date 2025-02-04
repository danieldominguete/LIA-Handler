"""
Get a random message from bible file
"""

import logging
import random
import datetime
import uuid
from dao.file import load_data_from_json


async def bible_message_service(request):

    # ===========================================================================================
    # Get random bible messages from file

    # get execution id
    id = str(uuid.uuid1().hex)

    logging.info(
        "Consultando uma mensagem aleatória no arquivo de mensagens biblicas..."
    )

    bible_data = load_data_from_json("src/static/biblia.json", encoding="utf-8-sig")
    service_config = load_data_from_json("src/config/lia_bible.json")

    date_ref_dt = datetime.datetime.now()
    date_ref = date_ref_dt.strftime("%Y-%m-%d %H:%M:%S")

    # selecionando o livro
    list_of_books = list(service_config.get("books"))
    random_selected = random.randint(0, len(list_of_books) - 1)
    book_selected = list_of_books[random_selected]
    book_id = book_selected.get("id")
    book_txt = bible_data[book_id]
    book_name = book_txt.get("name")

    # selecionando o capitulo
    book_n_chapters = book_selected.get("n_chapters")
    chapter_selected = random.randint(0, book_n_chapters - 1)
    chapter_txt = book_txt.get("chapters")[chapter_selected]

    book_how_to_read = book_selected.get("to_read")

    if book_how_to_read == "versiculo":
        # selecionando versiculo
        versiculo_selected = random.randint(0, len(chapter_txt) - 1)
        intro_message = (
            "Hoje tenho uma palavra especial para você de "
            + book_name
            + " capítulo "
            + str(chapter_selected)
            + " versículo "
            + str(versiculo_selected)
            + ". "
        )
        message = chapter_txt[versiculo_selected]
    else:
        # leitura de todo texto do capitulo
        intro_message = (
            "Hoje tenho uma palavra especial para você de "
            + book_name
            + " capítulo "
            + str(chapter_selected)
            + "."
        )
        message = " ".join(chapter_txt)

    logging.info("Mensagem coletada do livro de " + book_name + " :: " + message)
    logging.info("Consultando arquivo de mensagens biblicas... concluido!")

    response = {
        "execution_id": id,
        "datetime": date_ref,
        "message": intro_message + message,
    }

    return response
