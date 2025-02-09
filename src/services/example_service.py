import uuid
import logging
import datetime
from pytz import timezone


async def service_dummy(request):

    # get hash id
    id = str(uuid.uuid1().hex)

    # datetime local
    now = datetime.datetime.now(timezone("America/Sao_Paulo"))
    now = now.strftime("%Y-%m-%d-%H-%M-%S")

    try:
        a = request.number1
        b = request.number2

        soma = a + b

        msg = "Operation done with success! Result: " + str(soma)

        response = {
            "id": id,
            "datetime": now,
            "service": "dummy",
            "result": {"message": msg},
        }

        return response

    except Exception as e:
        msg = "API Error " + str(e)
        logging.error(msg)
        response.update({"msg": msg})

        return None
