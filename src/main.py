"""Script Main de Chamada da API"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from mangum import Mangum
import uvicorn
import logging
from schemas.data_request import EmptyRequestBody
from services.bible_service import bible_message_service
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

# todo: configurar o logging

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
lia_telegram = LiaTelegram()
lia_alexa = LiaAlexa()


# Chamada o serviço de teste de serviço
@app.post("/hello", dependencies=[Depends(verify_api_key)])
async def hello():
    try:
        msg = "LIA API is running!"
        lia_telegram.send_simple_msg_chat(message=msg)
        return {"message": msg}
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        logging.error(error_msg)
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ops... internal error! " + error_msg,
        )


# Chamada o serviço de mensagem biblica
@app.post("/bible", dependencies=[Depends(verify_api_key)])
async def bible(request: EmptyRequestBody):
    try:
        response = await bible_message_service(request=request)

        if response is None:
            logging.error(f"Request: {request}")
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ops... internal error!",
            )
        else:

            # telegram message
            msg = response.get("message")
            lia_telegram.send_simple_msg_chat(message=msg)

            # alexa message
            lia_alexa.register_flash_briefing_feed(message=msg, title="LIA Bible")

            return response
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        logging.error(error_msg)
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ops... internal error! " + error_msg,
        )


handler = Mangum(app=app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
