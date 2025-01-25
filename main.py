import requests
import asyncio
from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from telegram import Bot
from telegram.error import TelegramError

# Замените на ваш токен и chat_id
TELEGRAM_BOT_TOKEN = '7950399124:AAFxSpWkGDWMgGwuzsLT_2RJxW-bMXL3HNU'
CHAT_ID = '1205701281'

class InternetMonitorApp(App):
    def build(self):
        self.label = Label(text="Monitoring internet connection...")
        self.previous_state = None  # Предыдущее состояние интернета
        Clock.schedule_interval(self.check_internet, 10)  # Проверка каждые 10 секунд
        return self.label

    def check_internet(self, dt):
        try:
            # Проверяем доступность интернета
            requests.get('https://www.google.com', timeout=5)
            current_state = "connected"
        except requests.ConnectionError:
            current_state = "disconnected"

        # Если состояние изменилось
        if current_state != self.previous_state:
            self.previous_state = current_state

            # Определяем тип подключения
            connection_type = self.get_connection_type()

            # Отправляем сообщение
            if current_state == "connected":
                message = f"Подключен к интернету через {connection_type}."
            else:
                message = f"Отключен от интернета."

            # Запускаем асинхронную задачу
            asyncio.run_coroutine_threadsafe(self.send_telegram_message(message), self.loop)

    def get_connection_type(self):
        """
        Заглушка для тестирования на ПК.
        """
        return "Wi-Fi"  # Или "мобильную сеть" для тестирования

    async def send_telegram_message(self, message):
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        try:
            await bot.send_message(chat_id=CHAT_ID, text=message)
            print("Message sent successfully.")
        except TelegramError as e:
            print(f"Failed to send message: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    # Создаем и запускаем цикл событий asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Запускаем Kivy приложение
    app = InternetMonitorApp()
    app.loop = loop  # Передаем цикл событий в приложение

    # Запускаем цикл событий в отдельном потоке
    from threading import Thread
    Thread(target=loop.run_forever, daemon=True).start()

    # Запускаем Kivy
    app.run()