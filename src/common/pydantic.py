from pydantic import BaseModel


class StrRequiredError(TypeError):
    def __init__(self):
        super().__init__('str required')

class StrLengthError(ValueError):
    def __init__(self, min_length, max_length):
        super().__init__(f'string length must be between {min_length} and {max_length}')


class ConStr(str):
    min_length = 0
    max_length = 0

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: str):
        if not isinstance(value, str):
            raise StrRequiredError()

        if not cls.min_length <= len(value) <= cls.max_length:
            raise StrLengthError(cls.min_length, cls.max_length)

        return value

class BaseRequestCommand(BaseModel):
    pass