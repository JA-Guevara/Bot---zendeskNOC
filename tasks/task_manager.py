import asyncio
import logging
from manager.browser_manager import BrowserManager
from pages.login_page import LoginPage
from pages.zendesk_page import ZendeskPage 
from pages.outlook_page import OutlookPage

logger = logging.getLogger('main')

class LoginTask:
    def __init__(self, headless=False):
        """
        Inicializa la tarea de login.
        :param headless: Indica si el navegador debe ejecutarse en modo headless.
        """
        self.headless = headless
        self.browser_manager = BrowserManager(headless=self.headless)

    async def execute(self):
        """
        Ejecuta la tarea de login y luego la tarea de Zendesk.
        """
        logger.info("🚀 Iniciando tarea de login...")

        try:
            # Crear el navegador y el contexto
            context, browser = await self.browser_manager.create_browser_context()
            page = await context.new_page()

            # Inicializar la página de login
            login_page = LoginPage(page)

            # Ejecutar el inicio de sesión
            login_success = await login_page.stage_login()

            if login_success:
                logger.info("✅ Login completado con éxito.")

                # Inicializar la página de Zendesk
                zendesk_page = ZendeskPage(page)

                # Ejecutar la tarea de Zendesk
                logger.info("🚀 Iniciando tarea de Zendesk...")
                await zendesk_page.zendesk_extraction()
                logger.info("✅ Tarea de Zendesk completada con éxito.")
                
                outlook_page = OutlookPage(page)
                logger.info("🚀📤📩 Iniciando tarea de outlook...")
                await outlook_page.outlook_extraction()
                logger.info("✅ Tarea de Outlook completada con éxito.")

            else:
                logger.error("❌ Falló el login.")

        except Exception as e:
            logger.error(f"⚠️ Error durante la tarea de login o Zendesk: {e}")

        finally:
            # Cerrar el navegador al finalizar
            await self.browser_manager.close_browser()
            logger.info("✅ Navegador cerrado correctamente.")