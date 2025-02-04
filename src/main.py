"""Script Main de Chamada da API"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import uvicorn
import logging

# from service.example_service import service_dummy
# from schemas.example_data_request import ExampleRequestBody
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from message.lia_telegram import LiaTelegram
from security.security import verify_api_key


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


handler = Mangum(app=app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
