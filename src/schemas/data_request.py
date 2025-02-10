from pydantic import BaseModel


class ExampleRequestBody(BaseModel):

    number1: float = 0
    number2: float = 0


class ExampleResponseBody(BaseModel):

    id: str
    datetime: str
    service: str
    alexa_msg: str = ""
    email_msg: str = ""
    telegram_msg: str = ""
    result: dict
