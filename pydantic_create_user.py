import uuid
from pydantic import BaseModel, Field, EmailStr, HttpUrl, ValidationError


# Модель данных пользователя
class UserSchema(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")

    def get_username(self) -> str:
        return f"{self.first_name} {self.last_name}"


# Модель запроса на создание пользователя
class CreateUserRequestSchema(BaseModel):
    email: EmailStr
    password: str
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")


# Модель ответа с данными созданного пользователя
class CreateUserResponseSchema(BaseModel):
    user: UserSchema


# === Примеры использования ===

# --- 1. Инициализация через передачу аргументов ---
user_example = UserSchema(
    id="user-123",
    email="john.doe@example.com",
    lastName="Doe",
    firstName="John",
    middleName="A."
)
print("User model:", user_example)


# --- 2. Инициализация из словаря ---
user_dict = {
    "id": "user-456",
    "email": "jane.smith@example.com",
    "lastName": "Smith",
    "firstName": "Jane",
    "middleName": "M."
}
user_from_dict = UserSchema(**user_dict)
print("User from dict:", user_from_dict)


# --- 3. Инициализация запроса на создание пользователя ---
create_user_request = CreateUserRequestSchema(
    email="new.user@example.com",
    password="securepassword123",
    lastName="Bond",
    firstName="James",
    middleName="T."
)
print("CreateUserRequestSchema:", create_user_request)


# --- 4. Инициализация ответа от API ---
create_user_response = CreateUserResponseSchema(user=user_from_dict)
print("CreateUserResponseSchema:", create_user_response)


# --- 5. Валидация JSON ---
import json

json_data = '''
{
    "user": {
        "id": "user-789",
        "email": "valid.email@example.com",
        "lastName": "Last",
        "firstName": "First",
        "middleName": "Middle"
    }
}
'''

try:
    data = json.loads(json_data)
    response_model = CreateUserResponseSchema(**data)
    print("JSON validated model:", response_model)
except ValidationError as error:
    print("Validation error:", error)


# --- 6. Обработка ошибочной валидации ---
invalid_json_data = '''
{
    "user": {
        "id": "user-789",
        "email": "not-an-email",
        "lastName": "Last",
        "firstName": "First",
        "middleName": "Middle"
    }
}
'''

try:
    data = json.loads(invalid_json_data)
    response_model = CreateUserResponseSchema(**data)
    print("Invalid model:", response_model)
except ValidationError as error:
    print("Validation errors:")
    print(error.errors())
except json.JSONDecodeError as je:
    print("JSON decoding error:", je)