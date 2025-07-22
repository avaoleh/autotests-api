from typing import TypedDict
from pydantic import BaseModel
from httpx import Client
from functools import lru_cache  # Импортируем функцию для кеширования

from clients.authentication.authentication_client import get_authentication_client
from clients.authentication.authentication_schema import LoginRequestSchema

# Добавили суффикс Schema вместо Dict
class AuthenticationUserSchema(BaseModel, frozen=True):  # Добавили параметр frozen=True
    email: str
    password: str


# Создаем private builder
@lru_cache(maxsize=None)  # Кешируем возвращаемое значение
def get_private_http_client(user: AuthenticationUserSchema) -> Client:
    authentication_client = get_authentication_client()

    # Используем модель LoginRequestSchema
    # Значения теперь извлекаем не по ключу, а через атрибуты
    login_request = LoginRequestSchema(email=user.email, password=user.password)
    login_response = authentication_client.login(login_request)

    return Client(
        timeout=100,
        base_url="http://localhost:8000",
        # Значения теперь извлекаем не по ключу, а через атрибуты
        headers={"Authorization": f"Bearer {login_response.token.access_token}"}
    )