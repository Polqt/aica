import logging

class JSONFormatter(logging.Formatter):
    def format(self, record):
        return super().format(record)

def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logging.getLogger().handlers[0].setFormatter(JSONFormatter())
