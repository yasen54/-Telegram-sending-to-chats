from config import USER_NAME_OTS
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.errors.rpcerrorlist import SlowModeWaitError, UserBannedInChannelError, ChatAdminRequiredError, PeerIdInvalidError, ChatRestrictedError, ChannelPrivateError
from telethon.errors.rpcbaseerrors import ForbiddenError


async def gro_pipl(client, phone):
	await client.start(phone)
	dialogs = await client.get_dialogs()
	for dialog in dialogs:
		try:
			if dialog.is_group:
				entity = dialog.entity
				if hasattr(entity, 'username') and entity.username:
					users = await client.get_participants(dialog.id, aggressive=True)
					if len(users) < 1000:
						await client(LeaveChannelRequest(dialog.id))
					print(f"{entity.username} {len(users)}")
		except UserBannedInChannelError as e:
			pass
		except ChatAdminRequiredError as e:
			pass
		except PeerIdInvalidError as e:
			pass
		except ForbiddenError as e:
			pass
		except SlowModeWaitError as e:
			pass
		except ChatRestrictedError as e:
			pass
		except ChannelPrivateError as e:
			pass
	await client.send_message(USER_NAME_OTS, 'Проверка групп завершена')
