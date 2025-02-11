import logging
from utils.config import ZENDESK_USER, ZENDESK_PASSWORD, ZENDESK_URL, load_selectors
from logging_pages.logging_config import setup_logging

logger_server = logging.getLogger('main')

class LoginPage:
    def __init__(self, page, browser_manager=None):
        """
        Inicializa la página de login.
        :param page: Página de Playwright.
        :param browser_manager: Gestor del navegador (opcional).
        """
        self.page = page
        self.browser_manager = browser_manager
        self.selectors = load_selectors()["login"]

    async def clear_cache_and_cookies(self):
        """
        Limpia las cookies del navegador.
        """
        logger_server.info("🧹 Limpiando cookies...")
        await self.page.context.clear_cookies()  # Limpiar cookies

        # Forzar una recarga de la página para simular la limpieza de la caché
        logger_server.info("🧹 Recargando la página para limpiar la caché...")
        await self.page.reload()

    async def stage_login(self):
        """
        Realiza el proceso de inicio de sesión.
        :return: True si el login es exitoso, False si falla.
        """
        logger_server.info("🚀 Iniciando etapa de login...")
        try:
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
            logger_server.info("🔑 Seleccionando tipo de autenticación.")
            await self.page.click(self.selectors["button_not"])
            await self.page.click(self.selectors["button_call"])
            await self.page.click(self.selectors["button_day"])

            # Esperar que la página cargue completamente
            logger_server.info("⏳ Esperando que la red se estabilice después del inicio de sesión.")
            await self.page.wait_for_load_state("networkidle", timeout=15000)

            logger_server.info("✅ Interacciones completadas exitosamente.")
            return True

        except Exception as e:
            logger_server.error(f"❌ Error durante el login o interacciones: {e}")
            return False