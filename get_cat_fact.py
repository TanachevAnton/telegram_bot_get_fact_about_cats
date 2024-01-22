import time
import requests
from googletrans import Translator
from loguru import logger


URL = 'https://catfact.ninja/fact'
URL_PHOTO = 'https://api.thecatapi.com/v1/images/search'
ERROR_TEXT = 'Today, without facts about cats, there is no data =('

logger.add(
    f'logs/logs.log',
    rotation='10 mb',
    level='DEBUG'
)

def get_cat_photo(url: str) -> str:
    logger.debug(f'Вызов функции get_cat_photo с параметром URL: [{url}]')
    response = requests.get(url)
    logger.debug('Запрос и получение данных по API')
    if response.status_code == 200:
        logger.debug(f'Данные получены. Ответ сервера: [{response.status_code}]')
        photo_dict = response.text.replace('[', '')
        photo_dict = photo_dict.replace(']', '')
        photo_dict = eval(photo_dict)
        logger.debug(f'Получен словарь: [{photo_dict}]')
        photo_url = str(photo_dict.get('url'))
        logger.debug(f'Вытащили из словаря ссылку: [{photo_url}]')
        return photo_url
    else:
        logger.error(f'Картинки нет. Ответ от сервера не получен. Статус код: [{response.status_code}]')
        return ERROR_TEXT

def get_fact(url:str) -> str:
    logger.debug(f'Вызов функции get_fact c параметром URL: [{url}]')
    response = requests.get(url)
    logger.debug('Запрос и получение данных по API')
    if response.status_code == 200:
        logger.debug(f'Данные получены. Ответ сервера: [{response.status_code}]')
        fact = eval(response.text)
        logger.debug(f'Получен словарь: [{fact}]')
        return fact.get('fact')
    else:
        logger.error(f'Ответ от сервера не получен. Статус код: [{response.status_code}]')
        return ERROR_TEXT

def translate_ru(fact: str) -> str:
    logger.debug(f'Вызов функции translate_ru с параметром FACT: [{fact}]')
    logger.debug('Проверка наличия данных в агрументе функции')
    if fact == None:
        logger.debug('Проверка наличия данных в аргументе функции прошла без успеха, данных нет. Переводить нечего =(')
        return print('---')
    translator = Translator()
    logger.info('Начат перевод текста')
    translate = translator.translate(fact, src='en', dest='ru')
    logger.debug(f'Язык оригинала: [{translate.src}]')
    logger.debug(f'Язык перевода: [{translate.dest}]')
    logger.debug(f'Ориганал текста: [{translate.origin}]')
    logger.debug(f'Перевод текста: [{translate.text}]')
    return translate.text

def cats_fact():
    start_time = time.time()
    logger.info('-----'*20)
    logger.debug('Начало работы скрипта по получению данных факта о кошках')
    result = translate_ru(get_fact(URL))
    end_time = time.time()
    working_time = end_time - start_time
    logger.info('Данные получены, текст переведён, всё успешно')
    logger.debug(f'Завершение работы скрипта. Время выполнения, сек: [{working_time}]')
    return result
