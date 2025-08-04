from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema
from clients.users.users_schema import UserSchema, GetUserResponseSchema
from tools.assertions.base import assert_equal
import allure
from tools.logger import get_logger  # Импортируем функцию для создания логгера

logger = get_logger("USERS_ASSERTIONS")

@allure.step("Check create user response")
def assert_create_user_response(request: CreateUserRequestSchema, response: CreateUserResponseSchema):
    """
    Проверяет, что ответ на создание пользователя соответствует запросу.

    :param request: Исходный запрос на создание пользователя.
    :param response: Ответ API с данными пользователя.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    # Логируем факт начала проверки
    logger.info("Check create user response")

    assert_equal(response.user.email, request.email, "email")
    assert_equal(response.user.last_name, request.last_name, "last_name")
    assert_equal(response.user.first_name, request.first_name, "first_name")
    assert_equal(response.user.middle_name, request.middle_name, "middle_name")

@allure.step("Check user")
def assert_user(actual: UserSchema, expected: UserSchema) -> None:
    """
    Проверяет, что два объекта UserSchema содержат одинаковые значения полей.

    :param actual: Полученные данные пользователя.
    :param expected: Ожидаемые данные пользователя.
    :raises AssertionError: Если поля не совпадают.
    """
    # Логируем факт начала проверки
    logger.info("Check user")

    assert_equal(actual.id, expected.user.id, "id")
    assert_equal(actual.email, expected.user.email, "email")
    assert_equal(actual.first_name, expected.user.first_name, "first_name")
    assert_equal(actual.last_name, expected.user.last_name, "last_name")
    assert_equal(actual.middle_name, expected.user.middle_name, "middle_name")

@allure.step("Check get user response")
def assert_get_user_response(
    get_user_response: GetUserResponseSchema,
    create_user_response: CreateUserResponseSchema
) -> None:
    """
    Проверяет, что ответ от /api/v1/users/me соответствует данным созданного пользователя.

    :param get_user_response: Ответ API на GET /api/v1/users/me.
    :param create_user_response: Ответ API на создание пользователя.
    """
    # Логируем факт начала проверки
    logger.info("Check get user response")

    assert_user(actual=get_user_response.user, expected=create_user_response)