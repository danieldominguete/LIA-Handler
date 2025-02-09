"""Script Main de Chamada da API"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from mangum import Mangum
import uvicorn
from log.terminal_logging import LIALogs
from log.payload_logging import save_response_to_s3
from schemas.data_request import ExampleRequestBody
from services.bible_service import bible_message_service
from services.example_service import service_dummy
from channels.telegram import LiaTelegram
from channels.alexa import LiaAlexa
from security.security import verify_api_key
from dotenv import load_dotenv, find_dotenv

import os

# Environment variables
load_dotenv(find_dotenv())
ENV = os.getenv("ENV")

# ----------------------------------------------------------
# terminal logging

# Criando estrutura de logs
script_name = os.path.basename(__file__)
log = LIALogs(script_name=script_name)
log.init_run()

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
log.info("Creating general objects...")
lia_telegram = LiaTelegram()
lia_alexa = LiaAlexa()

log.info("Start services...")


# Chamada o serviço de teste de serviço
@app.post("/hello", dependencies=[Depends(verify_api_key)])
async def hello():
    try:
        msg = "LIA API is running!"
        lia_telegram.send_simple_msg_chat(message=msg)
        return {"message": msg}
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        log.error(error_msg)
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Ops... internal error!",
                "exception": str(e),
                "content": str(request),
            },
        )


# Chamada o serviço com request
@app.post("/response", dependencies=[Depends(verify_api_key)])
async def response(request: ExampleRequestBody):
    try:
        response = await service_dummy(request=request)

        if response is None:
            log.error(f"Request: {request}")
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "Ops... internal error!",
                    "exception": str(e),
                    "content": str(request),
                },
            )
        else:

            # save log
            save_response_to_s3(response=response)

            # telegram message
            msg = response.get("result").get("message")
            lia_telegram.send_simple_msg_chat(message=msg)

            # alexa message
            lia_alexa.register_flash_briefing_feed(message=msg, title="LIA Bible")

            return response
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        log.error(error_msg)
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Ops... internal error!",
                "exception": str(e),
                "content": str(request),
            },
        )


# Chamada o serviço de mensagem biblica
@app.post("/bible", dependencies=[Depends(verify_api_key)])
async def bible():
    try:
        request = None
        response = await bible_message_service(request=None)

        if response is None:
            log.error(f"Request: {request}")
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "Ops... internal error!",
                    "exception": str(e),
                    "content": str(request),
                },
            )
        else:

            # save log
            save_response_to_s3(response=response)

            # telegram message
            msg = response.get("result").get("message")
            lia_telegram.send_simple_msg_chat(message=msg)

            # alexa message
            lia_alexa.register_flash_briefing_feed(message=msg, title="LIA Bible")

            return response
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        log.error(error_msg)
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
