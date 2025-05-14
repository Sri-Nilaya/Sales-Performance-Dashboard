import logging
import os

class LoggerManager():
    """
    A class to manage logging for the application.
    """

    def __init__(self, logger_name, log_level, log_file_name):
        """
        Initializes the LoggerManager with the specified logger name, log level, and log file name.

        :param logger_name: Name of the logger.
        :param log_level: Logging level (e.g., logging.INFO, logging.DEBUG).
        :param log_file_name: Name of the log file (without extension).
        """
        self.log_level = log_level
        self.log_file_name = log_file_name
        self.logger_name = logger_name
        self.logger = None  # Placeholder for the logger instance

    def get_logger(self):
        """
        Configures and returns a logger instance with file and stream handlers.

        :return: Configured logger instance.
        """
        # Create or retrieve the logger instance
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(self.log_level)  # Set the logging level

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        #  Create 'logs' folder in current working directory
        logs_dir = os.path.join(os.getcwd(), 'logs')  
        os.makedirs(logs_dir, exist_ok=True)       

        #  Full log file path inside 'logs' directory
        log_file_path = os.path.join(logs_dir, f"{self.log_file_name}.log")  

        # CHANGED: Use full log file path instead of just filename
        file_handler = logging.FileHandler(log_file_path) 

        # Create a stream handler to output logs to the console
        stream_handler = logging.StreamHandler()

        # Set the formatter for both handlers
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        # Add handlers to the logger if they are not already added
        if not self.logger.hasHandlers():
            self.logger.addHandler(file_handler)
            self.logger.addHandler(stream_handler)

        return self.logger  # Return the configured logger