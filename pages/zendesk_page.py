import asyncio
from utils.config import load_selectors
import logging

logger_server = logging.getLogger('main')

class ZendeskPage:
    def __init__(self, page):
        self.page = page
        self.selectors = load_selectors()["zendesk"]
    
    # Async method to extract issues
    async def zendesk_extraction(self):
        try:
            # Perform the clicks using the selectors
            
            logger_server.info("⏳ iniciando proceso en zendesk.")
            await self.page.click(self.selectors["vistas_button"])
            await self.page.click(self.selectors["butthon_NOCTier1"])
            await self.page.click(self.selectors["acciones_button"])
            await self.page.click(self.selectors["exportar_button"])
            
            await asyncio.sleep(60)
            return True
            
        except Exception as e:
            logger_server.error(f"⚠️ Error al procesar en zendesk: {e}")
            return False
