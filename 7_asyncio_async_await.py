import asyncio
from time import time


# Функция считает числа
# @asyncio.coroutine - больше не используется
async def print_nums():
    num = 0

    while True:
        print(num)
        num += 1
        await asyncio.sleep(1)


# Функция считает время
# @asyncio.coroutine - больше не используется
async def print_time():
    count = 0

    while True:
        if count % 3 == 0:
            print("{} seconds have passed".format(count))
        count += 1
        await asyncio.sleep(1)


# Свяжем все функции в событийный цикл
# @asyncio.coroutine - больше не используется
async def main():
    # Обернем все функции в экземпляры класса Task и поставить в очередь событийного цикла
    task_1 = asyncio.create_task(print_nums())
    task_2 = asyncio.create_task(print_time())
    # Теперь нужно дождаться их выполнения
    await asyncio.gather(task_1, task_2)


if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()
    asyncio.run(main())
