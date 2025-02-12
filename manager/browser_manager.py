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
        """Verifica y elimina las cookies si han pasado más de 48 horas."""
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
        """Crea un archivo de estado vacío si no existe."""
        if not os.path.exists(self.storage_state_path):
            logger.info(f"📄 Archivo {self.storage_state_path} no encontrado. Creando archivo vacío...")
            with open(self.storage_state_path, 'w') as file:
                json.dump({"cookies": [], "origins": [], "last_session_time": datetime.now().isoformat()}, file)

    async def create_browser_context(self):
        """Crea un nuevo contexto del navegador y carga las cookies si existen."""
        if not self.playwright:
            self.playwright = await async_playwright().start()

        self.browser = await self.playwright.chromium.launch(headless=self.headless)

        # Cargar el estado de almacenamiento si existe
        if os.path.exists(self.storage_state_path):
            with open(self.storage_state_path, "r") as file:
                storage_state = json.load(file)
                self.context = await self.browser.new_context(storage_state=storage_state)
                logger.info("✅ Cookies cargadas desde el archivo de estado.")
        else:
            self.context = await self.browser.new_context()
            logger.info("🔄 No se encontraron cookies. Creando nuevo contexto.")

        return self.context, self.browser

    async def save_storage_state(self):
        """Guarda el estado de almacenamiento (cookies) en el archivo."""
        try:
            storage_state = await self.context.storage_state()
            storage_state["last_session_time"] = datetime.now().isoformat()
            with open(self.storage_state_path, "w") as file:
                json.dump(storage_state, file)
            logger.info("✅ Estado de almacenamiento guardado correctamente.")
        except Exception as e:
            logger.error(f"⚠️ Error guardando el estado de almacenamiento: {e}")

    async def close_browser(self):
        """Cierra el navegador y guarda las cookies antes de cerrar el contexto."""
        try:
            if self.context:
                # Guardar el estado de almacenamiento antes de cerrar el contexto
                await self.save_storage_state()
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