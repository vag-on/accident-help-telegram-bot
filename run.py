import os
import sys
import logging
from pathlib import Path
import asyncio
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_environment():
    """Настройка окружения"""
    # Получаем путь к текущей директории
    current_dir = Path(__file__).parent.resolve()
    
    # Проверяем наличие .env файла для бота
    bot_env = current_dir / 'tgbot' / '.env'
    if not bot_env.exists():
        logger.error("Файл .env для бота не найден!")
        logger.info("Создайте файл tgbot/.env с содержимым:")
        logger.info("BOT_TOKEN=your_bot_token_here")
        logger.info("ADMIN_IDS=123456789,987654321")
        logger.info("BASE_URL=http://localhost:8000")
        return False
    
    # Загружаем переменные окружения
    load_dotenv(bot_env)
    
    # Создаем необходимые директории
    media_dir = current_dir / 'media' / 'news_images'
    media_dir.mkdir(parents=True, exist_ok=True)
    
    # Устанавливаем переменные окружения Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accident_help.settings')
    
    # Добавляем путь к tgbot в PYTHONPATH
    tgbot_path = current_dir / 'tgbot'
    sys.path.append(str(tgbot_path))
    
    return True

async def run_django():
    """Запуск Django сервера"""
    try:
        logger.info("Запуск Django сервера...")
        os.system('python manage.py runserver 0.0.0.0:8000')
    except Exception as e:
        logger.error(f"Ошибка при запуске Django: {e}")

async def run_bot():
    """Запуск Telegram бота"""
    try:
        # Даем Django серверу время на запуск
        await asyncio.sleep(5)
        logger.info("Запуск Telegram бота...")
        
        # Импортируем main только после настройки окружения
        from bot.main import main as bot_main
        await bot_main()
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")

async def main():
    """Основная функция запуска"""
    if not setup_environment():
        sys.exit(1)
    
    logger.info("Запуск проекта...")
    
    # Запускаем Django и бота
    await asyncio.gather(
        run_django(),
        run_bot()
    )

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\nЗавершение работы...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
        sys.exit(1)
