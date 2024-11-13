from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup


import keyboards
import crud_functions

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


class RegistrationSate(StatesGroup):
    username = State()
    email = State()
    age = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.",
                         reply_markup=keyboards.start_kb)


@dp.message_handler(text="Регистрация")
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит)")
    await RegistrationSate.username.set()


@dp.message_handler(state=RegistrationSate.username)
async def set_username(message, state):
    name_incl = crud_functions.is_included(message.text)
    if name_incl:
        await message.answer("Пользователь существует, введите другое имя")
        await message.answer("Введите имя пользователя (только латинский алфавит)")
        await RegistrationSate.username.set()
    else:
        await state.update_data(first=message.text)
        await message.answer("Введите свой email:")
        await RegistrationSate.email.set()


@dp.message_handler(state=RegistrationSate.email)
async def set_email(message, state):
    await state.update_data(second=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationSate.age.set()


@dp.message_handler(state=RegistrationSate.age)
async def set_age(message, state):
    await state.update_data(third=message.text)
    data = await state.get_data()
    crud_functions.add_user(str(data['first']), str(data['second']), int(data['third']))
    await message.answer("Регистрация успешно завершена", reply_markup=keyboards.start_kb)
    await state.finish()


@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer("Выберите опцию", reply_markup=keyboards.calories_kb)


@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer("10*вес(кг) + 6.25 * рост(см) + 5 * возраст(г) + 5")
    await call.message.answer("Выберите опцию", reply_markup=keyboards.calories_kb)
    await call.answer()


@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer("Введите свой возраст:")
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(first=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(second=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_colories(message, state):
    await state.update_data(third=message.text)
    data = await state.get_data()
    calc_colories = 10 * int(data['first']) + 6.25 * int(data['second']) + 5 * int(data['third']) + 5
    await message.answer(f"Ваша норма калорий: {calc_colories}")
    await message.answer("Продолжите выбор опций", reply_markup=keyboards.start_kb)
    await state.finish()


@dp.message_handler(text="Купить")
async def get_buying_list(message):
    data_products = crud_functions.get_all_products()
    for product in data_products:
        await message.answer(
            f"Название: {product[1]} | Описание: {product[2]}| Цена: {product[3]}")
        with open(f'p{product[0]}.jpg', 'rb') as ph:
            await message.answer_photo(ph)
    await message.answer("Выберите продукт для покупки", reply_markup=keyboards.catalog_kb)


@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
