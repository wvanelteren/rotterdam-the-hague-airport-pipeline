import logging


def setup_logger(logger_name, level=logging.DEBUG):
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
    file_handler = logging.FileHandler(f"{logger_name}.log", mode="w")
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger


logger = setup_logger("rth-data-pipeline")
