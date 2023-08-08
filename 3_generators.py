from time import time

# генерация рандомного имени файла
def gen_filename():
    while True:
        pattern = 'file{}.jpeg'
        t= time() * 1000 # 1000 чтобы перевести в мс
        yield pattern.format(t)

def gen1(s):
    for i in s:
        yield i

def gen2(n):
    for i in range(n):
        yield i

g1 = gen1('semen')
g2 = gen2(3)

tasks = [g1, g2]

# Принцип Round Robin
while tasks:
    # Формируем задачу - 1й элемент из списка задач
    task = tasks.pop(0)

    try:
        # Обрабатываем задачу
        i = next(task)
        print(i)
        tasks.append(task)
    except StopIteration:
        # Если генератор закончился -> пропускаем все
        pass





