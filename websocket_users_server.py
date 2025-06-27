# websocket_users_server.py

import asyncio
import websockets

async def handle_connection(websocket: websockets.ServerConnection):
    print("Новое подключение от клиента")
    try:
        async for message in websocket:
            message_str = message.decode() if isinstance(message, bytes) else message
            print(f"Получено сообщение от пользователя: {message_str}")

            # Отправляем 5 ответных сообщений
            for i in range(1, 6):
                response = f"{i} Сообщение пользователя: {message_str}"
                await websocket.send(response)
    except websockets.exceptions.ConnectionClosed:
        print("Клиент отключился")

async def start_server():
    async with websockets.serve(handle_connection, "localhost", 8765):
        print("WebSocket-сервер запущен на ws://localhost:8765")
        await asyncio.Future()  # бессрочный цикл ожидания подключений

if __name__ == "__main__":
    asyncio.run(start_server())