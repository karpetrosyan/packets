from logging import config

logger_config = {
    "version": 1,
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO",
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
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        }
    },
}

config.dictConfig(logger_config)
