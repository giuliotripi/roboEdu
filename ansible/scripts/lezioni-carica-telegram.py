#!/usr/bin/python3

from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeFilename, DocumentAttributeVideo
import sys
import sqlite3
import time
import logging

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
					level=logging.INFO)

# Use your own values from my.telegram.org
api_id = 00000
api_hash = 'XXXXXX'

client = TelegramClient('anon', api_id, api_hash)

if len(sys.argv) == 2 and sys.argv[1] == "login":
	client.start()
	sys.exit(0)

if len(sys.argv) < 6:
	print("Usage: %s filename destinatario corso anno codiceMateria [durata] [thumb]" % sys.argv[0])
	print("Usage: %s login" % sys.argv[0])
	sys.exit(1)

file = sys.argv[1]
destinatario = int(sys.argv[2])
corso = sys.argv[3]
anno = sys.argv[4]
codiceMateria = sys.argv[5]
sendAsFile = True

if len(sys.argv) == 8:
	durata = int(sys.argv[6].split(".")[0])
	thumb = sys.argv[7]
	sendAsFile = False


async def send():
	try:
		f = open("materie.txt", "r")
		materie = {value: key for value, key in map(lambda i: i.strip("\n").split(": "), f.readlines())}
		materia = materie[codiceMateria]
	except (KeyError, FileNotFoundError):
		materia = "altro"

	inviato = False
	while not inviato:
		try:
			info = "#" + materia + " " + corso + " " + anno + " (" + codiceMateria + ")"
			if sendAsFile:
				await client.send_file(destinatario, file, caption=info, force_document=True,
									   attributes=[DocumentAttributeFilename("registrazione.mkv")])
			else:
				await client.send_file(destinatario, file, caption=info, supports_streaming=True,
									   attributes=[DocumentAttributeVideo(durata, 1920, 1080)], thumb=thumb)
			logging.info("Inviato " + file)
			inviato = True
		except sqlite3.OperationalError:  # multiple users are using this db at the same time
			logging.info("In attesa di inviare " + file)
			time.sleep(60)


connesso = False
while not connesso:
	try:
		client.start()
		connesso = True
	except sqlite3.OperationalError:  # multiple users are using this db at the same time
		logging.info("In attesa di inviare " + file)
		time.sleep(60)

client.loop.run_until_complete(send())
