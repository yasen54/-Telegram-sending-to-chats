import time
from telethon.errors.rpcerrorlist import SlowModeWaitError, UserBannedInChannelError, ChatAdminRequiredError, PeerIdInvalidError, ChatRestrictedError, ChannelPrivateError
from telethon.errors.rpcbaseerrors import ForbiddenError
from telethon.tl.functions.channels import LeaveChannelRequest
from config import GROOP_FROM_MESSAGE, TIME_SPAM_PAUSE


async def get_last_message(client):
	try:
		async for message in client.iter_messages(GROOP_FROM_MESSAGE, limit=1):
			return message.id
	except ConnectionError as e:
		print(f"An error occurred: {e}")


async def activ_gro(client, chat):
	try:
		mes = await get_last_message(client=client)
		await client.forward_messages(entity=chat, messages=mes, from_peer=GROOP_FROM_MESSAGE)
		return True
	except UserBannedInChannelError as e:
		return False
	except ChatAdminRequiredError as e:
		return False
	except PeerIdInvalidError as e:
		await client(LeaveChannelRequest(chat))
		return False
	except ForbiddenError as e:
		return False
	except SlowModeWaitError as e:
		return True
	except ChatRestrictedError as e:
		return False
	except ChannelPrivateError as e:
		return False


async def gro_spam(client, phone):
	await client.start(phone)
	while True:
		dialogs = await client.get_dialogs()
		a = 1
		a1 = 1
		a2 = 1
		false_lists = []
		true_lists = []
		for dialog in dialogs:
			try:
				if dialog.is_group:
					entity = dialog.entity
					if hasattr(entity, 'username') and entity.username:
						current_time = time.strftime("%H:%M:%S", time.localtime())
						a += 1
						if await activ_gro(client=client, chat=dialog.id):
							true_lists.append(f"https://t.me/{str(entity.username)}")
							a1 += 1
							print(f"{a} {current_time} {entity.username}: {dialog.id} true")
						else:
							false_lists.append(f"https://t.me/{str(entity.username)}")
							a2 += 1
							print(f"{a} {current_time} {entity.username}: {dialog.id} false")
			except UserBannedInChannelError as e:
				pass
			except ChatAdminRequiredError as e:
				pass
			except PeerIdInvalidError as e:
				pass
			except ForbiddenError as e:
				pass
			except ChannelPrivateError as e:
				pass
		false_lists.clear()
		if a1 < 100:
			await client.send_message("SpamBot", '/start')
		current = time.strftime("%H:%M:%S", time.localtime())
		print(f"{current} Всего групп: {a} True: {a1} false: {a2}\nЧерез {TIME_SPAM_PAUSE/60} минут рассылка повториться")
		time.sleep(TIME_SPAM_PAUSE)


def text_create(data, data1):
	with open('false_gro_spam.txt', 'wb'):
		pass
	with open('true_gro_spam.txt', 'wb'):
		pass
	with open('false_gro_spam.txt', 'a', encoding="utf-8") as text_file:
		for link in data:
			text_file.write(link + "\n")
	with open('true_gro_spam.txt', 'a', encoding="utf-8") as text_file:
		for link in data1:
			text_file.write(link + "\n")