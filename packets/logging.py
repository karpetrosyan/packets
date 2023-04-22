from logging import config

logger_config = {
    "version": 1,
    "handlers": {
        "packets-stream": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "DEBUG",
            "stream": "ext://sys.stderr",
        },
    },
    "formatters": {
        "standard": {
            "format": "%(levelname)s [%(module)s:%(lineno)d]"
            " [%(asctime)s] %(name)s - %(message)s"
        }
    },
    "loggers": {
        "packets": {
            "handlers": ["packets-stream"],
            "level": "INFO",
            "propagate": False,
        }
    },
}

config.dictConfig(logger_config)