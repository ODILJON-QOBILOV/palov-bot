import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
API_TOKEN = '6535660484:AAFzZt9tDQ9vsbahb87rZTZqnZaqT4oR4XI'
storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)

from app import database

dict_of_items = {
    'guruch': 1,
    'gosht': 1,
    'dumba': 0.15,
    'sabzi': 1.2,
    'yog' : 0.34,
    'nohot': 0.1,
    'piyoz': 0.3,
    'magiz': 0.1
}

price_of_items = {
    'guruch': 34000,
    'gosht': 100000,
    'dumba': 100000,
    'sabzi': 8000,
    'yog' : 25000,
    'nohot': 50000,
    'piyoz': 5000,
    'magiz': 40000
}

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    database.start_db()
    database.add_user(message.from_user.username, message.from_user.id)
    await message.answer("Hi!")

    # if message.from_user.id == 7049119939:
    #     await message.answer("Siz admin")


@dp.message_handler(commands=['new_order'])
async def new_order(message: types.Message):
    await message.answer('Oshni kg sini kiriting: ')




@dp.message_handler()
async def get_weight(message: types.Message):
    try:
        weight = float(message.text)
        results = []
        total_sum = 0
        
        for item, weight_multiplier in dict_of_items.items():
            if item in price_of_items:
                total_cost = weight * weight_multiplier * price_of_items[item]
                total_sum += total_cost
                formatted_price = format_price(price_of_items[item])
                formatted_result = f'{item}: {weight * weight_multiplier:.2f} kg, narxi: {format_cost(total_cost)} so\'m'
                results.append(formatted_result)
        
        formatted_total_sum = format_cost(total_sum)
        results.append(f'\nNarxi: {formatted_total_sum} so\'m')

        await message.answer('\n'.join(results))
        # await message.answer(7049119939, '\n'.join(results))
        # await message.answer(7049119939, message.from_user.id)
        admin_id = 7049119939  # Replace with actual admin ID
        admin_message = f"User: {message.from_user.full_name}\nID: {message.from_user.id}\n"
        admin_message += '\n'.join(results)
        
        if message.from_user.id == admin_id:
            await message.answer(admin_message)
        else:
            await bot.send_message(admin_id, admin_message)
    except ValueError:
        await message.answer("Invalid input. Please enter a valid number for the weight.")


def format_price(price):
    return '{:,.0f}'.format(price).replace(',', '.')


def format_cost(cost):
    return '{:,.0f}'.format(cost).replace(',', '.')







if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)