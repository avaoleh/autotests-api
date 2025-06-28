import httpx

# Константы
BASE_URL = "http://localhost:8000"
LOGIN_ENDPOINT = "/api/v1/authentication/login"
USER_ME_ENDPOINT = "/api/v1/users/me"

# Учетные данные пользователя
AUTH_PAYLOAD = {
    "email": "user@user.com",  # Замените на актуальные данные
    "password": "user_test"
}

def get_access_token():
    """
    Выполняет вход в систему и возвращает accessToken.
    """
    login_url = BASE_URL + LOGIN_ENDPOINT

    with httpx.Client() as client:
        response = client.post(login_url, json=AUTH_PAYLOAD)

    if response.status_code == 200:
        try:
            return response.json()["token"]["accessToken"]
        except KeyError:
            raise KeyError("Ответ не содержит 'token' или 'accessToken'")
    else:
        raise Exception(f"Ошибка авторизации. Статус код: {response.status_code}, Ответ: {response.text}")


def get_user_info(access_token):
    """
    Получает информацию о текущем пользователе с использованием access токена.
    """
    user_me_url = BASE_URL + USER_ME_ENDPOINT

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    with httpx.Client() as client:
        response = client.get(user_me_url, headers=headers)

    return response.json(), response.status_code


def main():
    try:
        # Шаг 1: Получить accessToken
        access_token = get_access_token()
        print("Авторизация успешна. AccessToken получен.")

        # Шаг 2: Получить информацию о пользователе
        user_data, status_code = get_user_info(access_token)

        # Шаг 3: Вывести результат
        print("Ответ от /users/me:")
        print(user_data)
        print("Статус код:", status_code)

    except Exception as e:
        print("Ошибка выполнения:", str(e))


if __name__ == "__main__":
    main()