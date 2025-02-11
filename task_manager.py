import asyncio
import logging
from utils.config import ZENDESK_USER, ZENDESK_PASSWORD, ZENDESK_URL
from manager.browser_manager import BrowserManager
from pages.login_page import LoginPage

logger_server = logging.getLogger('main')

class TaskManager:
    def __init__(self, headless=False):
        """
        Inicializa el TaskManager.
        :param headless: Indica si el navegador debe ejecutarse en modo headless.
        """
        self.headless = headless
        self.browser_manager = BrowserManager(headless=self.headless)

    async def run_login_task(self):
        """
        Ejecuta la tarea de inicio de sesión.
        """
        logger_server.info("🚀 Iniciando tarea de login...")

        try:
            # Crear el navegador y el contexto
            context, browser = await self.browser_manager.create_browser_context()
            page = await context.new_page()

            # Inicializar la página de login
            login_page = LoginPage(page)

            # Ejecutar el inicio de sesión
            login_success = await login_page.stage_login()

            if login_success:
                logger_server.info("✅ Login completado con éxito.")
            else:
                logger_server.error("❌ Falló el login.")

        except Exception as e:
            logger_server.error(f"⚠️ Error durante la tarea de login: {e}")

        finally:
            # Cerrar el navegador al finalizar
            await self.browser_manager.close_browser()
            logger_server.info("✅ Navegador cerrado correctamente.")