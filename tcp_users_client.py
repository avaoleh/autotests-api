import socket

# Настройка клиента
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

# Отправляем сообщение серверу
message = "Привет, сервер!"
client_socket.send(message.encode())

# Получаем ответ от сервера
response = client_socket.recv(1024).decode()
print(response)

# Закрываем соединение
client_socket.close()