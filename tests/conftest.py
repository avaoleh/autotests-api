import pytest  # Импортируем pytest
from pydantic import BaseModel, EmailStr

# Импортируем API клиенты
from clients.authentication.authentication_client import AuthenticationClient, get_authentication_client
from clients.users.public_users_client import get_public_users_client, PublicUsersClient
from clients.users.private_users_client import get_private_users_client, PrivateUsersClient

# Импортируем запрос и ответ создания пользователя, модель данных пользователя
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, UserSchema
from clients.users.private_users_client import AuthenticationUserSchema

# Модель для агрегации возвращаемых данных фикстурой function_user
class UserFixture(BaseModel):
    request: CreateUserRequestSchema
    response: CreateUserResponseSchema

    @property
    def email(self) -> EmailStr:  # Быстрый доступ к email пользователя
        return self.request.email

    @property
    def password(self) -> str:  # Быстрый доступ к password пользователя
        return self.request.password

    @property
    def authentication_user(self) -> AuthenticationUserSchema:
        """
        Возвращает объект для аутентификации API-клиента.
        Используется в билдерах вроде private_http_builder
        """
        return AuthenticationUserSchema(email=self.email, password=self.password)

@pytest.fixture  # Объявляем фикстуру, по умолчанию скоуп function, то что нам нужно
def authentication_client() -> AuthenticationClient:  # Аннотируем возвращаемое фикстурой значение
    # Создаем новый API клиент для работы с аутентификацией
    return get_authentication_client()


@pytest.fixture  # Объявляем фикстуру, по умолчанию скоуп function, то что нам нужно
def public_users_client() -> PublicUsersClient:  # Аннотируем возвращаемое фикстурой значение
    # Создаем новый API клиент для работы с публичным API пользователей
    return get_public_users_client()

@pytest.fixture
def private_users_client(function_user: UserFixture) -> PrivateUsersClient:
    """
    Возвращает инициализированный клиент для приватных эндпоинтов пользователей.
    Аутентифицируется под созданным пользователем.
    """
    return get_private_users_client(user=function_user.authentication_user)

# Фикстура для создания пользователя
@pytest.fixture
# Используем фикстуру public_users_client, которая создает нужный API клиент
def function_user(public_users_client: PublicUsersClient) -> UserFixture:
    request = CreateUserRequestSchema()
    response = public_users_client.create_user(request)
    return UserFixture(request=request, response=response)  # Возвращаем все нужные данные