import json
import os
import logging
from utils.config import ZENDESK_USER, ZENDESK_PASSWORD, ZENDESK_URL,OUTLOOK_URL, load_selectors
from logging_pages.logging_config import setup_logging

logger_server = logging.getLogger('main')

class LoginPage:
    def __init__(self, page, browser_manager=None):
        self.page = page
        self.browser_manager = browser_manager
        self.selectors = load_selectors()["login"]
        
        async def stage_login(self):
            logger_server.info("🚀 Iniciando etapa de login...")
            try:
                # Limpiar caché y cookies
                logger_server.info("🧹 Limpiando caché y cookies...")
                await self.clear_cache_and_cookies()

                # Navegar a la página de login
                logger_server.info(f"🌍 Navegando a {ZENDESK_URL}...")
                await self.page.goto(ZENDESK_URL)

                # Rellenar el formulario de login
                logger_server.info("🔑 Rellenando usuario y contraseña.")
                await self.page.fill(self.selectors["email_field"], ZENDESK_USER)
                await self.page.fill(self.selectors["email_password_field"], ZENDESK_PASSWORD)

                # Localizar y hacer clic en los botones de inicio de sesión
                logger_server.info("✅ Localizando y presionando botones de inicio de sesión.")
                await self.page.wait_for_selector(self.selectors["submit_button"])
                await self.page.click(self.selectors["submit_button"])
                await self.page.click(self.selectors["login_button"])

                # Esperar que la página cargue completamente antes de continuar
                logger_server.info("⏳ Esperando que la red se estabilice después del inicio de sesión.")
                await self.page.wait_for_load_state("networkidle", timeout=15000)

                # Iniciar las interacciones posteriores al login
                logger_server.info("🔄 Realizando interacciones posteriores al login.")

                # Presionar el botón de cancelación de entrantes (starters_button)
                logger_server.info("🛑 Presionando el botón de cancelación de entrantes.")
                await self.page.click(self.selectors["starters_button"])


                logger_server.info("✅ Interacciones completadas exitosamente.")

                # # **Descanso de 10 segundos para revisión**
                # logger_server.info("⏳ Pausando 5 segundos para revisión...")
                # await self.page.wait_for_timeout(5000)  # 5 segundos

                return True
            
            except Exception as e:
                logger_server.error(f"❌ Error durante el login o interacciones: {e}")
                return False