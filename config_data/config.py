from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту


@dataclass
class Weather:
    token: str  # Токен для доступа к api погоды


@dataclass
class Exchange:
    token: str  # Токен для доступа к api курсов обмена валют


@dataclass
class Config:
    tg_bot: TgBot
    weather: Weather
    exchange: Exchange


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')), weather=Weather(token=env('WEATHER_TOKEN')),
                  exchange=Exchange(token=env('EXCHANGE_RATE_TOKEN')))
