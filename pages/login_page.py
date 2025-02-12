import os
import asyncio
import json
import logging
from utils.config import ZENDESK_USER, ZENDESK_PASSWORD, ZENDESK_URL, load_selectors
from logging_pages.logging_config import setup_logging

logger_server = logging.getLogger('main')

class LoginPage:
    def __init__(self, page, browser_manager=None):
        self.page = page
        self.browser_manager = browser_manager
        self.selectors = load_selectors()["login"]

    async def clear_cache_and_cookies(self):
        """Limpia las cookies y recarga la página para simular la limpieza de la caché."""
        logger_server.info("🧹 Limpiando cookies...")
        await self.page.context.clear_cookies()  # Limpiar cookies

        # Forzar una recarga de la página para simular la limpieza de la caché
        logger_server.info("🧹 Recargando la página para limpiar la caché...")
        await self.page.reload()

    async def verify_cookies(self):
        """Verifica si las cookies son válidas y si hay una sesión activa."""
        cookies_exist = os.path.exists("user_data.json")
        cookies_valid = False

        if cookies_exist:
            try:
                with open("user_data.json", "r") as file:
                    storage_data = json.load(file)
                    cookies = storage_data.get("cookies", [])
                    cookies_valid = bool(cookies)

                    # Cargar las cookies en el contexto del navegador
                    if cookies_valid:
                        await self.page.context.add_cookies(cookies)
                        logger_server.info("✅ Cookies cargadas en el contexto del navegador.")
            except Exception as e:
                logger_server.error(f"⚠️ Error leyendo archivo de cookies: {e}")

        if cookies_valid:
            logger_server.info("✅ Cookies válidas encontradas. Verificando sesión activa...")
            
            # Intentar cargar la página para verificar si realmente hay sesión activa
            await self.page.goto(ZENDESK_URL)
            
            # Esperar a que la página cargue completamente
            await self.page.wait_for_load_state("networkidle")

            # Verificar si el usuario está autenticado
            try:
                await self.page.wait_for_selector(self.selectors["welcome_message"], timeout=5000)
                logger_server.info("✅ Sesión activa confirmada.")
                return True
            except Exception as e:
                logger_server.info("🔄 Las cookies no son válidas. Iniciando sesión desde cero...")
                return False

        return False

    async def save_session_state(self):
        """Guarda el estado de la sesión (cookies y datos) en un archivo JSON."""
        try:
            storage_state = await self.page.context.storage_state()
            with open("user_data.json", "w") as file:
                json.dump(storage_state, file)
            logger_server.info("✅ Estado de sesión guardado en 'user_data.json'.")
        except Exception as e:
            logger_server.error(f"⚠️ Error guardando el estado de sesión: {e}")

    async def stage_login(self):
        """Maneja el proceso completo de inicio de sesión."""
        logger_server.info("🚀 Iniciando etapa de login...")
        try:
            # Verificar si las cookies son válidas
            cookies_valid = await self.verify_cookies()

            if not cookies_valid:
                logger_server.info("🔄 No se encontraron cookies válidas. Iniciando sesión desde cero...")

                # Limpiar cookies y recargar la página
                await self.clear_cache_and_cookies()

                # Navegar a la página de login
                logger_server.info(f"🌍 Navegando a {ZENDESK_URL}...")
                await self.page.goto(ZENDESK_URL)

                # Rellenar el formulario de login
                logger_server.info("🔑 Rellenando usuario y contraseña.")
                await self.page.fill(self.selectors["email_field"], ZENDESK_USER)
                await self.page.click(self.selectors["submit_button"])
                await self.page.fill(self.selectors["email_password_field"], ZENDESK_PASSWORD)
                await self.page.click(self.selectors["login_button"])

                # Seleccionar tipo de autenticación
                logger_server.info("🔏 Seleccionando tipo de autenticación...")
                await self.page.click(self.selectors["button_not"])
                await self.page.click(self.selectors["button_call"])
                await self.page.click(self.selectors["button_day"])
                
                await asyncio.sleep(30)
                
                await self.page.click(self.selectors["show_button"])
                await self.page.click(self.selectors["logged_button"])

                # Esperar que la página cargue completamente
                logger_server.info("⏳ Esperando que la red se estabilice después del inicio de sesión.")
                await self.page.wait_for_load_state("networkidle", timeout=3000)

                # Guardar el estado de sesión (cookies y datos)
                await self.save_session_state()

            logger_server.info("✅ Interacciones completadas exitosamente.")
            return True

        except Exception as e:
            logger_server.error(f"❌ Error durante el login o interacciones: {e}")
            return False