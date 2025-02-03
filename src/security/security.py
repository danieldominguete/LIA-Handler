from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_401_UNAUTHORIZED
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

API_KEY_NAME = "x-api-key"
API_KEY = os.getenv("API_KEY")

# auto error enable other authentication alternatives
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Could not validate credentials!"
        )
