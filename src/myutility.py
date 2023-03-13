from config import channels, logging
from io import TextIOWrapper
import json5

def add_channel(tgch: str, dsch: int) -> None:
  channels[dsch] = tgch
  logging.info("discord: added telegram id {} and discord id {} in memory.".format(tgch, dsch))

def save_channels() -> None:
  channels_file: TextIOWrapper =  open("channels.json", "w", encoding="utf-8")
  try:
    json5.dump(channels, channels_file)
  except TypeError:
    logging.info("discord: unable to save channels as JSON locally.")
    raise TypeError
  logging.info("discord: successfully saved channels as JSON locally.")
  channels.clear()
  channels_file.close()

def load_channels() -> None:
  if channels_file.closed != True:
    channels_file.close()
  channels_file = open("channels.json", "r", encoding="utf-8")
  try: 
    channels = json5.load(channels)
  except ValueError:
    logging.info("Loading channels.json failed, ValueError exception, is the format correct?")
  channels_file.close()