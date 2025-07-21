from http import HTTPStatus

import pytest

from clients.users.public_users_client import PublicUsersClient
from clients.users.private_users_client import PrivateUsersClient
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.users import assert_create_user_response, assert_get_user_response, assert_user
from tools.fakers import fake

@pytest.mark.users
@pytest.mark.regression
@pytest.mark.parametrize(
    "email_domain",
    [
        "mail.ru",
        "gmail.com",
        "example.com"
    ]
)
def test_create_user(email_domain: str, public_users_client: PublicUsersClient):  # Используем фикстуру API клиента
    # Генерируем email с нужным доменом
    email = fake.email(domain=email_domain)

    # Создаём тело запроса с этим email
    request = CreateUserRequestSchema(
        email=email,
        password=fake.password(),
        last_name=fake.last_name(),
        first_name=fake.first_name(),
        middle_name=fake.middle_name()
    )

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
      - валидацию JSON schema через validate_json_schema
      - соответствие данных пользователя
    """
    # Шаг 1: Выполняем запрос
    response = private_users_client.get_user_me_api()

    # Шаг 2: Проверяем статус
    assert_status_code(response.status_code, HTTPStatus.OK)

    # Шаг 3: Валидируем JSON-схему ответа
    validate_json_schema(response.json(), GetUserResponseSchema.model_json_schema())

    # Шаг 4: Парсим данные для сравнения
    get_user_response = GetUserResponseSchema.model_validate(response.json())

    # Шаг 5: Проверяем корректность тела ответа
    assert_get_user_response(get_user_response, function_user.response)