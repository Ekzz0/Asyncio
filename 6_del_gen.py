# Функция для инициализации корутины
def coroutine(func):
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g

    return inner


class SomeException(Exception):
    pass


# Делегирующий генератор - это тот, который внутри вызывает другой генератор
# Подгенератор - это вызываемый генератор

# Что-то делает внутри
# Внутри subgen находится обработчик исключений
# !!! Нужно иметь условие окончания работы генератора !!!
def subgen():
    while True:
        try:
            message = yield
        except StopIteration:
            print('ku-ku!')
            break
        else:
            print(".....", message)
    return "Returned from subgen()"


# Транслирует то, что делает subgen
@coroutine
def delegator(g):
    # while True:
    #     try:
    #         data = yield
    #         g.send(data)
    #     except SomeException as e:
    #         g.throw(e)
    result = yield from g  # Код выше, но в 1 строку. + инициализация подгенератора как корутины
    print(result)


sg = subgen()
g = delegator(sg)
g.send('ok')
g.throw(StopIteration)
