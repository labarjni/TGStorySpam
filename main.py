from telethon import TelegramClient
from telethon import functions, types

import asyncio

import time 
import random

from config import ACCOUNTS, STORY_DELAY_RANGE, STORY_IMAGE, USER_IDS_FILE, GROUP_SIZE_FOR_STORY, FWD_FROM_USERNAME, FWD_STORY_ID

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

async def sleep_account(account, user_id):
    print(f"@{user_id} the user get a spam block and sleep for 24 hours")
    await asyncio.sleep(60 * 60 * 24)

    ACCOUNTS.append(account)
    print(f"@{user_id} available again")

async def main():
    user_n = 0
    account_index = 0
    total_groups = 0

    with open(USER_IDS_FILE, 'r') as file:
        user_ids = file.read().splitlines()

    groups = [user_ids[i:i+GROUP_SIZE_FOR_STORY] for i in range(0, len(user_ids), GROUP_SIZE_FOR_STORY)]

    for group in groups:
        message_n = 0
        index_of_account = account_index % len(ACCOUNTS)
        account_data = ACCOUNTS[index_of_account]

        client = TelegramClient(account_data['session'], account_data['api_id'], account_data['api_hash'])
        await client.start()

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
                print(f"{str(message_n)} message of {str(GROUP_SIZE_FOR_STORY)}")
            except Exception as e:
                delete_user_from_file(USER_IDS_FILE, user_id)

                if 'Too many requests' in e.__str__():
                    await client.send_message("SpamBot", "/start")
                    ACCOUNTS.remove(index_of_account)
                
                    await sleep_account(account_data, user_id)
                    group.clear()

                print(f"An error occurred while processing the user: {e}")

        if len(group) == GROUP_SIZE_FOR_STORY:
            story_message = ' '.join([f'@{user}' for user in group])
            await send_story(client, story_message, account_data['username'])
            print("The story has been sent to users")

        await client.disconnect()

        account_index += 1
        total_groups += 1

        time.sleep(random.randint(STORY_DELAY_RANGE[0], STORY_DELAY_RANGE[1]))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

