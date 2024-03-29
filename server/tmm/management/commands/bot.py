import requests

from django.core.management.base import BaseCommand
from django.conf import settings

from telegram import (Bot, Update, )
from telegram.ext import (
    CallbackContext,
    Filters,
    MessageHandler,
    CommandHandler,
    Updater, defaults,
)
from telegram.utils.request import Request

from tmm.models import (UserMails,)


def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Произошла ошибка: {e}'
            print(error_message)
            raise e
    return inner


@log_errors
def do_start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    user_id = text.replace('/start ', '')

    try:
        user = UserMails.objects.get(id=user_id)

        if UserMails.external_id is None:
            UserMails.external_id = chat_id
            UserMails.name = update.message.from_user.username
            UserMails.save()

            update.message.reply_text(
                text='Авторизация успешно пройдена'
            )
            return
        


    except UserMails.DoesNotExist:
        update.message.reply_text(
            text='Данного пользователя не существует, за подробностями обратитесь к техническому администратору'
        )
        return


class Command(BaseCommand):
    help = 'Telegram Bot'

    def handle(self, *args, **options):
        print('Start')
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )

        bot = Bot(
            request=request,
            token=settings.TOKEN,
            base_url=settings.PROXY_URL
        )

        print(bot.get_me())

        updater = Updater(
            bot=bot,
            use_context=True,
        )

        bind_user = CommandHandler('start', do_start)
        updater.dispatcher.add_handler(bind_user)

        updater.start_polling()
        updater.idle()
