import asyncio
import telethon
from telethon.errors import ChatAdminRequiredError
from telethon.tl.functions.channels import JoinChannelRequest
from config import USER_NAME_OTS


async def join_chat(client, chat_link, phone):
	try:
		await client.start(phone)
		await client(JoinChannelRequest(chat_link))
		print(f"Успешно присоединено к: {chat_link}")
	except ChatAdminRequiredError as e:
		print(f"Ошибка: {str(e)}. Ожидание {e.seconds} сек.")
		await asyncio.sleep(e.seconds)
		await join_chat(chat_link=chat_link, client=client, phone=phone)
	except telethon.errors.rpcerrorlist.UsernameNotOccupiedError as e:
		print(f"Ошибка: {str(e)}. Ссылка занесина в false_gro.txt")
		remove_chat_from_file(chat_link)
	except Exception as e:
		if "A wait of" in str(e) and "seconds is required" in str(e):
			wait_time = int(str(e).split("A wait of")[1].split("seconds")[0].strip())
			print(f"Необходимо подождать {wait_time} секунд")
			await asyncio.sleep(wait_time)
			await join_chat(chat_link=chat_link, client=client, phone=phone)
		elif "No user has" in str(e) and "as username" in str(e):
			print(f"Ошибка: {str(e)}. Удаление ссылки из файла...")
			remove_chat_from_file(chat_link)
		elif "The channel specified is private" in str(e):
			print(f"Ошибка: {str(e)}. Удаление ссылки из файла...")
			remove_chat_from_file(chat_link)
		elif "Nobody is using this username" in str(e):
			print(f"Ошибка c {chat_link}: {str(e)}. Удаление ссылки из файла...")
			remove_chat_from_file(chat_link)


def remove_chat_from_file(chat_link):
	with open('false_gro.txt', 'a', encoding="utf-8") as text_file:
		text_file.write(str(chat_link) + "\n")


async def gro_join(client, phone):
	with open("groop.txt", "r") as file:
		for groop in file:
			gro = groop.strip()
			await join_chat(chat_link=gro, client=client, phone=phone)
		await client.send_message(USER_NAME_OTS, 'Вход в группы завершон')
