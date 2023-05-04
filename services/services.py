import requests

from config_data.config import Config, load_config

# Загружаем конфиг в переменную config
config: Config = load_config()

# ---------------Работаем с погодой-------------------
weather_api_key = config.weather.token


def get_weather(city: str) -> dict[str:str]:
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&lang=ru&units=metric&appid=' + weather_api_key
    responce = requests.get(url.format(city)).json()
    if responce['cod'] == '404':
        city_info = {'error': 'Город не найден.'}
        return city_info
    city_info = {
        'temp': round(responce['main']['temp']),
        'description': responce['weather'][0]['description'],
        'error': None
    }
    return city_info


# ---------------Работаем с курсом валют--------------
exchange_api_key = config.exchange.token


def get_rate(currency1: str, currency2: str, amount: str) -> dict[str:str | int]:
    url = f'https://v6.exchangerate-api.com/v6/{exchange_api_key}/latest/{currency1}'
    responce = requests.get(url).json()
    result = {
        'rate': responce['conversion_rates'][currency2],
        'exchange': int(amount) * responce['conversion_rates'][currency2]
    }
    return result


# ---------------Работаем с картинкой-------------------

def get_image() -> str:
    url = 'https://randomfox.ca/floof/?ref=apilist.fun'
    responce = requests.get(url).json()
    result = responce['image']
    return result


# ---------------Работаем с опросом-------------------

def get_poll_answers(answers: str) -> list[str]:
    poll_answers = []
    answer = ''

    for i in answers:
        if i == '\n':
            poll_answers.append(answer.strip())
            answer = ''
        answer += i
    poll_answers.append(answer.strip())

    return poll_answers
