from dataclasses import dataclass

from pydantic import BaseModel

from modules.auth.domain.value_objects import Email, Password, Username


@dataclass(frozen=True)
class NewUserCommand(BaseModel):
    username: Username
    password: Password
    email: Email
