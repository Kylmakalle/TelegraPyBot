from html_telegraph_poster import TelegraphPoster
from newspaper import Article
from xml.etree import ElementTree
import telebot
from postercredentials import token, access_token

t = TelegraphPoster(access_token=access_token)

bot = telebot.TeleBot(token)

linktrigger = ['.ru', '.com', '.net', '.org']


def page_create(message):
    try:
        article = Article(message.text)
        article.download()
        article.parse()
        html = str(ElementTree.tostring(article.clean_top_node), 'utf-8')
        bot.send_message(message.chat.id, t.post(title=article.title,
                                                 author='@TelegraPyBot',
                                                 author_url='https://t.me/TelegraPyBot',
                                                 text='<img src="{}">'.format(
                                                     article.top_image) + html + '<br><br><a href="{}">Оригинал</a>'.format(
                                                     message.text))['url'])
    except:
        bot.send_message(message.chat.id, 'Чёт не получается(')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Отправь мне ссылку')


@bot.message_handler(content_types=['text'])
def link_parser(message):
    if any(i in message.text for i in linktrigger):
        bot.send_chat_action(message.chat.id, 'typing')
        page_create(message)
    else:
        bot.send_message(message.chat.id, 'Это не ссылка')


bot.skip_pending = True
bot.polling(none_stop=True, interval=0)
