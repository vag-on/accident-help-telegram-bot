import sys
import os
import logging
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
import asyncio
import threading
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Запуск Telegram бота'

    def setup_environment(self):
        """Настройка окружения для запуска бота"""
        # Проверяем наличие .env файла
        tgbot_path = Path(settings.BASE_DIR) / 'tgbot'
        env_path = tgbot_path / '.env'
        
        if not env_path.exists():
            self.stdout.write(self.style.ERROR('Файл .env не найден в директории tgbot!'))
            self.stdout.write('Создайте файл .env с необходимыми переменными:')
            self.stdout.write('BOT_TOKEN=your_bot_token_here')
            self.stdout.write('ADMIN_IDS=123456789,987654321')
            self.stdout.write('BASE_URL=http://localhost:8000')
            return False
        
        # Загружаем переменные окружения из .env файла
        load_dotenv(env_path)
        
        # Проверяем наличие директории для медиафайлов
        media_dir = Path(settings.BASE_DIR) / 'media' / 'news_images'
        media_dir.mkdir(parents=True, exist_ok=True)
        
        return True

    def handle(self, *args, **options):
        if not self.setup_environment():
            return
        
        try:
            # Импортируем main только после настройки окружения
            from bot.main import main as run_bot
            
            # Запускаем бота в отдельном потоке
            bot_thread = threading.Thread(target=self._run_bot, args=(run_bot,))
            bot_thread.daemon = True
            bot_thread.start()
            
            self.stdout.write(self.style.SUCCESS('Telegram бот запущен'))
            
            # Держим основной поток активным
            try:
                while True:
                    if not bot_thread.is_alive():
                        self.stdout.write(self.style.ERROR('Бот неожиданно остановился!'))
                        break
                    asyncio.get_event_loop().run_until_complete(asyncio.sleep(1))
            except KeyboardInterrupt:
                self.stdout.write(self.style.SUCCESS('\nБот остановлен'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при запуске бота: {e}'))
            logger.error(f"Ошибка при запуске бота: {e}", exc_info=True)

    def _run_bot(self, run_bot):
        """Запуск бота через asyncio"""
        try:
            asyncio.run(run_bot())
        except Exception as e:
            logger.error(f"Ошибка в работе бота: {e}", exc_info=True)
