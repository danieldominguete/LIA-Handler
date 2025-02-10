import uuid
import logging
import datetime
from pytz import timezone
from channels.alexa import LiaAlexa
from dao.aws_s3 import download_all_from_s3
from dao.file import create_folder

PATH_ENV = "prd"


# service to update alexa flash briefing from logs
async def alexa_service(request):

    # alexa object
    lia_alexa = LiaAlexa()

    # get hash id
    id = str(uuid.uuid1().hex)

    # datetime service
    now = datetime.datetime.now(timezone("America/Sao_Paulo"))
    now = now.strftime("%Y-%m-%d-%H-%M-%S")

    # create folder to download logs
    target_folder = "/tmp/feeds/"
    create_folder(target_folder)

    # ----------------------------------------------------------
    # current date json logs
    today = datetime.datetime.now(timezone("America/Sao_Paulo"))
    today = today.strftime("%Y-%m-%d")

    # get all logs from S3 :: bible
    path_day = "date=" + str(today)
    download_all_from_s3(
        "lia-handler",
        "lia_logs/" + PATH_ENV + "/bible/" + path_day,
        target_folder,
    )

    # ----------------------------------------------------------
    # yesterday json logs
    yesterday = datetime.datetime.now(
        timezone("America/Sao_Paulo")
    ) - datetime.timedelta(days=1)
    yesterday = yesterday.strftime("%Y-%m-%d")

    # get all logs from S3 :: bible
    path_day = "date=" + str(yesterday)
    download_all_from_s3(
        "lia-handler",
        "lia_logs/" + PATH_ENV + "/bible/" + path_day,
        target_folder,
    )

    # ----------------------------------------------------------
    # save all contents to
    n_feeds = lia_alexa.register_json_logs_briefing_feed(target_folder)

    txt = "Foram atualizados " + str(n_feeds) + " feeds no Alexa Flash Briefing."

    response = {
        "id": id,
        "datetime": now,
        "service": "alexa",
        "alexa_msg": txt,
        "email_msg": txt,
        "telegram_msg": txt,
        "result": {"n_feeds": n_feeds},
    }

    return response
