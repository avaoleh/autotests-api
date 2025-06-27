import socket

# Создаем список для хранения сообщений
messages = []

# Настройка сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(10)

print("Сервер запущен и ожидает подключений...")

try:
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Пользователь с адресом: {addr} подключился к серверу")

        # Получаем сообщение от клиента
        data = client_socket.recv(1024).decode()
        if data:
            print(f"Пользователь с адресом: {addr} отправил сообщение: {data}")
            messages.append(data)

            # Отправляем всю историю сообщений клиенту
            response = '\n'.join(messages)
            client_socket.send(response.encode())

        client_socket.close()

except KeyboardInterrupt:
    print("\nСервер остановлен.")

finally:
    server_socket.close()