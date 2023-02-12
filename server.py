import logging
import os

from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher, executor, types

import tools
from vkLogic import get_vk_session, get_vk_tracks
import yandexMusicLogic as yandex


logging.basicConfig(level=logging.INFO)

load_dotenv(find_dotenv('config.env'))
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
VK_BOT_LOGIN = os.getenv('VK_BOT_LOGIN')
VK_BOT_PASSWORD = os.getenv('VK_BOT_PASSWORD')
TEST_YANDEX_MUSIC_TOKEN = os.getenv('TEST_YANDEX_MUSIC_TOKEN')

bot = Bot(token=TELEGRAM_API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """ Отправляет приветственное сообщение и информацию о боте """
    await message.answer(
        'Пришлите мне ссылку на запись в ВК, '
        'и я добавлю музыку из нее во временный плейлист Яндекс.Музыки'
    )


@dp.message_handler(lambda message: message.text.startswith('https://vk.com/'))
async def add_tracks_to_buffer_playlist(message: types.Message):
    """ Находит в посте ВК песни и добавляет их в буферный
        плейлист Яндекс.Музыки
    """
    vk_session = get_vk_session((VK_BOT_LOGIN, VK_BOT_PASSWORD))
    tracks = get_vk_tracks(vk_session, message.text)
    client = yandex.get_client(TEST_YANDEX_MUSIC_TOKEN)
    tracks_id = yandex.get_tracks_id(client, tracks)
    if yandex.create_buffer_playlist(client, tracks_id):
        await message.answer(tools.create_tracks_answer_message(tracks))
    await message.answer('Возникла проблема с созданием плейлиста (￢_￢;)')


@dp.message_handler()
async def react_to_undefined_message(message: types.Message):
    """ Отвечает на флуд пользователя """
    await message.answer('Я не знаю, что делать с твоим сообщением :(')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
