from http import HTTPStatus

import pytest

from clients.users.public_users_client import PublicUsersClient
from clients.users.private_users_client import PrivateUsersClient
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.users import assert_create_user_response, assert_get_user_response, assert_user

@pytest.mark.users
@pytest.mark.regression
def test_create_user(public_users_client: PublicUsersClient):  # Используем фикстуру API клиента

    request = CreateUserRequestSchema()
    response = public_users_client.create_user_api(request)
    response_data = CreateUserResponseSchema.model_validate_json(response.text)

    assert_status_code(response.status_code, HTTPStatus.OK)
    # Используем функцию для проверки ответа создания юзера
    assert_create_user_response(request, response_data)

    validate_json_schema(response.json(), response_data.model_json_schema())



@pytest.mark.users
@pytest.mark.regression
def test_get_user_me(private_users_client: PrivateUsersClient, function_user) -> None:
    """
    Тестируем GET /api/v1/users/me
    Проверяем:
      - статус-код 200
      - валидацию JSON schema
      - соответствие данных
    """
    # Шаг 1: Выполняем запрос
    response = private_users_client.get_user_me_api()

    # Шаг 2: Проверяем статус
    assert response.status_code == HTTPStatus.OK, (
        f"Ожидался статус 200, получен {response.status_code}"
    )

    # Шаг 3: Парсим тело ответа и валидируем схему
    get_user_response = GetUserResponseSchema.model_validate(response.json())

    # Шаг 4: Проверяем корректность данных
    assert_get_user_response(get_user_response, function_user.response)