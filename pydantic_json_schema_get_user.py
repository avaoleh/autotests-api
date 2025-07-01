# autotests-api/pydantic_json_schema_get_user.py

from clients.users.public_users_client import get_public_users_client, CreateUserRequestSchema
from clients.users.private_users_client import get_private_users_client, GetUserResponseSchema
from clients.private_http_builder import AuthenticationUserSchema

# Импортируем функцию валидации из tools
from tools.assertions.schema import validate_json_schema

from tools.fakers import fake

# Шаг 1: Создаем пользователя
public_users_client = get_public_users_client()

create_user_request = CreateUserRequestSchema(
    email=fake.email(),
    password="string",
    last_name="string",
    first_name="string",
    middle_name="string"
)

create_user_response = public_users_client.create_user(create_user_request)
print("Создан пользователь:", create_user_response.model_dump())

# Шаг 2: Авторизуемся под созданным пользователем
auth_user = AuthenticationUserSchema(
    email=create_user_request.email,
    password=create_user_request.password
)
private_users_client = get_private_users_client(auth_user)

# Шаг 3: Получаем данные о пользователе по ID
user_id = create_user_response.user.id
response = private_users_client.get_user_api(user_id)

user_data = response.json()
print("Получены данные о пользователе:", user_data)

# Шаг 4: Генерируем JSON Schema из модели GetUserResponseSchema
schema = GetUserResponseSchema.model_json_schema()

# Шаг 5: Провалидируем ответ от API
try:
    validate_json_schema(instance=user_data, schema=schema)
    print("Ответ соответствует ожидаемой схеме")
except AssertionError as e:
    print(f"Ошибка валидации: {e}")
    raise

