import pytest
from http import HTTPStatus

# Клиенты
from clients.authentication.authentication_client import get_authentication_client
from clients.users.public_users_client import get_public_users_client

# Схемы
from clients.authentication.authentication_schema import LoginResponseSchema
from clients.users.users_schema import CreateUserRequestSchema

# Утилиты и ассерты
from tools.assertions.base import assert_status_code
from tools.assertions.authentication import assert_login_response
from tools.assertions.schema import validate_json_schema


def test_login():
    """
    Тест проверяет процесс аутентификации через POST /api/v1/authentication/login.
    """

    # Arrange: Создаем клиенты
    public_users_client = get_public_users_client()
    authentication_client = get_authentication_client()

    # Act 1: Создать нового пользователя
    request = CreateUserRequestSchema()
    create_user_response = public_users_client.create_user_api(request)

    # Assert для создания пользователя
    assert_status_code(create_user_response.status_code, HTTPStatus.OK)

    # Act 2: Выполнить аутентификацию
    login_response = authentication_client.login_api(request)

    # Assert 1: Проверить статус-код
    assert_status_code(login_response.status_code, HTTPStatus.OK)

    # Assert 2: Десериализовать JSON и проверить содержимое
    login_response_data = LoginResponseSchema.model_validate_json(login_response.text)
    assert_login_response(login_response_data)

    # Assert 3: Валидация JSON-схемы ответа
    validate_json_schema(login_response.json(), login_response_data.model_json_schema())