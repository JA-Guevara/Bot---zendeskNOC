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
            "button_not": 'a[aria-describedby="idDiv_SAOTCAS_Title idDiv_SAOTCAS_Description"]',  
            "button_call": '#idDiv_SAOTCS_Proofs > div:nth-child(5) > div > div > div.table-cell.text-left.content', 
            "button_day": '#idChkBx_SAOTCC_TD',
            "logged_button": '#idSIButton9',  # Botón de "Inicio" en la barra de navegación
            "show_button": '#KmsiCheckboxField',  # Botón de "Mostrar contraseña"
            "welcome_message": '#ember2620 > div > nav > div.StyledBaseNavItem-sc-zvo43f-0.StyledLogoNavItem-sc-saaydx-0.gvFgbC.bdDIaV.sc-19et275-0.kpIgbf',
            
            },  
        "zendesk": {

            "vistas_button": '[data-test-id="views_icon"]',  # Botón de "Vistas" en la barra lateral
            "butthon_NOCTier1": 'a[data-test-id="views_views-tree_item-view-28175453910675"] .sc-gxrqff-0.htlang',  # Vista de tickets NOC Tier 1
            "acciones_button": 'button[data-test-id="views_views-header-options-button"]',  # Botón de "Acciones" en la vista de tickets
            "exportar_button": 'li[data-test-id="views_views-header-row-option-export-as-csv"]',  # Botón de "Exportar" en la vista de tickets
            
            }, 
        "outlook": {
            "report_button": 'div[data-folder-name="reporte zendesk"]',  # Botón de "ReportES" 
            "recent_button": '(//div[contains(@class, "jGG6V gDC9O")])[1]',  # Botón de para correo mas reciente
            "buthon_descargar": 'a[href*="expirable_attachments/token"][data-auth="NotApplicable"]',  # Botón de "Exportar" en la vista de tickets
            
            },      
    }

def get_environment():
    return os.getenv("ENVIRONMENT", "development")
