import asyncio
from utils.config import  OUTLOOK_URL, load_selectors
import logging

logger_server = logging.getLogger('main')

class OutlookPage:
    def __init__(self, page):
        self.page = page
        self.selectors = load_selectors()["outlook"]
    
    # Async method to extract issues
    async def outlook_extraction(self):
        try:
            
            await self.page.goto(OUTLOOK_URL)
            # Perform the clicks using the selectors
            
            logger_server.info("📩📤iniciando proceso en outlook.")
            
            await self.page.click(self.selectors["report_button"])
            await self.page.click(self.selectors["recent_button"])
            await self.page.click(self.selectors["buthon_descargar"])
            
            
            
            
        except Exception as e:
            logger_server.error(f"⚠️ Error al procesar en outlook: {e}")