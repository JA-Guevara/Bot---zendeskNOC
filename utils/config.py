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

            # Primera etapa: Login de correo
            "email_field": '#i0116',  # Campo de correo electrónico
            "email_password_field": '#i0118',  # Campo de contraseña del correo
            "submit_button": 'input#idSIButton9',  # Botón "Siguiente" en el primer login
            "login_button": '#idSIButton9',  # Botón "Iniciar sesión" (primera etapa)
            "button_not": '#idDiv_SAOTCS_HavingTrouble',  
            "button_call": '#idDiv_SAOTCS_Proofs > div:nth-child(5) > div > div > div.table-cell.text-left.content', 
            "button_day": '#idChkBx_SAOTCC_TD',
            
            },   
    }

def get_environment():
    return os.getenv("ENVIRONMENT", "development")
