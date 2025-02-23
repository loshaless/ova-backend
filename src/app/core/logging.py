import logging


def setup_logging():
    """Configures the application's logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )

if __name__ != "__main__": # Only configure if imported, not when run directly
    setup_logging()