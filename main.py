import os
import random
import yaml
import time
import pytz
from datetime import datetime

from vk_messages import MessagesAPI
from vk_messages.utils import get_random

# config
with open('config.yaml', encoding='utf-8') as f:
    config = yaml.safe_load(f)

LOGIN = config['VK']['LOGIN']
PASSWORD = config['VK']['PASSWORD']

USER_ID = config['VK']['USER_ID']  # person's id who should get messages

DELAY = float(config['DELAY'])  # Interval between sending messages (hours)
DELAY_VARIATION = int(config['DELAY_VARIATION'])

TZ = pytz.timezone(config['TZ'])  # Time zone

START_TIME = config['START_TIME']

MESSAGE_FILE = config['MESSAGE_FILE']

SESSIONS_DIR = 'sessions/'

# creating  directory for sessions
if not os.path.exists(SESSIONS_DIR):
    os.mkdir(SESSIONS_DIR)

# authorization
messages = MessagesAPI(login=LOGIN, password=PASSWORD, cookies_save_path=SESSIONS_DIR)


def send_message(message, user_id=USER_ID, domain=USER_ID):
    try:
        if user_id.isdigit():
            messages.method('messages.send', user_id=user_id, message=message,
                            random_id=get_random())

        else:
            messages.method('messages.send', domain=domain, message=message,
                            random_id=get_random())
        print(f'The message is sent: {message}')
    except Exception as e:
        print(f'\033[31mError: {e}\033[0m')


def send_attachment(attachment, user_id=USER_ID, domain=USER_ID):
    try:
        if user_id.isdigit():
            messages.method('messages.send', user_id=user_id,
                            attachment=attachment, random_id=get_random())

        else:
            messages.method('messages.send', domain=domain,
                            attachment=attachment, random_id=get_random())
        print(f'The photo is sent: "{attachment}"')
    except Exception as e:
        print(f'\033[31mError: {e}\033[0m')


# read all messages from a file
with open(MESSAGE_FILE, 'r', encoding='utf8') as file:
    content = file.read().split('-------')

# waiting for the start time
start_time = datetime(START_TIME['year'], START_TIME['month'], START_TIME['day'],
                      START_TIME['hour'], START_TIME['minute'])
print('Waiting for the start time:', start_time)
while True:
    time_now = datetime.now(tz=TZ)
    if time_now.day == start_time.day:
        if time_now.hour >= start_time.hour:
            if time_now.minute >= start_time.minute:
                print('The script is running...\n')
                break

# send the messages with delay
for message in content:
    print(datetime.now(tz=TZ))
    # search and send photo
    if '%%' in message:
        message = message.split('%%')
        photo = message[1]
        message = message[-1]
        send_message(message=message)
        send_attachment(attachment=photo)
    # send only text
    else:
        send_message(message=message)
    print('==============================')

    random_delay = random.randint(-DELAY_VARIATION, DELAY_VARIATION)  # plus or minus minutes to the delay time
    delay = (DELAY * 60 * 60 + random_delay * 60)  # interval between sending messages
    time.sleep(delay)

print(datetime.now(tz=TZ))
print('All the messages have been sent')
