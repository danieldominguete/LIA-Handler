from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from channels.gemini import LiaGemini
import os

# Environment variables
load_dotenv(find_dotenv())
GEMINI_KEY = os.getenv("GEMINI_KEY")


import uuid
import logging
import datetime
from pytz import timezone


def get_date_in_portuguese(now: datetime.datetime):

    now = now.strftime("%Y-%m-%d")

    months_in_portuguese = {
        "01": "janeiro",
        "02": "fevereiro",
        "03": "março",
        "04": "abril",
        "05": "maio",
        "06": "junho",
        "07": "julho",
        "08": "agosto",
        "09": "setembro",
        "10": "outubro",
        "11": "novembro",
        "12": "dezembro",
    }

    days_in_portuguese = {
        "01": "primeiro",
        "02": "dois",
        "03": "três",
        "04": "quatro",
        "05": "cinco",
        "06": "seis",
        "07": "sete",
        "08": "oito",
        "09": "nove",
        "10": "dez",
        "11": "onze",
        "12": "doze",
        "13": "treze",
        "14": "quatorze",
        "15": "quinze",
        "16": "dezesseis",
        "17": "dezessete",
        "18": "dezoito",
        "19": "dezenove",
        "20": "vinte",
        "21": "vinte e um",
        "22": "vinte e dois",
        "23": "vinte e três",
        "24": "vinte e quatro",
        "25": "vinte e cinco",
        "26": "vinte e seis",
        "27": "vinte e sete",
        "28": "vinte e oito",
        "29": "vinte e nove",
        "30": "trinta",
        "31": "trinta e um",
    }

    day_of_month = now.split("-")[2]
    month = now.split("-")[1]
    day_of_month_text = days_in_portuguese.get(day_of_month, day_of_month)
    month_text = months_in_portuguese.get(month, month)

    return f"{day_of_month_text} de {month_text}"


async def get_santo_do_dia_service(request):

    # obtain question
    model = LiaGemini()

    # get hash id
    id = str(uuid.uuid1().hex)

    # datetime service
    now = datetime.datetime.now(timezone("America/Sao_Paulo"))
    now_txt = get_date_in_portuguese(now)
    now = now.strftime("%Y-%m-%d")

    question = (
        "Prepare uma resposta no idioma português Brasil. Qual é o santo católico que se celebra no dia de "
        + now_txt
        + " segundo o calendário liturgico do Brasil? Envie uma resposta em texto sem formatação em idioma português do brasil."
    )
    answer = model.get_answer(question)

    response = {
        "id": id,
        "datetime": now,
        "service": "gemini",
        "alexa_msg": answer,
        "email_msg": "teste mensagem email",
        "telegram_msg": answer,
        "result": {"message": answer},
    }

    return response
