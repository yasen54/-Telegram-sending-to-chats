from telethon import TelegramClient
from config import *
from join import gro_join
from leave import leave_groups
from chek_pipel_goop import gro_pipl
import logging
from spam import gro_spam


logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)
api_id = API_ID
api_hash = API_HASH
phone = PHONE
client = TelegramClient('anon', api_id, api_hash)


async def main():
    while True:
        print("1 - Запустить спамер\n2 - Входить в групп из groop.txt\n3 - Выйте из всех групп на акаунте\n4 - Выйте из групп где меньше 1000 участников")
        inputs = int(input("Выберите действия - "))
        if inputs == 1:
            await gro_spam(client=client, phone=phone)
        if inputs == 2:
            await gro_join(client=client, phone=phone)
        if inputs == 3:
            await leave_groups(client=client, phone=phone)
        if inputs == 4:
            await gro_pipl(client=client, phone=phone)
        if inputs == 100:
            return False
        else:
            print(inputs, "-неверная команда")


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())


