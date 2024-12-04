# Конфигурация аккаунтов (премиум обязателен) 
# |*| Account Configuration [premium is required]
ACCOUNTS = [
    {
        'api_id': '26364589',
        'api_hash': '1edb4139bfc4aaf3b1db5d57bbe6016f',
        'session': 'account1', # .session file
        'username': 'labarjni'
    }
]

# Диапазон задержек между историями (в секундах) 
# |*| Delay range between stories [in seconds]
STORY_DELAY_RANGE = (600, 900)

# Интервал проверки спам-блока и сна в случае ограничений (в минутах)
# |*| The interval for checking the spam block and sleep in case of restrictions [in minutes]
SPAM_BLOCK_DELAY = 3
 
# Количество отметок для отправки истории (рекомендуется 5) 
# |*| The number of mentions to send the story [recommended 5]
GROUP_SIZE_FOR_STORY = 5

# Айди пользователя, чью историю пересылаем (необязательно)
# |*| Username of the user whose story we are forwarding [optional]
FWD_FROM_USERNAME = ''

# Айди истории которую пересылаем (необязательно)
# |*| ID of the story that we are forwarding [optional]
FWD_STORY_ID = 1

# Имя файла с вложением для истории 
# |*| The name of the file with the attachment for the story
STORY_IMAGE = 'image.png'

# Имя файла с айди пользователей (с новой строки, без @) 
# |*| File name with user IDs [from a new line, without @]
USER_IDS_FILE = 'users_base.txt'