# Функция для инициализации корутины
def coroutine(func):
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g
    return inner


def subgen():
    x = "ready"
    message = yield x
    print("Получили", message)


class SomeException(Exception):
    pass


@coroutine
def average():
    count = 0
    summ = 0
    average_x = None

    while True:
        try:
            x = yield average_x
        except StopIteration:
            print("Done!")
        except SomeException:
            print("SomeException!")
        else:
            count += 1
            summ += x
            average_x = round(summ / count, 2)
    # Чтобы получить это значение - нужно обратиться к исключению StopIteration
    # и обратиться к его свойству value
    return average_x


g = average()
print(g.send(2))
print(g.send(5))
print(g.send(10))
print(g.throw(StopIteration))  # Передать исключение Корутине
print(g.throw(SomeException))
