from pydantic import BaseModel


class ResponseRequestBody(BaseModel):

    task: str = ""


class ExampleResponseBody(BaseModel):

    id: str
    datetime: str
    service: str
    alexa_msg: str = ""
    email_msg: str = ""
    telegram_msg: str = ""
    result: dict
