import asyncio
import logging
from tasks.task_manager import LoginTask
from logging_pages.logging_config import setup_logging

# Configurar el logger
setup_logging()

logger = logging.getLogger('main')

async def main():
    """
    Función principal que ejecuta la tarea de login.
    """
    logger.info("🚀 Iniciando el programa...")

    # Crear la tarea de login (modo no headless para ver el navegador)
    login_task = LoginTask(headless=False)

    # Ejecutar la tarea
    await login_task.execute()

    logger.info("🏁 Programa finalizado.")

if __name__ == "__main__":
    asyncio.run(main())