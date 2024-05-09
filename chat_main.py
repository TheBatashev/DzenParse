
import openai
from aiogram import Bot

openai.api_key = ''



def send_to_gpt(text, bot : Bot):

    '''
    Функция отправки промта чатгпт и получение результата
    '''

    completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты журналист"},
                {"role": "user",
                "content": f"Прочитай эту новость, придумай заголовок и сократи текст. После заголовка всегда делай пропус строки. В ответе не используй слово 'заголовок' и ссылки. Что бы сократить текст новости спользуй от 20 до 100 слов. Новость:  {text}"}
            ]
        )
    
    response = completion.choices[0].message.content

    return response
