import asyncio
import logging
from tasks.task_manager import LoginTask
from logging_pages.logging_config import setup_logging

# Configurar el logger
setup_logging()

logger = logging.getLogger('main')

async def main():
    
    logger.info("🚀 Iniciando el programa...")


    login_task = LoginTask(headless=False)
    await login_task.execute()

    logger.info("🏁 Programa finalizado.")

if __name__ == "__main__":
    asyncio.run(main())