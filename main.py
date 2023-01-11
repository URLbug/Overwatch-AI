from aiogram import types, executor, Bot, Dispatcher
from aiogram.types import InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from AI import win_procent
from context import AI_Go
from __init__ import config, text


bot = Bot(config['TOKEN'])
dp = Dispatcher(bot,storage=MemoryStorage())

ai_predicts = {
    'url': None,
    'comand': None,
    'page': None
}

@dp.message_handler(commands=['start'])
async def start(m: types.Message):

    markup = InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Меню', callback_data='menu'))

    await m.reply(text['start'], reply_markup=markup)

@dp.callback_query_handler(text='menu')
async def menu(call: types.CallbackQuery):

    markup = InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Начать', callback_data='go'))

    await call.message.edit_text(text['menu'],reply_markup=markup)

@dp.callback_query_handler(text='go',state=None)
async def menu(call: types.CallbackQuery, state: FSMContext):

    await call.message.edit_text('url')
    await AI_Go.url.set()


@dp.message_handler(state=AI_Go.url)
async def menu(m: types.Message, state: FSMContext):

    ai_predicts['url'] = m.text
    await m.reply('comand')
    await bot.delete_message(chat_id=m.chat.id, message_id=m.message_id)
    await AI_Go.next()

@dp.message_handler(state=AI_Go.comand)
async def menu(m: types.Message, state: FSMContext):

    ai_predicts['comand'] = m.text
    await m.reply('page')
    await bot.delete_message(chat_id=m.chat.id, message_id=m.message_id)
    await AI_Go.next()

@dp.message_handler(state=AI_Go.sum_page)
async def menu(m: types.Message, state: FSMContext):

    ai_predicts['page'] = m.text
    await m.reply('second')
    why = win_procent(ai_predicts['url'],ai_predicts['comand'],int(ai_predicts['page']))
    await m.reply(why)
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True)