from telethon import TelegramClient
from telethon import functions, types

import asyncio
import threading

import logging
import colorlog

import time 
import random

from config import (
    ACCOUNTS,
    STORY_DELAY_RANGE,
    STORY_IMAGE,
    USER_IDS_FILE,
    GROUP_SIZE_FOR_STORY,
    FWD_FROM_USERNAME,
    FWD_STORY_ID,
    SPAM_BLOCK_DELAY
)

logger = colorlog.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
))

file_handler = logging.FileHandler('TGStorySpam.log', mode='a')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger.addHandler(handler)
logger.addHandler(file_handler)


async def send_story(client, msg, username):
    story_request = functions.stories.SendStoryRequest(
        peer=username,
        media=types.InputMediaUploadedPhoto(
            file=await client.upload_file(STORY_IMAGE),
            spoiler=True,
            stickers=[types.InputDocument(
                id=-12398745604826,
                access_hash=-12398745604826,
                file_reference=b'arbitraryx7f data xfa here'
            )],
            ttl_seconds=42
        ),
        privacy_rules=[types.InputPrivacyValueAllowContacts()],
        pinned=True,
        noforwards=True,
        fwd_modified=True,
        media_areas=[types.MediaAreaCoordinates(
            x=7.13,
            y=7.13,
            w=7.13,
            h=7.13,
            rotation=7.13
        )],
        caption=msg,
        period=None
    )

    if FWD_FROM_USERNAME != '':
        story_request.fwd_from_id = FWD_FROM_USERNAME
        story_request.fwd_from_story = FWD_STORY_ID

    await client(story_request)


async def add_contact(client, user_id, user_n):
    await client(functions.contacts.AddContactRequest(
        id=user_id,
        first_name='User',
        last_name=str(user_n),
        phone='+7977777777'
    ))

def delete_user_from_file(filename, user_to_delete):
    with open(filename, 'r') as file:
        users = file.readlines()
    
    with open(filename, 'w') as file:
        for user in users:
            if user.strip() != user_to_delete:
                file.write(user)


def sleep_account(account):
    logger.warning(f"@{account['username']} the user get a spam block and sleep for {str(SPAM_BLOCK_DELAY)} minutes")
    time.sleep(60 * SPAM_BLOCK_DELAY)

    ACCOUNTS.append(account)
    logger.info(f"@{account['username']} available again")


async def process_group(group, account_data, user_n, account_index):
    client = TelegramClient(account_data['session'], account_data['api_id'], account_data['api_hash'])
    await client.start()

    message_n = 0
    spam_block = False

    for user_id in group:
        try:
            await add_contact(client, user_id, user_n)
            time.sleep(2)

            message = await client.send_message(user_id, 'Привет!')
            message_n += 1
            time.sleep(1)

            await message.delete()
            time.sleep(5)

            delete_user_from_file(USER_IDS_FILE, user_id)

            user_n += 1
            logger.debug(f"{str(message_n)} out of {str(GROUP_SIZE_FOR_STORY)} messages in the group has been sent")
        except Exception as e:
            delete_user_from_file(USER_IDS_FILE, user_id)

            if 'Too many requests' in e.__str__():
                await client.send_message("SpamBot", "/start")
                ACCOUNTS.pop(account_index)

                spam_block = True

                threading.Thread(target=sleep_account, args=(account_data,)).start()
                break

            logger.error(f"An error occurred while processing the user: {e}")

    if len(group) == GROUP_SIZE_FOR_STORY and not spam_block:
        story_message = ' '.join([f'@{user}' for user in group])
        await send_story(client, story_message, account_data['username'])
        logger.info("The story has been sent to users")

    await client.disconnect()


async def main():
    print("The script was started successfully, author: Alexander Tyrin, @labarjni")

    user_n = 1
    account_index = 0
    total_groups = 0

    with open(USER_IDS_FILE, 'r') as file:
        user_ids = file.read().splitlines()

    groups = [user_ids[i:i + GROUP_SIZE_FOR_STORY] for i in range(0, len(user_ids), GROUP_SIZE_FOR_STORY)]

    for group in groups:
        while not ACCOUNTS:
            logger.warning("No accounts available, waiting...")
            time.sleep(10)

        account_index = account_index % len(ACCOUNTS)
        account_data = ACCOUNTS[account_index]
        await process_group(group, account_data, user_n, account_index)

        account_index += 1
        total_groups += 1

        time.sleep(random.randint(STORY_DELAY_RANGE[0], STORY_DELAY_RANGE[1]))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

