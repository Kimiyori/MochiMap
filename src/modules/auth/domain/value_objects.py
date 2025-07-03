from pydantic import EmailStr, ValidationError

from common.pydantic import ConStr


class Username(ConStr):
    min_length: 1
    max_length: 3000


class Password(ConStr):
    min_length: 8
    max_length: 128

    @classmethod
    def __get_validators__(cls):
        yield from super().__get_validators__()
        yield cls.validate_password

    @classmethod
    def validate_password(cls, value):
        # Example: enforce at least one letter and one number
        if not any(c.isalpha() for c in value):
            raise ValueError("Password must contain at least one letter.")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one digit.")
        return value


class Email(ConStr):
    min_length: 5
    max_length: 254

    @classmethod
    def __get_validators__(cls):
        yield from super().__get_validators__()
        yield cls.validate_email

    @classmethod
    def validate_email(cls, value):
        try:
            EmailStr.validate(value)
        except ValidationError as err:
            raise ValueError() from err
        return value
