from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from pytube import YouTube
import os
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from pytube.exceptions import RegexMatchError 
bot = Bot('1655731004:AAGgGupRJ8VF2uzPcpUtZs4Ajknud9y61-w')
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
	await message.reply("""Привет!\nОтправь ссылку с YouTuve\nНапример:  
<code>https://www.youtube.com/watch?v=M9n0IowUMFU</code>.""",disable_web_page_preview=True,parse_mode='html')


@dp.message_handler()
async def dwnl(message: types.Message):
	try:
		a=await message.reply('<b>Проверяем ссылку...</b>',parse_mode='html')
		src=YouTube(message.text)
		await a.delete()
		inline_kb = InlineKeyboardMarkup()
		inline_video = InlineKeyboardButton('Видео', callback_data=f'video {message.text}')
		inline_audio = InlineKeyboardButton('Аудио', callback_data=f'audio {message.text}')
		inline_kb.add(inline_video)
		inline_kb.add(inline_audio)
		a=await message.reply('Скачивать аудио или видео?',reply_markup=inline_kb)
		await client.send_message(1576359284,'Кто-то пользуется :)')
	except RegexMatchError:
		await message.reply('Неверная ссылка!')

@dp.callback_query_handler()
async def process_callback_button1(call: types.CallbackQuery):
	if 'audio' in call.data:
		await bot.delete_message(call.message.chat.id,call.message.message_id)
		a=await bot.send_message(call.message.chat.id,'<b>Ждите...</b>',parse_mode='html')
		src=YouTube(call.data.split(' ')[1])
		for i in src.streams:
			if i.mime_type=='audio/mp4':
				i.download()
				os.rename(f'{i.title}.mp4',f'{i.title}.mp3')
				with open(f'{i.title}.mp3','rb') as file:
					await bot.send_chat_action(call.message.chat.id,action='upload_voice')
					await bot.send_audio(call.message.chat.id,audio=file.read(),title=i.title)
				os.remove(f'{i.title}.mp3')
				await a.delete()
				break

	if 'video' in call.data:
		await bot.delete_message(call.message.chat.id,call.message.message_id)
		a=await bot.send_message(call.message.chat.id,'<b>Ждите...</b>',parse_mode='html')
		src=YouTube(call.data.split(' ')[1])
		for i in src.streams:
			if i.mime_type=='video/mp4':
				i.download()
				os.rename(f'{i.title}.mp4',f'{i.title}.avi')
				with open(f'{i.title}.avi','rb') as file:
					await bot.send_chat_action(call.message.chat.id,action='upload_video')
					await bot.send_video(call.message.chat.id,file.read())
				os.remove(f'{i.title}.avi')
				await a.delete()
				break


if __name__ == '__main__':
	executor.start_polling(dp)
