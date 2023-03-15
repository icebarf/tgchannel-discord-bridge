# myutility.py - a bunch of utility functions for discord_cogs.py to work
# Copyright (C) 2023 Amritpal Singh
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from config import logging
from io import TextIOWrapper
import config
import json5
import os

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
    logging.info("discord: closed file {}".format(filename))


def dump_channels() -> str:
    channels_file = get_file(filename, "r")
    raw_json = channels_file.read()
    channels_file.close()
    logging.info("discord: closed file {}".format(filename))
    return raw_json


def load_channels() -> None:
    channels_file = open(filename, "r", encoding="utf-8")
    config.channels = json5.load(channels_file)
    logging.info("discord: Loading channels.json successful")
    logging.info("discord: loaded data: {}".format(config.channels))
    channels_file.close()
    if not isinstance(config.channels, dict):
        raise TypeError("JSON loader did not return a dictionary")


def convert_to_mp4(file: str) -> str:
    i: int = file.rfind(".")
    output = file[:i] + ".mp4"
    # (
    #     ffmpeg
    #     .input(file)
    #     .output(output, codec='copy')
    #     .run()
    # )
    # return output
    os.system('ffmpeg -i {} -codec copy {}'.format(file, output))
    return output
