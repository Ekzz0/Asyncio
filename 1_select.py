import socket
from select import select

# select - системная функция для мониторинга состояния файловых объектов
# Файловый объект - это любой объект, у которого есть метод .fileno() - возвращает файловый дескриптор ( номер файла)


to_monitor = []
to_write = []
errors = []
# AF_INET - ip протокол 4й версии, SOCK_STREAM - поддержка tcp
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Чтобы повторно можно было использовать тот же номер сокета (после сбоя итд.)-> необходимо определить опции
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Укажем к какому домему и порту мы привяжем опции
server_socket.bind(("localhost", 5001))
# Скажем сокету проверять входящий буффер наналичие подключений
server_socket.listen(1)


def accept_connection(server_socket):
    # Читает данные их входящего буффера и ищет подключения
    client_socket, addr = server_socket.accept()
    print("Connection from", addr)

    to_monitor.append(client_socket)


def send_message(client_socket):
    # Сообщение с клиентского сокета. Аргумент - размер сообщения в байтах
    request = client_socket.recv(4096)
    if request:
        # encode - для преобразования строки в байты
        response = "Response!\n".encode()
        client_socket.sendall(response)
    else:
        client_socket.close()


def event_loop():
    while True:
        # Мониторинг сокетов, доступных для чтения
        ready_to_read, ready_to_write, with_errors = select(to_monitor, to_write, errors)
        # Обработаем списки с объектами:

        for s in ready_to_read:
            if s is server_socket:
                accept_connection(s)
            else:
                send_message(s)


if __name__ == "__main__":
    to_monitor.append(server_socket)
    event_loop()
