import socket
import selectors

# select - системная функция для мониторинга состояния файловых объектов
# Файловый объект - это любой объект, у которого есть метод .fileno() - возвращает файловый дескриптор ( номер файла)


selector = selectors.DefaultSelector()


def server():
    # AF_INET - ip протокол 4й версии, SOCK_STREAM - поддержка tcp
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Чтобы повторно можно было использовать тот же номер сокета (после сбоя итд.)-> необходимо определить опции
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Укажем к какому домему и порту мы привяжем опции
    server_socket.bind(("localhost", 5001))
    # Скажем сокету проверять входящий буффер наналичие подключений
    server_socket.listen(1)
    # Регистрация сокета
    selector.register(fileobj=server_socket, events=selectors.EVENT_READ, data=accept_connection)
    # Тут регистрируется сокет и связанная с ним функция


def accept_connection(server_socket):
    # Читает данные их входящего буффера и ищет подключения
    client_socket, addr = server_socket.accept()
    print("Connection from", addr)
    # Регистрация сокета
    selector.register(fileobj=client_socket, events=selectors.EVENT_READ, data=send_message)


def send_message(client_socket):
    # Сообщение с клиентского сокета. Аргумент - размер сообщения в байтах
    request = client_socket.recv(4096)
    if request:
        # encode - для преобразования строки в байты
        response = "Response!\n".encode()
        client_socket.sendall(response)
    else:
        # Сняли с регистрации перед закрытием
        selector.unregister(client_socket)
        client_socket.close()


def event_loop():
    while True:
        events = selector.select()  # (key, events)
        # key - объект SelectorKey - для связи сокета, ожидаемого события и данных
        # это именованный кортеж

        for key, _ in events:
            callback = key.data  # извлекаем функцию, связанную с сокетом
            callback(key.fileobj)  # fileobj - это сам сокет


if __name__ == "__main__":
    # Инициализация сервера
    server()
    # Запуск ивент лупа
    event_loop()
