import os
import yaml
import logging
import logging.config


def setup_default_logger(level):
    FORMAT = "[%(asctime)s] %(levelname)-8s: %(message)s"
    DATEFMT = "%Y%m%d %H:%M:%S"
    logging.basicConfig(level=level, format=FORMAT, datefmt=DATEFMT)


def setup_logger_failed_message(msg):
    log = logging.getLogger()
    log.warn(msg)


def setup_logger(log_config, default_level=logging.INFO):
    if log_config:
        with open(log_config, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)

            except Exception as e:
                # import traceback
                # traceback.print_exc()
                setup_default_logger(default_level)
                msg = ('Failed to setup by config file, using basic config \n\t'
                       'Exception: {}').format(str(e))
                setup_logger_failed_message(msg)
    else:
        setup_default_logger(default_level)
        msg = 'Log config not found, using basic config'
        setup_logger_failed_message(msg)


class SetLogDirRotatingFileHandler(logging.handlers.RotatingFileHandler):
    def __init__(self, logBaseDir, filename, maxBytes=20 * 1024 * 1024, backupCount=5):
        os.makedirs(logBaseDir, exist_ok=True)
        super().__init__(os.path.join(logBaseDir, filename), maxBytes=maxBytes, backupCount=backupCount)
