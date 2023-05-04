from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU

# ------- Создаем инлайн клавиатуру выбора функции бота -------

# Создаем кнопки выбора действия
button_weather: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_RU['weather_button'],
                                                            callback_data='weather_button_pressed')
button_currency: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_RU['currency_button'],
                                                             callback_data='exchange_button_pressed')
button_cute_image: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_RU['cute_image_button'],
                                                               callback_data='cute_image_button_pressed')
button_polls: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_RU['polls_button'],
                                                          callback_data='polls_button_pressed')
# Инициализируем билдер для клавиатуры функций с кнопками
base_kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

# Добавляем кнопки в билдер с параметром width=2
base_kb_builder.row(button_weather, button_currency, button_cute_image, button_polls, width=2)

# Создаем клавиатуру
base_kb = base_kb_builder.as_markup(resize_keyboard=True)

# ------- Создаем инлайн валютную клавиатуру -------
currency_list1 = ['USD', 'AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT',
                  'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL', 'BSD', 'BTN', 'BWP', 'BYN', 'BZD', 'CAD', 'CDF',
                  'CHF', 'CLP', 'CNY', 'COP', 'CRC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN',
                  'ETB', 'EUR', 'FJD', 'FKP', 'FOK', 'GBP', 'GEL', 'GGP', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD',
                  'HKD', 'HNL', 'HRK', 'HTG', 'HUF', 'IDR', 'ILS', 'IMP', 'INR', 'IQD', 'IRR', 'ISK', 'JEP', 'JMD',
                  'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KID', 'KMF', 'KRW', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR',
                  'LRD', 'LSL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRU', 'MUR', 'MVR']

currency_list2 = ['MWK', 'MXN', 'MYR', 'MZN', 'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK',
                  'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR', 'SDG', 'SEK',
                  'SGD', 'SHP', 'SLE', 'SLL', 'SOS', 'SRD', 'SSP', 'STN', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND',
                  'TOP', 'TRY', 'TTD', 'TVD', 'TWD', 'TZS', 'UAH', 'UGX', 'UYU', 'UZS', 'VES', 'VND', 'VUV', 'WST',
                  'XAF', 'XCD', 'XDR', 'XOF', 'XPF', 'YER', 'ZAR', 'ZMW', 'ZWL']

# Инициализируем список для кнопок
buttons1: list[InlineKeyboardButton] = []
buttons2: list[InlineKeyboardButton] = []
# Инициализируем билдер для клавиатуры валют
currency_kb_builder1: InlineKeyboardBuilder = InlineKeyboardBuilder()
currency_kb_builder2: InlineKeyboardBuilder = InlineKeyboardBuilder()
for button in currency_list1:
    buttons1.append(InlineKeyboardButton(text=button, callback_data=button))

buttons1.append(InlineKeyboardButton(text='->', callback_data='->'))
buttons2.append(InlineKeyboardButton(text='<-', callback_data='<-'))

for button in currency_list2:
    buttons2.append(InlineKeyboardButton(text=button, callback_data=button))

# Добавляем кнопки в билдер с параметром width=6
currency_kb_builder1.row(*buttons1, width=6)
currency_kb_builder2.row(*buttons2, width=6)
# Создаем клавиатуру
currency_kb1 = currency_kb_builder1.as_markup(resize_keyboard=True)
currency_kb2 = currency_kb_builder2.as_markup(resize_keyboard=True)
