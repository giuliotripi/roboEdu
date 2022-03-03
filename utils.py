#!/usr/bin/python3

from telethon import TelegramClient, utils
from telethon.tl.types import User
import sys


async def list_dialogs(filter: str):
	me: User = await client.get_me()
	print("Il tuo ID utente è: " + str(me.id))
	async for dialog in client.iter_dialogs():
		if filter.lower() in dialog.name.lower():
			print(dialog.name, ":", utils.get_peer_id(dialog.entity))

try:
	f = open("secrets/telegram_api.yml", "r")
	info = {key.strip(" "): value.strip("\"' ") for key, value in map(lambda i: i.strip("\n").split(":"), f.readlines())}
	api_id = info["api_id"]
	api_hash = info["api_hash"]
	client = TelegramClient('anon', api_id, api_hash)
	client.start()
	if len(sys.argv) > 1:
		client.loop.run_until_complete(list_dialogs(" ".join(sys.argv[1:])))
except FileNotFoundError:
	print("File secrets/telegram_api.yml non trovato")
except KeyError:
	print("Il file secrets/telegram_api.yml non contiene i parametri richiesti")
