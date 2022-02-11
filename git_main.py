from aiogram import Bot, types, executor, Dispatcher
import sqlite3
import logging

TOKEN = "_TOKEN_"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['show'])
async def test(message: types.Message):
    key = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton(text='Test it', callback_data='testit')
    key.row(b1)
    await message.answer('Take a chance', reply_markup=key)

@dp.callback_query_handler(text='testit')
async def update(call: types.CallbackQuery): #вот эта функция не выполняется полностью
    uid = call.message.from_user.id
    conn = sqlite3.connect('db/gecko.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('UPDATE table_name SET column = ? WHERE user_id = ?', ('some_text', uid))
    conn.commit()
    cursor.close()
    print('ok')

@dp.message_handler(content_types=['text'])
async def sl(msg: types.Message): #эта функция работает прекрасно и вносит все изменения в таблицу
    if msg.text == 'sl':
        uid = msg.from_user.id
        conn = sqlite3.connect('db/gecko.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('UPDATE table_name SET column = ? WHERE user_id = ?', ('some_text', uid))
        conn.commit()
        cursor.close()
        print('ok')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)