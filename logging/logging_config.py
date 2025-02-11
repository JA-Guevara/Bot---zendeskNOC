import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
import os


# # Validar valores de entorno con valores predeterminados
# MAILHOST = os.getenv('MAILHOST', 'smtp.office365.com')
# MAILPORT = os.getenv('MAILPORT', '587')
# MAILORIGEN = os.getenv('MAILORIGEN', 'a.bazan@conecta.com.bo')
# EMAIL = os.getenv('EMAIL', 'a.bazan@conecta.com.bo')
# CLAVE = os.getenv('CLAVE', 'Passw0rd19****')
# DESTINATARIOS = os.getenv('DESTINATARIOS', 'l.torricos@conecta.com.bo,jr.guarachi@conecta.com.bo')
# DESTINATARIOS2 = os.getenv('DESTINATARIOS2', 'sylvia.terrazas@conecta.com.bo,r.aro@conecta.com.bo,ralgaranaz@conecta.com.bo,l.torricos@conecta.com.bo')
# LISTA = [email.strip() for email in DESTINATARIOS.split(',')]
# LISTA2 = [email.strip() for email in DESTINATARIOS2.split(',')]


# Constantes para la configuración de logging
LOG_DIR = os.path.join('logging', 'logs')
SERVER_LOG_PATH = os.path.join(LOG_DIR, 'server.log')
MAX_LOG_SIZE = 90 * 1024 * 1024  # 90 MB
BACKUP_COUNT = 3
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = logging.INFO


class UTF8RotatingFileHandler(RotatingFileHandler):
    def _open(self):
        return open(self.baseFilename, self.mode, encoding='utf-8')


# class InfoFilter(logging.Filter):
#     """Filtro para detectar mensajes específicos de nivel INFO."""
#     def filter(self, record):
#         return record.levelname == 'INFO' and 'Iniciando proceso speech_analitycs_cobranzas' in record.msg.strip()


def setup_logging():
    # Crear el directorio de logs si no existe
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Configuración del logging general
    logging.basicConfig(level=LOG_LEVEL)

 
    # Configuración del logger para el servidor
    logger_server = logging.getLogger('main')
    handler_server = UTF8RotatingFileHandler(SERVER_LOG_PATH, maxBytes=MAX_LOG_SIZE // 2, backupCount=BACKUP_COUNT)
    handler_server.setLevel(LOG_LEVEL)
    formatter_server = logging.Formatter(LOG_FORMAT)
    handler_server.setFormatter(formatter_server)
    logger_server.addHandler(handler_server)
    logger_server.propagate = False

    # # Configuración del SMTPHandler para enviar correos electrónicos en caso de error
    # mail_handler_error = SMTPHandler(
    #     mailhost=(MAILHOST, int(MAILPORT)),
    #     fromaddr=MAILORIGEN,
    #     toaddrs=LISTA,
    #     subject='Error en speech_analitycs_cobranzas',
    #     credentials=(EMAIL, CLAVE),
    #     secure=()
    # )
    # mail_handler_error.setLevel(logging.ERROR)
    # mail_handler_error.setFormatter(formatter_server)
    # logger_server.addHandler(mail_handler_error)

    # # Configuración del SMTPHandler para mensajes INFO específicos
    # mail_handler_info = SMTPHandler(
    #     mailhost=(MAILHOST, int(MAILPORT)),
    #     fromaddr=MAILORIGEN,
    #     toaddrs=LISTA2,
    #     subject='ALERTA: INICIANDO SPEECH ANALITYCS COBRANZAS',
    #     credentials=(EMAIL, CLAVE),
    #     secure=()
    # )
    # mail_handler_info.setLevel(logging.INFO)
    # mail_handler_info.setFormatter(formatter_server)
    # mail_handler_info.addFilter(InfoFilter())  # Se añade el filtro personalizado
    # logger_server.addHandler(mail_handler_info)




