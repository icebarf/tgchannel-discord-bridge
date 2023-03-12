from config import LocalTelegramClient as Client, telegram_channel_id, message_queue
from config import events, logging
import asyncio

@Client.on(events.NewMessage)
async def message_event_handler(event):
    logging.info("telegram: Message handler was called")
    logging.info("telegram: Chat Id: " + str(event.chat_id))
    logging.info("telegram: Local Chat Id: " + str(telegram_channel_id))
    if int(telegram_channel_id) == event.chat_id:
        media = event.file
        path = None
        if media is not None:
            path = await event.download_media()
            logging.info("telegram: Downloaded media file at : " + path)
        item = [event.text, path]
        await message_queue.put(item)        
        logging.info("telegram: %s", event.text)
        logging.info("telegram: exiting the message_event_handler()")

async def telegram_main():
    me = await Client.get_me()
    logging.info("telegram: Telegram User information: %s", me.stringify())

    username = me.username
    logging.info("telegram: %s", username)
    logging.info("telegram: %s", me.phone)

    async for dialog in Client.iter_dialogs():
        string = dialog.name + ' has ID ' + str(dialog.id)
    logging.info("telegram: %s", string)
        
    while True: 
        await asyncio.sleep(1)