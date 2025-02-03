from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKey
from security.security import get_api_key
from mangum import Mangum
import uvicorn
import logging
from service.example_service import service_dummy
from schemas.example_data_request import ExampleRequestBody
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

# ----------------------------------------------------------
# terminal logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s: %(levelname)s - %(message)s",
    datefmt="%y-%m-%d %H:%M",
)
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


@app.get("/")
async def hello():
    response = {"message": "Hello World"}
    logging.info(f"/ response: {response}")
    return response


@app.post("/example")
async def example(request: ExampleRequestBody, api_key: APIKey = Depends(get_api_key)):
    response = await service_dummy(request=request)

    if not response:
        logging.error(f"Request: {request}")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Ops... internal error!"
        )

    logging.info(f"Request: {request}")
    logging.info(f"Response: {response}")

    return response


handler = Mangum(app=app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
