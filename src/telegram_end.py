from config import LocalTelegramClient as Client, channel_id
from config import events, logging

import shutil

def save(file_path):
    shutil.move(file_path, "./media/")

@Client.on(events.NewMessage)
async def message_event_handler(event):
    logging.info("telegram: Message handler was called")
    logging.info("telegram: Chat Id: " + str(event.chat_id))
    logging.info("telegram: Local Chat Id: " + str(channel_id))
    if int(channel_id) == event.chat_id:
        media = event.file
        path = None
        if media is not None:
            path = await event.download_media()
            logging.info("telegram: Downloaded media file at : " + path)
            save(path)
        item = [event.raw_text, path]
        logging.info("telegram: %s", event.raw_text)

async def telegram_main():
    me = await Client.get_me()
    logging.info("telegram: Telegram User information: %s", me.stringify())

    username = me.username
    logging.info("telegram: %s", username)
    logging.info("telegram: %s", me.phone)

    async for dialog in Client.iter_dialogs():
        string = dialog.name + ' has ID ' + str(dialog.id)
        logging.info("telegram: %s", string)
    
    await Client.run_until_disconnected()