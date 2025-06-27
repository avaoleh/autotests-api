import asyncio  # Импортируем asyncio для работы с асинхронными операциями

import websockets  # Импортируем библиотеку для работы с WebSockets
from websockets import ServerConnection


# Обработчик входящих сообщений
async def echo(websocket: websockets.ServerConnection):
    async for message in websocket:  # Асинхронно обрабатываем входящие сообщения
        print(f"Получено сообщение: {message}")  # Логируем полученное сообщение

        response = f"Сервер получил: {message}"  # Формируем ответное сообщение
        await websocket.send(response)  # Отправляем ответ клиенту


# Запуск WebSocket-сервера на порту 8765
async def main():
    server = await websockets.serve(echo, "localhost", 8765)  # Запускаем сервер
    print("WebSocket сервер запущен на ws://localhost:8765")  # Выводим сообщение о запуске

    await server.wait_closed()  # Ожидаем закрытия сервера (обычно он работает вечно)



asyncio.run(main())  # Запускаем асинхронный код
