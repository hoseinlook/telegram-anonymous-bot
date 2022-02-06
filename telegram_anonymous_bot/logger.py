import logging.handlers

from .config import PATH_STORAGE

FORMAT = '%(asctime)s ==>%(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG,
                    datefmt='%Y-%m-%d:%H-%M-%S')
# error configs
log_file = PATH_STORAGE.joinpath('error_logs.txt')
handler = logging.handlers.RotatingFileHandler(
    log_file, maxBytes=20 * 1000 * 1000, backupCount=1, )
handler.setFormatter(logging.Formatter(FORMAT))
error_logger = logging.getLogger(str(log_file))
error_logger.propagate = True
error_logger.setLevel(logging.ERROR)
error_logger.addHandler(handler)

# info_log configs
TELEGRAM_LOG_LEVEL = 1000
log_file = PATH_STORAGE.joinpath('info_logs.txt')
handler = logging.handlers.RotatingFileHandler(
    log_file, maxBytes=20 * 1000 * 1000, backupCount=1, )
handler.setFormatter(logging.Formatter(FORMAT))
info_log = logging.getLogger(str(log_file))
info_log.propagate = True
info_log.setLevel(TELEGRAM_LOG_LEVEL)
info_log.addHandler(handler)
