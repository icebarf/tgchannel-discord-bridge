from config import logging
import config
from io import TextIOWrapper
import json5

filename: str = "channels.json"


def get_file(name, mode) -> TextIOWrapper:
    try:
        file = open(name, mode, encoding="utf-8")
    except IOError:
        logging.error(
            "discord: Unable to open {} in mode {}".format(name, mode))
        raise IOError
    logging.info("discord: opened file {} in mode {}".format(name, mode))
    return file


def add_channel(tgch: list, dsch: int) -> None:
    config.channels[dsch] = tgch
    logging.info(
        "discord: added telegram id {} and discord id {} in memory.".format(tgch, dsch))


def save_channels() -> None:
    channels_file = get_file(filename, "w")
    try:
        json5.dump(config.channels, channels_file)
    except TypeError:
        logging.error("discord: unable to save channels as JSON locally.")
        channels_file.close()
        raise TypeError
    logging.info("discord: successfully saved channels as JSON locally.")
    config.channels.clear()
    channels_file.close()


def dump_channels() -> str:
    channels_file = get_file(filename, "r")
    raw_json = channels_file.read()
    channels_file.close()
    return raw_json


def load_channels() -> None:
    channels_file = open(filename, "r", encoding="utf-8")
    config.channels = json5.load(channels_file)
    logging.info("discord: Loading channels.json successful")
    logging.info("discord: loaded data: {}".format(config.channels))
    channels_file.close()
    if not isinstance(config.channels, dict):
        raise TypeError("JSON loader did not return a dictionary")
