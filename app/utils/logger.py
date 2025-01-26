import logging
import logging.handlers

class Logger:

    _instance = None  # Class-level variable to store the single instance
    # _instance: naming convention for private class attribute(not actually private)

    # Class methods can access and modify class-level data
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()  # Create and store the instance
            # cls() calls the constructor (__init__), creating an instance of the class.
        return cls._instance
    
    def __init__(self):
        self.logger = logging.getLogger("Logster O_O")
        self.setup_logging()

    def setup_logging(self):
        LOG_FORMAT = "%(asctime)s - %(filename)s - %(name)s - %(levelname)s - %(message)s"
        logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

        #configure formatter
        formatter = logging.Formatter(LOG_FORMAT)

        #configure console handler
        console = logging.StreamHandler()
        console.setFormatter(formatter)

        #configure TimeRotatingFileHandler
        log_file = "logs/fastapi.log" 
        file = logging.handlers.TimedRotatingFileHandler(filename=log_file, when="midnight", backupCount=5)
        file.setFormatter(formatter)

        #add handlers
        self.logger.addHandler(console)
        self.logger.addHandler(file)   

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)