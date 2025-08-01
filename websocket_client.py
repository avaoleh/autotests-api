import asyncio

import websockets


async def client():
    uri = "ws://localhost:8765"  # Адрес сервера
    async with websockets.connect(uri) as websocket:
        message = "Привет, сервер!"  # Сообщение, которое отправит клиент
        print(f"Отправка: {message}")
        await websocket.send(message)  # Отправляем сообщение

        response = await websocket.recv()  # Асинхронно получаем ответ от сервера
        print(f"Ответ от сервера: {response}")  # Логируем полученный ответ

asyncio.run(client())