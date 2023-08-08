import requests
from time import time


# Синхронный вариант
def get_file(url):
    r = requests.get(url, allow_redirects=True)
    return r


def write_file(response):
    # Получение имя файла с редиректа
    filename = "simple" + './pictures/' + response.url.split("/")[-1]
    # Запись файла
    with open(filename, 'wb') as file:
        file.write(response.content)  # .content - бинарные данные


def main():
    url = 'https://loremflickr.com/320/240'

    for i in range(10):
        write_file(get_file(url))


# .................................................................................
# Асинхронный вариант
import asyncio  # не работает с протоколм http -> устанавливаем aiohttp
import aiohttp


# Лучше не смешивать синхронный и асинхронный код, но для решаемой задачи подойдет такой вариант
def write_image(data):
    filename = '_async' + './pictures/' + str(int((time() * 1000))) + '.jpeg'
    with open(filename, 'wb') as file:
        file.write(data)  # .content - бинарные данные


async def fetch_content(url, session):
    async with session.get(url, allow_redirects=True) as response:
        data = await response.read()  # read() - возвращает бинарные данные
        write_image(data)


async def main2():
    url = 'https://loremflickr.com/320/240'
    tasks = []
    async with aiohttp.ClientSession() as session:
        for i in range(10):
            task = asyncio.create_task(fetch_content(url, session))
            tasks.append(task)

        # Дождемся результата работа корутин
        await asyncio.gather(*tasks)  # * - распаковка


if __name__ == '__main__':
    t_0 = time()
    main()
    print("синхронный скрипт работал:", time() - t_0)
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main2())
    # loop.close()
    t_0 = time()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main2())
    print("асинхронный скрипт работал:", time() - t_0)

    # asyncio.run(main2())
