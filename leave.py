from telethon.tl.functions.channels import LeaveChannelRequest
from config import USER_NAME_OTS


async def leave_groups(client, phone):
	await client.start(phone)
	dialogs = await client.get_dialogs()
	for dialog in dialogs:
		if dialog.is_group or dialog.is_channel:
			try:
				await client(LeaveChannelRequest(dialog.entity))
				print(f"Вышел из чата: {dialog.name}")
			except Exception as e:
				print(f"Ошибка - {dialog.name}: {e}")
	await client.send_message(USER_NAME_OTS, 'Выход из групп завершон')