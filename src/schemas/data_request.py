from pydantic import BaseModel


class EmptyRequestBody(BaseModel):
    pass


class ExampleRequestBody(BaseModel):

    number1: float = 0
    number2: float = 0
    operator: str
