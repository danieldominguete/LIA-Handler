"""Script Main de Chamada da API"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from mangum import Mangum
import uvicorn
import logging
import watchtower
from log.payload_logging import save_response_to_s3
from schemas.data_request import ResponseRequestBody
from services.bible_service import bible_message_service
from services.alexa_service import alexa_service
from services.gemini_service import get_santo_do_dia_service, get_dica_saude_service
from channels.telegram import LiaTelegram


from security.security import verify_api_key
from dotenv import load_dotenv, find_dotenv

import os

# Environment variables
load_dotenv(find_dotenv())
ENV = os.getenv("ENV")

# ----------------------------------------------------------

# Criando estrutura de logs
script_name = os.path.basename(__file__)

if ENV == "local":

    logger = logging.getLogger(script_name)
    logger.setLevel(logging.INFO)

    # Create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter(
        "%(asctime)s: %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    ch.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(ch)

    logger.info("Setting up logger for local environment")

else:
    logger = logging.getLogger(script_name)
    logger.setLevel(logging.INFO)

    # Create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Create CloudWatch handler
    cloudwatch_handler = watchtower.CloudWatchLogHandler(log_group="LIA-Handler-Logs")
    cloudwatch_handler.setLevel(logging.INFO)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter(
        "%(asctime)s: %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    ch.setFormatter(formatter)
    cloudwatch_handler.setFormatter(formatter)

    # Add the handlers to the logger

    logger.addHandler(ch)
    logger.addHandler(cloudwatch_handler)

    logger.info("Setting up logger for local environment")


# ----------------------------------------------------------
# Start application
app = FastAPI(title="LIA Handler")

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# General objects
logger.info("Creating general objects...")
lia_telegram = LiaTelegram()


logger.info("Start services...")


# Chamada o serviço de teste de serviço
@app.post("/hello", dependencies=[Depends(verify_api_key)])
async def hello():
    logger.info("Starting hello service ...")
    try:
        msg = "LIA API is running!"
        lia_telegram.send_simple_msg_chat(message=msg)
        return {"message": msg}
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Ops... internal error!",
                "exception": str(e),
                "content": str(""),
            },
        )


# Exemplo de serviço com request
# @app.post("/response", dependencies=[Depends(verify_api_key)])
# async def response(request: ExampleRequestBody):
#     logger.info("Starting response service ...")
#     try:

#         # call the service
#         response = await service_dummy(request=request)

#         # save result log
#         save_response_to_s3(response=response)

#         # telegram message
#         msg = response.get("telegram_msg")
#         lia_telegram.send_simple_msg_chat(message=msg)

#         return response

#     except Exception as e:
#         error_msg = f"An error occurred: {e}"
#         logger.error(error_msg)
#         raise HTTPException(
#             status_code=HTTP_500_INTERNAL_SERVER_ERROR,
#             detail={
#                 "error": "Ops... internal error!",
#                 "exception": str(e),
#                 "content": str(request),
#             },
#         )


# Chamada o serviço de mensagem biblica
@app.post("/bible", dependencies=[Depends(verify_api_key)])
async def bible():
    logger.info("Starting bible service ...")
    try:
        # call the service
        request = None
        response = await bible_message_service(request=request)

        # save result log
        save_response_to_s3(response=response)

        # telegram message
        msg = response.get("telegram_msg")
        lia_telegram.send_simple_msg_chat(message=msg)

        return response
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Ops... internal error!",
                "exception": str(e),
                "content": str(request),
            },
        )


# Exemplo de serviço com request
@app.post("/response", dependencies=[Depends(verify_api_key)])
async def response(request: ResponseRequestBody):
    logger.info("Starting response service ...")
    try:

        if request.task == "santo_do_dia":
            # call the service
            response = await get_santo_do_dia_service(request=request)

            # save result log
            save_response_to_s3(response=response)

            # telegram message
            msg = response.get("telegram_msg")
            lia_telegram.send_simple_msg_chat(message=msg)

            return response

        if request.task == "dica_saude":
            # call the service
            response = await get_dica_saude_service(request=request)

            # save result log
            save_response_to_s3(response=response)

            # telegram message
            msg = response.get("telegram_msg")
            lia_telegram.send_simple_msg_chat(message=msg)

            return response

    except Exception as e:
        error_msg = f"An error occurred: {e}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Ops... internal error!",
                "exception": str(e),
                "content": str(request),
            },
        )


# Chamada o serviço de construcao de feeds alexa a partir dos logs de D-1 e D0
@app.post("/alexa", dependencies=[Depends(verify_api_key)])
async def alexa():
    logger.info("Starting alexa service ...")
    try:
        # call the service
        request = None
        response = await alexa_service(request=None)

        # save result log
        save_response_to_s3(response=response)

        # telegram message
        msg = response.get("telegram_msg")
        lia_telegram.send_simple_msg_chat(message=msg)

        return response

    except Exception as e:
        error_msg = f"An error occurred: {e}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Ops... internal error!",
                "exception": str(e),
                "content": str(request),
            },
        )


handler = Mangum(app=app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
