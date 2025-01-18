import logging
import logging.handlers

class Logger:
    def __init__(self):
        self.logger = logging.getLogger(" ")
        self.setup_logging()

    def setup_logging(self):
        LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
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