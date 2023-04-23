#!/usr/bin/python3

import os
import sys

# Using the Telethon telegram api
import configparser
from telethon.sync import TelegramClient, events
from telethon.errors import SessionPasswordNeededError

# Accessing files in directories
if getattr(sys, 'frozen', False):
    # running in a bundled form
    base_dir = sys._MEIPASS # pylint: disable=no-member
else:
    # running normally
    base_dir = os.path.dirname(os.path.abspath(__file__))

# Locating helper files in the current working directory
config_file_path = os.path.join(base_dir, 'config.ini')

# Reading the configs
config = configparser.ConfigParser()
config.read(config_file_path)

# Then setting our config values
app_name = config['Telegram']['app_name']
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
api_hash = str(api_hash)
bot_token = config['Telegram']['bot_token']

phone_no = config['Telegram']['phone_no']
username = config['Telegram']['username']

source_group_invite_link = config['Telegram']['s_tg_group_link']
source_group_invite_link = str(source_group_invite_link)

destination_group_invite_link = config['Telegram']['tg_group_link']
destination_group_invite_link = str(destination_group_invite_link)

# Create the client and connect
client = TelegramClient(username, api_id, api_hash)
client.start()
print("Client Created")
# Ensure you're authorized
if not client.is_user_authorized():
    client.send_code_request(phone_no)
    try:
        client.sign_in(phone_no, input('Enter the code: '))
    except SessionPasswordNeededError:
        client.sign_in(password=input('Password: '))


print('Connection successfull!')

# *******************************************************************************************
# *******************************************************************************************
# *******************************************************************************************

# Listen to msgs in your telegram account and forward message to group(s)
dest_group=client.get_entity(destination_group_invite_link)
source_group=client.get_entity(source_group_invite_link)

@client.on(events.NewMessage(incoming=True,pattern='.*facebook.com.*',chats=source_group))
async def my_event_handler(event):
    await client.send_message(entity=dest_group,message=event.message)
    os.system('notify-send -t 150000 -i dialog-information "Каритас" "Сообщение с facebook"')
    print('Msg forwarded successfully!')


client.start()
client.run_until_disconnected()
