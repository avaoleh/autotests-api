import httpx

from tools.fakers import get_random_email

# Создаем пользователя
print("\nСоздаем пользователя")
create_user_payload = {
    "email": get_random_email(),
    "password": "string",
    "lastName": "string",
    "firstName": "string",
    "middleName": "string"
}
create_user_response = httpx.post("http://localhost:8000/api/v1/users", json=create_user_payload)
create_user_response_data = create_user_response.json()
print('Create user data:', create_user_response_data)

# Проходим аутентификацию
print("\nПроходим аутентификацию")
login_payload = {
    "email": create_user_payload['email'],
    "password": create_user_payload['password']
}
login_response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=login_payload)
login_response_data = login_response.json()
print('Login data:', login_response_data)

# Получаем данные пользователя
print("\nПолучаем данные пользователя")
get_user_headers = {
    "Authorization": f"Bearer {login_response_data['token']['accessToken']}"
}
get_user_response = httpx.get(
    f"http://localhost:8000/api/v1/users/{create_user_response_data['user']['id']}",
    headers=get_user_headers
)
get_user_response_data = get_user_response.json()
print('Get user data:', get_user_response_data)


# Обновляем пользователя
print("\nОбновляем пользователя")

# Формируем новую случайную почту с помощью get_random_email()
update_user_payload = {
    "email": get_random_email(),
    "lastName": "Иванов",
    "firstName": "Иван",
    "middleName": "Иванович"
}

# Формируем заголовок с токеном авторизации
update_user_headers = {
    "Authorization": f"Bearer {login_response_data['token']['accessToken']}"
}

# Формируем URL с ID пользователя из ответа создания
update_user_url = f"http://localhost:8000/api/v1/users/{create_user_response_data['user']['id']}"

# Выполняем PATCH-запрос для обновления данных пользователя
update_user_response = httpx.patch(update_user_url, json=update_user_payload, headers=update_user_headers)

# Получаем JSON-ответ
update_user_response_data = update_user_response.json()

# Выводим результат в консоль
print("Ответ от сервера при обновлении пользователя:")
print('Get updated user data:', update_user_response_data)
print("Статус код:", update_user_response.status_code)