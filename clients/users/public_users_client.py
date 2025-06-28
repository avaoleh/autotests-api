from typing import TypedDict, Dict, Any

from httpx import Response

from clients.api_client import APIClient


class CreateUserRequestDict(TypedDict):
    """
    TypedDict для тела запроса создания пользователя.

    Attributes:
        email (str): Email пользователя.
        password (str): Пароль пользователя.
        firstName (str): Имя пользователя.
        lastName (str): Фамилия пользователя.
        middleName (str | None): Отчество пользователя (опционально).
    """
    email: str
    password: str
    firstName: str
    lastName: str
    middleName: str


class PublicUsersClient(APIClient):
    """
    Клиент для работы с публичным эндпоинтом /api/v1/users.
    Предоставляет методы для создания и управления пользователями.
    """

    def create_user_api(self, request: CreateUserRequestDict) -> Response:
        """
        Метод выполняет POST-запрос к /api/v1/users для создания нового пользователя.

        :param request: Словарь с данными пользователя, соответствующий структуре CreateUserRequestDict.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.post("/api/v1/users", json=request)