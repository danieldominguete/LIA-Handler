"""Security Package"""

from fastapi import HTTPException, Depends
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_401_UNAUTHORIZED
import os
from dotenv import load_dotenv, find_dotenv

# Load API Token

load_dotenv(find_dotenv())
API_KEY_NAME = "X-API-Key"
API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name=API_KEY_NAME)


async def verify_api_key(api_key_header: str = Depends(api_key_header)):
    """
    Asynchronous function to verify the provided API key.

    Args:
        api_key_header (str): The API key provided in the request header.

    Returns:
        str: The validated API key if it matches the expected API key.

    Raises:
        HTTPException: If the provided API key does not match the expected API key,
                       an HTTP 401 Unauthorized exception is raised with a detail message.
    """
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Token inválido")
