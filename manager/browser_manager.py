import os
import json
from playwright.async_api import async_playwright

class BrowserManager:
    

    def __init__(self, headless: bool = False):
        """
        :param headless: Indica si el navegador debe ejecutarse en modo headless.
        """
        self.headless = headless
        self.browser = None
        self.context = None
        self.playwright = None  # Guardar la instancia de Playwright
        
    async def prepare_storage_state(self):
        """
        Verifica y crea un archivo de estado vacío si no existe.
        """
        if not os.path.exists(self.storage_state_path):
            print(f"Archivo {self.storage_state_path} no encontrado. Creando archivo vacío...")
            with open(self.storage_state_path, 'w') as file:
                json.dump({"cookies": [], "origins": []}, file)

    async def create_browser_context(self):
        """
        Crea el navegador y su contexto asociado.
        """
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)

        # Crear un contexto vacío (sin almacenamiento de cookies ni estado)
        self.context = await self.browser.new_context()
        return self.context, self.browser

    async def close_browser(self):
        """
        Cierra el navegador y su contexto asociado.
        Si el navegador ya está cerrado, no realiza ninguna acción.
        """
        try:
            if self.context:
                await self.context.close()
                print("✔ Contexto cerrado correctamente.")

            if self.browser:
                await self.browser.close()
                print("✔ Navegador cerrado correctamente.")

            # Cerrar Playwright
            if self.playwright:
                await self.playwright.stop()
                print("✔ Playwright detenido correctamente.")

        except Exception as e:
            print(f"⚠️ Error al cerrar el navegador o contexto: {e}")
