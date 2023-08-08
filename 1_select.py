import socket

# domain: 5000

# AF_INET - ip протокол 4й версии, SOCK_STREAM - поддержка tcp
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Чтобы повторно можно было использовать тот же номер сокета (после сбоя итд.)-> необходимо определить опции
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Укажем к какому домему и порту мы привяжем опции
server_socket.bind(("localhost", 5001))
# Скажем сокету проверять входящий буффер наналичие подключений
server_socket.listen(1)


def accept_connection(server_socket):
    # Цикл с отношениями клиент-сервер
    while True:
        # Читает данные их входящего буффера и ищет подключения
        client_socket, addr = server_socket.accept()
        print("Connection from", addr)
        send_message(client_socket)


def send_message(client_socket):
    while True:
        # Сообщение с клиентского сокета. Аргумент - размер сообщения в байтах
        print("Сервер ждет сообщение")
        request = client_socket.recv(4096)
        print(f'Получено: {request.decode()}')
        if not request:
            break
        else:
            # encode - для преобразования строки в байты
            response = "Response!\n".encode()
            client_socket.sendall(response)

    client_socket.close()


if __name__ == "__main__":
    accept_connection(server_socket)
