import asyncio
import logging
from tasks.task_manager import TaskManager  # Importa la clase correcta
from logging_pages.logging_config import setup_logging

# Configurar el logger
setup_logging()

logger = logging.getLogger('main')

async def main():
    logger.info("🚀 Iniciando el programa...")

    # Crear instancia de TaskManager y ejecutar la tarea
    task_manager = TaskManager(headless=False)
    await task_manager.execute()

    logger.info("🏁 Programa finalizado.")

if __name__ == "__main__":
    asyncio.run(main())
