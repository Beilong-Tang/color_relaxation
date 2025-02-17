import logging


def setup_logger(name):
    # Create a logger
    logger = logging.getLogger(name)  # You can name the logger whatever you like
    
    # Set the log level
    logger.setLevel(logging.DEBUG)
    
    # Create a stream handler (to output logs to console)
    console_handler = logging.StreamHandler()
    
    # Set the log level for the handler
    console_handler.setLevel(logging.DEBUG)
    
    # Create a formatter and set it for the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    # Add the handler to the logger
    logger.addHandler(console_handler)

    return logger
