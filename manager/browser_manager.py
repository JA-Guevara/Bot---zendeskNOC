import os
import json
import logging
from playwright.async_api import async_playwright
from datetime import datetime, timedelta

logger = logging.getLogger('main')

class BrowserManager:
    def __init__(self, headless=False):
        
        self.headless = headless
        self.browser = None
        self.context = None
        self.playwright = None
        self.storage_state_path = "user_data.json"  # Definir la ruta del archivo de estado

    async def check_and_clear_cookies(self):
        
        if os.path.exists(self.storage_state_path):
            try:
                with open(self.storage_state_path, "r") as file:
                    storage_data = json.load(file)
                    last_session_time = storage_data.get("last_session_time")

                    if last_session_time:
                        last_session_time = datetime.fromisoformat(last_session_time)
                        if datetime.now() - last_session_time > timedelta(hours=48):
                            logger.info("🕒 Han pasado más de 48 horas. Eliminando cookies...")
                            os.remove(self.storage_state_path)
                            await self.prepare_storage_state()  # Crear nuevo archivo vacío
                            return True  # Indicar que las cookies fueron eliminadas
            except Exception as e:
                logger.error(f"⚠️ Error verificando/eliminando cookies: {e}")
        return False  # Indicar que no se eliminaron cookies

    async def prepare_storage_state(self):
        
        if not os.path.exists(self.storage_state_path):
            logger.info(f"📄 Archivo {self.storage_state_path} no encontrado. Creando archivo vacío...")
            with open(self.storage_state_path, 'w') as file:
                json.dump({"cookies": [], "origins": [], "last_session_time": datetime.now().isoformat()}, file)

    async def create_browser_context(self):
        
        if not self.playwright:
            self.playwright = await async_playwright().start()

        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context()

        # Actualizar la última sesión en el archivo de almacenamiento
        with open(self.storage_state_path, 'w') as file:
            json.dump({"cookies": [], "origins": [], "last_session_time": datetime.now().isoformat()}, file)

        return self.context, self.browser

    async def close_browser(self):
        
        try:
            if self.context:
                await self.context.close()
                logger.info("✔ Contexto cerrado correctamente.")

            if self.browser:
                await self.browser.close()
                logger.info("✔ Navegador cerrado correctamente.")

            if self.playwright:
                await self.playwright.stop()
                logger.info("✔ Playwright detenido correctamente.")

        except Exception as e:
            logger.error(f"⚠️ Error al cerrar el navegador o contexto: {e}")
