import asyncio
import logging
from manager.browser_manager import BrowserManager
from pages.login_page import LoginPage
from pages.zendesk_page import ZendeskPage
from pages.outlook_page import OutlookPage
from pages.excel_page import ExcelPage

logger = logging.getLogger('main')

class TaskManager:
    def __init__(self, headless=False):
        """
        Inicializa el TaskManager.
        :param headless: Indica si el navegador debe ejecutarse en modo headless.
        """
        self.headless = headless
        self.browser_manager = BrowserManager(headless=self.headless)

    async def execute(self):
        """
        Ejecuta todas las tareas en secuencia: login, Zendesk, Outlook y Excel.
        """
        logger.info("🚀 Iniciando Task Manager...")

        try:
            # Crear el navegador y el contexto
            context, browser = await self.browser_manager.create_browser_context()
            page = await context.new_page()

            # Ejecutar la tarea de login
            if not await self._execute_login(page):
                logger.error("❌ No se pudo completar el login. Deteniendo la ejecución.")
                return

            # Ejecutar la tarea de Zendesk
            await self._execute_zendesk(page)

            # Ejecutar la tarea de Outlook
            await self._execute_outlook(page)

            # Ejecutar la tarea de Excel
            await self._execute_excel(page)

        except Exception as e:
            logger.error(f"⚠️ Error durante la ejecución de tareas: {e}")
        finally:
            # Cerrar el navegador al finalizar
            await self.browser_manager.close_browser()
            logger.info("✅ Navegador cerrado correctamente.")

    async def _execute_login(self, page):
        """
        Ejecuta la tarea de inicio de sesión.
        :return: True si el login fue exitoso, False en caso contrario.
        """
        logger.info("🚀 Iniciando tarea de login...")
        login_page = LoginPage(page)
        login_success = await login_page.stage_login()

        if login_success:
            logger.info("✅ Login completado con éxito.")
            return True
        else:
            logger.error("❌ Falló el login.")
            return False

    async def _execute_zendesk(self, page):
        """
        Ejecuta la tarea de extracción de datos de Zendesk.
        """
        logger.info("🚀 Iniciando extracción de datos de Zendesk...")
        zendesk_page = ZendeskPage(page)
        await zendesk_page.zendesk_extraction()
        await asyncio.sleep(20)
        logger.info("✅ Extracción de Zendesk completada con éxito.")

    async def _execute_outlook(self, page):
        """
        Ejecuta la tarea de extracción de datos de Outlook.
        """
        logger.info("🚀📤📩 Iniciando extracción de datos de Outlook...")
        outlook_page = OutlookPage(page)
        await outlook_page.outlook_extraction()
        logger.info("✅ Extracción de Outlook completada con éxito.")

    async def _execute_excel(self, page):
       
        logger.info("🚀📊 Iniciando procesamiento de archivos Excel...")
        excel_page = ExcelPage(page)
        await excel_page.download_zip_from_email()
        await asyncio.sleep(30)
        await excel_page.extract_csv_from_zip()
        await excel_page.update_excel_consolidado()
        logger.info("✅ Procesamiento de Excel completado con éxito.")

if __name__ == "__main__":
    task_manager = TaskManager(headless=False)
    asyncio.run(task_manager.execute())