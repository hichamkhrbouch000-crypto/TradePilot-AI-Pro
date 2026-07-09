import logging
from logging.handlers import RotatingFileHandler

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # تنسيق الرسائل (الوقت - المستوى - الرسالة)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # ملف للأخطاء فقط (Error.log)
    error_handler = RotatingFileHandler('errors.log', maxBytes=1000000, backupCount=3)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    
    # ملف لكل شيء (App.log)
    app_handler = RotatingFileHandler('app.log', maxBytes=1000000, backupCount=3)
    app_handler.setLevel(logging.INFO)
    app_handler.setFormatter(formatter)
    
    logger.addHandler(error_handler)
    logger.addHandler(app_handler)
    
    return logger
