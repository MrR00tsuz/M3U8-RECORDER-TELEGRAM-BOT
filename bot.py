import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import subprocess
import os

TOKEN = 'BOT_TOKEN'
ffmpeg_process = None

KAYIT_DIZINI = r'C:\Users\root\Pictures\M3U8\Kayıtlar'

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Merhaba! Canlı yayını kaydetmek için /kaydet komutunu kullanabilirsin.")

def kaydet(update, context):
    url = context.args[0]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Lütfen kaydedilecek video dosyasının adını girin:")
    context.user_data['isim_bekliyor'] = True
    context.user_data['url'] = url

def handle_video_name(update, context):
    if 'isim_bekliyor' in context.user_data and context.user_data['isim_bekliyor']:
        video_dosya_adi = update.message.text.strip()
        url = context.user_data['url']
        os.makedirs(KAYIT_DIZINI, exist_ok=True)
        video_dosya_yolu = os.path.join(KAYIT_DIZINI, video_dosya_adi)
        komut = ['ffmpeg', '-i', url, '-c', 'copy', video_dosya_yolu]
        global ffmpeg_process
        ffmpeg_process = subprocess.Popen(komut, creationflags=subprocess.CREATE_NEW_CONSOLE)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Canlı yayın kaydediliyor.")
        context.user_data['isim_bekliyor'] = False
        context.user_data['url'] = None
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Dosya adı beklenmiyor.")

def stop(update, context):
    global ffmpeg_process
    if ffmpeg_process:
        ffmpeg_process.terminate()
        ffmpeg_process = None
        context.bot.send_message(chat_id=update.effective_chat.id, text="Kayıt durduruldu.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Hiçbir kayıt işlemi yok.")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    kaydet_handler = CommandHandler('kaydet', kaydet)
    stop_handler = CommandHandler('stop', stop)
    video_name_handler = MessageHandler(Filters.text & ~Filters.command, handle_video_name)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(kaydet_handler)
    dispatcher.add_handler(stop_handler)
    dispatcher.add_handler(video_name_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
