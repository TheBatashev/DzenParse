from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class Config:

    """
    Конфиг.Хранение всех значений
    """

    token_bot : str # Токен бота
    api_key_gpt : str # Апи ключ ЧАТГПТ
    chat_id : int # Чат ид куда отправляются СМС
    url : str # Юрл сайта
    message_timeout : int # Задержка перезагрузки сайта для ожидания новсстей


# Создаем экземпляр класса конфига и достаем значения из файла .env

config = Config(token_bot=os.getenv('TOKEN_BOT'), api_key_gpt=os.getenv('API_KEY_GPT'), 
                chat_id=os.getenv('CHAT_ID'), url=os.getenv('URL'), message_timeout=os.getenv('MESSAGE_TIMEOUT'))

