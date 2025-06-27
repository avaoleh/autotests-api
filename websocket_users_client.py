# websocket_users_client.py

import asyncio
import websockets

async def connect_to_server():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        print("Подключение к серверу установлено")
        message = "Привет, сервер!"
        await websocket.send(message)
        print(f"Сообщение отправлено: {message}")

        # Получаем 5 ответов от сервера
        for _ in range(5):
            response = await websocket.recv()
            print(f"Получено от сервера: {response}")

asyncio.run(connect_to_server())