from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.filters import Command, CommandStart, StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message

from keyboards.keyboards import (base_kb, currency_kb1, currency_kb2,
                                 currency_list1, currency_list2)
from lexicon.lexicon_ru import LEXICON_RU
from services.services import (get_image, get_poll_answers, get_rate,
                               get_weather)
from states.states import FSMFillForm

router: Router = Router()

# Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
storage: MemoryStorage = MemoryStorage()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text=f'<b>Привет {message.from_user.first_name}!</b>\n\n{LEXICON_RU["/start"]}')


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/help'], reply_markup=base_kb)
    await state.clear()


# -------------------------------- Погода ---------------------------------------------

# Этот хэндлер срабатывает на инлайн кнопку погода
@router.callback_query(Text(text='weather_button_pressed'), StateFilter(default_state))
async def process_weather(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['weather_ask'])
    # Устанавливаем состояние ожидания ввода города
    await state.set_state(FSMFillForm.fill_city)


# Этот хэндлер будет срабатывать во время ввода города
# показывать погоду и выводить из машины состояний
@router.message(StateFilter(FSMFillForm.fill_city))
async def process_name_sent(message: Message, state: FSMContext):
    weather = get_weather(message.text)
    if weather['error']:
        await message.answer(text=weather["error"], reply_markup=base_kb)
    else:
        await message.answer(text=f'В городе {message.text} сейчас:\n'
                                  f'Температура: {"+" if weather["temp"] > 0 else ""}{weather["temp"]}, '
                                  f'{weather["description"]}', reply_markup=base_kb)
        # Завершаем машину состояний
    await state.clear()


# -------------------------------- Курс валют ---------------------------------------------


# Этот хэндлер срабатывает на инлайн кнопку курс валют
@router.callback_query(Text(text='exchange_button_pressed'), StateFilter(default_state))
async def process_exchange_rate(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['currency_ask1'], reply_markup=currency_kb1)
    # Устанавливаем состояние ожидания выбора валюты
    await state.set_state(FSMFillForm.fill_currency1)


# Этот хэндлер срабатывает на перелистывание списка валют вперед при выборе 1й валюты
@router.callback_query(Text(text='->'), StateFilter(FSMFillForm.fill_currency1))
async def process_currency1_forward(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON_RU['currency_ask1'], reply_markup=currency_kb2)


# Этот хэндлер срабатывает на перелистывание списка валют назад при выборе 1й валюты
@router.callback_query(Text(text='<-'), StateFilter(FSMFillForm.fill_currency1))
async def process_currency1_back(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON_RU['currency_ask1'], reply_markup=currency_kb1)


# Этот хэндлер срабатывает на инлайн кнопки выбора валюты 1
@router.callback_query(StateFilter(FSMFillForm.fill_currency1))
async def process_currency1(callback: CallbackQuery, state: FSMContext):
    if callback.data in currency_list1 or callback.data in currency_list2:
        await state.update_data(currency1=callback.data)
        await callback.message.edit_text(text=LEXICON_RU['currency_ask2'], reply_markup=currency_kb1)
        # Устанавливаем состояние ожидания выбора валюты
        await state.set_state(FSMFillForm.fill_currency2)


# Этот хэндлер срабатывает на перелистывание списка валют вперед при выборе 2й валюты
@router.callback_query(Text(text='->'), StateFilter(FSMFillForm.fill_currency2))
async def process_currency2_forward(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON_RU['currency_ask2'], reply_markup=currency_kb2)


# Этот хэндлер срабатывает на перелистывание списка валют назад при выборе 2й валюты
@router.callback_query(Text(text='<-'), StateFilter(FSMFillForm.fill_currency2))
async def process_currency2_back(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON_RU['currency_ask2'], reply_markup=currency_kb1)


# Этот хэндлер срабатывает на инлайн кнопки выбора валюты 2
@router.callback_query(StateFilter(FSMFillForm.fill_currency2))
async def process_currency2(callback: CallbackQuery, state: FSMContext):
    if callback.data in currency_list1 or callback.data in currency_list2:
        await state.update_data(currency2=callback.data)
        await callback.message.edit_text(text=LEXICON_RU['amount_ask'])
        # Устанавливаем состояние ожидания выбора валюты
        await state.set_state(FSMFillForm.fill_amount)


# Этот хэндлер будет срабатывать во время ввода количества валюты
# и выдавать результат обмена
@router.message(StateFilter(FSMFillForm.fill_amount), F.text.isdigit())
async def process_exchange(message: Message, state: FSMContext):
    currency_data = await state.get_data()
    result = get_rate(currency_data['currency1'], currency_data['currency2'], message.text)
    await message.answer(text=f"{currency_data['currency1']} -> {currency_data['currency2']}\n"
                              f"1 {currency_data['currency1']} = {result['rate']} {currency_data['currency2']}\n"
                              f"{message.text} {currency_data['currency1']} = "
                              f"{result['exchange']} {currency_data['currency2']}", reply_markup=base_kb)
    # Завершаем машину состояний
    await state.clear()


# -------------------------------- Картинка ---------------------------------------------


# Этот хэндлер срабатывает на инлайн кнопку картинка
@router.callback_query(Text(text='cute_image_button_pressed'), StateFilter(default_state))
async def process_image(callback: CallbackQuery):
    image = get_image()
    await callback.message.edit_text(text=image, reply_markup=base_kb)


# -------------------------------- Опрос ---------------------------------------------

# Этот хэндлер срабатывает на инлайн кнопку опроса
@router.callback_query(Text(text='polls_button_pressed'), StateFilter(default_state))
async def process_poll(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['ask_poll_question'])
    await state.set_state(FSMFillForm.fill_poll_question)


# Этот хэндлер срабатывает на ввод вопроса опроса
@router.message(StateFilter(FSMFillForm.fill_poll_question))
async def process_poll_question(message: Message, state: FSMContext):
    await state.update_data(question=message.text)
    await message.answer(text=LEXICON_RU['ask_poll_answer'])
    await state.set_state(FSMFillForm.fill_poll_answer)


# Этот хэндлер срабатывает на ввод ответов опроса
@router.message(StateFilter(FSMFillForm.fill_poll_answer))
async def process_poll_answers(message: Message, state: FSMContext):
    await state.update_data(answers=message.text)
    poll = await state.get_data()
    if len(poll['answers']) < 2:
        await message.answer(text=LEXICON_RU['questions_error'])
    else:
        await message.answer(text=LEXICON_RU['poll_id_ask'])
        await state.set_state(FSMFillForm.fill_poll_id_send)


# Этот хэндлер срабатывает на ввод id чата для отправки вопроса
@router.message(StateFilter(FSMFillForm.fill_poll_id_send))
async def process_poll_send_id(message: Message, state: FSMContext, bot: Bot):
    poll = await state.get_data()
    poll_answers = get_poll_answers(poll['answers'])

    try:
        await bot.get_chat_member(message.text, 6236078581)
    except TelegramBadRequest:
        await message.answer(text=LEXICON_RU['chat_id_error'])
    else:
        try:
            await bot.send_poll(chat_id=message.text, question=poll['question'], options=poll_answers)
        except TelegramForbiddenError:
            await message.answer(text=LEXICON_RU['chat_id_error2'])
        else:
            await message.answer(text=f'Ваш опрос отправлен в чат {message.text}', reply_markup=base_kb)
            await state.clear()
