import logging

class ColorFormatter(logging.Formatter):
    # Codes ANSI
    RESET = "\033[0m"
    GREY = "\033[90m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"

    LEVEL_COLORS = {
        logging.DEBUG: CYAN,
        logging.INFO: GREEN,
        logging.WARNING: YELLOW,
        logging.ERROR: RED,
        logging.CRITICAL: RED
    }

    def format(self, record):
        # Définir les couleurs
        level_color = self.LEVEL_COLORS.get(record.levelno, self.RESET)
        time_color = self.GREY
        message_color = self.RESET  # message brut en couleur par défaut

        # Appliquer le format avec les couleurs séparées
        log_time = time_color + self.formatTime(record, "%Y-%m-%d %H:%M:%S") + self.RESET
        log_level = level_color + record.levelname + self.RESET
        message = message_color + record.getMessage() + self.RESET

        return f"{log_time} - {log_level} - {message}"