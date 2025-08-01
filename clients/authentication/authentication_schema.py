from pydantic import BaseModel, Field

from tools.fakers import fake


class TokenSchema(BaseModel):
    """
    Описание структуры аутентификационных токенов.
    """
    token_type: str = Field(alias="tokenType")  # Использовали alise
    access_token: str = Field(alias="accessToken")  # Использовали alise
    refresh_token: str = Field(alias="refreshToken")  # Использовали alise


# Добавили суффикс Schema вместо Dict
class LoginRequestSchema(BaseModel):  # Наследуем от BaseModel вместо TypedDict
    """
    Описание структуры запроса на аутентификацию.
    """
    email: str = Field(default_factory=fake.email)
    password: str = Field(default_factory=fake.password)


# Добавили суффикс Schema вместо Dict
class LoginResponseSchema(BaseModel):  # Наследуем от BaseModel вместо TypedDict
    """
    Описание структуры ответа аутентификации.
    """
    token: TokenSchema


# Добавили суффикс Schema вместо Dict
class RefreshRequestSchema(BaseModel):  # Наследуем от BaseModel вместо TypedDict
    """
    Описание структуры запроса для обновления токена.
    """
    refresh_token: str = Field(alias="refreshToken", default_factory=fake.sentence)  # Использовали alise