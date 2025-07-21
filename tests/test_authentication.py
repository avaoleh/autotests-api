import pytest
from http import HTTPStatus

# Клиенты
from clients.authentication.authentication_client import AuthenticationClient
from clients.users.public_users_client import PublicUsersClient

# Схемы
from clients.authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema
from clients.users.users_schema import CreateUserRequestSchema


# Утилиты и ассерты
from tools.assertions.base import assert_status_code
from tools.assertions.authentication import assert_login_response
from tools.assertions.schema import validate_json_schema
from fixtures.users import UserFixture

@pytest.mark.regression
@pytest.mark.authentication
def test_login(
        function_user: UserFixture,  # Используем фикстуру для создания пользователя
        authentication_client: AuthenticationClient
):
    """
    Тест проверяет процесс аутентификации через POST /api/v1/authentication/login.
    """

    # Запрос на логин (login_request -> request)
    request = LoginRequestSchema(email=function_user.email, password=function_user.password)
    # Выполняем логин (login_response -> response)
    response = authentication_client.login_api(request)
    # Валидация ответа (login_response_data -> response_data)
    response_data = LoginResponseSchema.model_validate_json(response.text)

    assert_status_code(response.status_code, HTTPStatus.OK)
    assert_login_response(response_data)

    validate_json_schema(response.json(), response_data.model_json_schema())