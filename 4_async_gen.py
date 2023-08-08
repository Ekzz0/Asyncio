import socket
from select import select

# domain: 5000


# Алгоритм предложил David Beazley
# Конкурентность в питоне с нуля в живую - на русском.
tasks = []  # по-хорошему нужно использовать очередь

to_read = {}
to_write = {}


def server():
    # AF_INET - ip протокол 4й версии, SOCK_STREAM - поддержка tcp
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Чтобы повторно можно было использовать тот же номер сокета (после сбоя итд.)-> необходимо определить опции
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Укажем к какому домему и порту мы привяжем опции
    server_socket.bind(("localhost", 5001))
    # Скажем сокету проверять входящий буффер наналичие подключений
    server_socket.listen(1)

    # Цикл с отношениями клиент-сервер
    while True:
        yield ('read', server_socket)  # пометка для чего сокет используется

        # Читает данные их входящего буффера и ищет подключения
        client_socket, addr = server_socket.accept()  # read
        print("Connection from", addr)
        tasks.append(client(client_socket))


def client(client_socket):
    while True:
        # Сообщение с клиентского сокета. Аргумент - размер сообщения в байтах
        yield ('read', client_socket)

        request = client_socket.recv(4096)  # read
        if request:
            # encode - для преобразования строки в байты
            response = "Response!\n".encode()

            yield ('write', client_socket)

            client_socket.sendall(response)  # write
        else:
            break
    client_socket.close()


def event_loop():
    # Если хоть один словарь полный -> будет True. Если все пустые -> False
    while any(
            [tasks, to_read, to_write]):  # any() принимает список значений, каждое из которых должно быть false or true

        # Заполнение tasks новыми заданиями
        while not tasks:  # Работает только если tasks - пустой
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])  # Тут она забирает ключи - т.е сокеты

            for s in ready_to_read:
                tasks.append(to_read.pop(s))  # Получаем значение по ключу s

            for s in ready_to_write:
                tasks.append(to_write.pop(s))  # Получаем значение по ключу s

        try:
            task = tasks.pop(0)  # В task лежит генератор
            reason, s = next(task)  # yield ('reason', socket)

            if reason == 'read':
                to_read[s] = task
            elif reason == 'write':
                to_write[s] = task

        except StopIteration:
            print('Done!')


if __name__ == "__main__":
    tasks.append(server())
    event_loop()
