import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By

from aiogram import Bot, Dispatcher, types , Router 
import asyncio

from config import config
from chat_main import send_to_gpt


async def send_message_to_telegram(chat_id, message):
    await bot.send_message(chat_id, message)

bot = Bot(token=config.token_bot, parse_mode='HTML')
dispatcher = Dispatcher()



url = config.url

service = Service('C:\\Users\\Admin\\Desktop\\dzen_pars\\chromedriver.exe')
option_chrome = webdriver.ChromeOptions()
# option_chrome.add_argument('--headless')

# processed_links = set()
links = []

async def start_parsing():

    """
    Функция бесконечного парсинга страницы , ожидаем новости и обрабатываем как только их получаем
    """

    browser =  webdriver.Chrome(options=option_chrome, service=service) 
    browser.get(url=url)

    browser.find_element(By.CLASS_NAME, 'news-feed-redesign__list')        
    browser.find_elements(By.CLASS_NAME, 'mg-card__shown-card news-card2-redesign__show-wKQenXg2q6OVuo52I')
    all_links = browser.find_elements(By.TAG_NAME, 'a')


    # while True:

    for link in all_links:
        href = link.get_attribute('href')
        if href.startswith('https://dzen.ru') and len(href) > 40:
            if href != 'https://dzen.ru/news/rubric/personal_feed':
                links.append(href)

    while True:
        browser.refresh()
        all_links = browser.find_elements(By.TAG_NAME, 'a')
        for link in all_links:
            href = link.get_attribute('href')
            # if href.startswith('https://dzen.ru') and len(href) > 40:
            if href != 'https://dzen.ru/news/rubric/personal_feed' and href not in links and href.startswith('https://dzen.ru') and len(href) > 40:
                    browser.get(href)
                    desc = browser.find_elements(By.CLASS_NAME, 'news-story-redesign__summarization-item-text')
                    text = []
                    for d in desc:
                        text.append(d.text)
                        # print(d.text)                
                        time.sleep(1)
                    response_gpt = send_to_gpt(' '.join(text))
                    await send_message_to_telegram(chat_id=config.chat_id, message=response_gpt)
                    links.append(href)
                    text.clear()
                    break
            else:
                time.sleep(config.message_timeout)
                break
                

async def main():
    # Объект бота
    bot = Bot(token=config.token_bot, parse_mode='HTML')

    # Диспетчер
    dp = Dispatcher()
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


# Запускаем                        

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(start_parsing())
    asyncio.run(main())