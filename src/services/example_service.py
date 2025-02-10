import uuid
import logging
import datetime
from pytz import timezone


async def service_dummy(request):

    # get hash id
    id = str(uuid.uuid1().hex)

    # datetime service
    now = datetime.datetime.now(timezone("America/Sao_Paulo"))
    now = now.strftime("%Y-%m-%d-%H-%M-%S")

    # business rules
    a = request.number1
    b = request.number2

    soma = a + b

    msg = "Operation done with success! Result: " + str(soma)

    response = {
        "id": id,
        "datetime": now,
        "service": "dummy",
        "alexa_msg": "teste mensagem alexa",
        "email_msg": "teste mensagem email",
        "telegram_msg": "teste mensagem telegram",
        "result": {"message": msg},
    }

    return response
