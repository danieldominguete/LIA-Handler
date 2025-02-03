from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import uvicorn
import logging
from service.example_service import service_dummy
from schemas.example_data_request import ExampleRequestBody
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from lib.message.lia_telegram import LiaTelegram
from dotenv import load_dotenv, find_dotenv
import os

# ----------------------------------------------------------
# terminal logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s: %(levelname)s - %(message)s",
    datefmt="%y-%m-%d %H:%M",
)
# ----------------------------------------------------------
# Start application

load_dotenv(find_dotenv())

API_KEY_NAME = "X-API-Key"
API_KEY = os.getenv("API_KEY")

app = FastAPI(title="LIA Handler")


# Função para verificar o token de API
api_key_header = APIKeyHeader(name=API_KEY_NAME)


async def verify_api_key(api_key_header: str = Depends(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(status_code=401, detail="Token de API inválido")


app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get("/")
# async def hello():
#     response = {"message": "Hello World"}
#     logging.info(f"/ response: {response}")
#     return response


# @app.post("/example")
# # async def example(request: ExampleRequestBody, api_key: APIKey = Depends(get_api_key)):
# async def example(request: ExampleRequestBody):
#     response = await service_dummy(request=request)

#     if not response:
#         logging.error(f"Request: {request}")
#         raise HTTPException(
#             status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Ops... internal error!"
#         )

#     logging.info(f"Request: {request}")
#     logging.info(f"Response: {response}")

#     return response


@app.post("/hello", dependencies=[Depends(verify_api_key)])
# @app.post("/hello")
async def hello():
    msg = "teste LIA handler"
    lia_telegram = LiaTelegram()
    lia_telegram.send_simple_msg_chat(message=msg)
    return {"message": "Hello World"}


handler = Mangum(app=app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
