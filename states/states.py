from aiogram.fsm.state import State, StatesGroup


# Создаем класс, наследуемый от StatesGroup, для группы состояний FSM
class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    fill_city = State()  # Состояние ожидания ввода города
    fill_currency1 = State()  # Состояния ожидания выбора 1 валюты
    fill_currency2 = State()  # Состояния ожидания выбора 2 валюты
    fill_amount = State()  # Состояния ожидания ввода суммы
    fill_poll_question = State()  # Состояние ожидания ввода вопроса для опроса
    fill_poll_answer = State()  # Состояние ожидания ввода ответа для опроса
    fill_poll_id_send = State()  # Состояние ожидания ввода ответа для опроса
