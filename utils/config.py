import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

ZENDESK_USER=  os.getenv("ZENDESK_USER") 
ZENDESK_PASSWORD=  os.getenv("ZENDESK_PASSWORD") 
ZENDESK_URL=  os.getenv("ZENDESK_URL") 
OUTLOOK_URL=  os.getenv("OUTLOOK_URL")

def load_selectors():

    return {
        "login": {

            "end_button": "button.q-btn:has(span.block:has-text('Terminar'))"

            
            },   
    }

def get_environment():
    return os.getenv("ENVIRONMENT", "development")
