from django_log_formatter_asim import ASIMFormatter

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "asim_formatter": {
            "()": ASIMFormatter,
        },
    },
    "handlers": {
        "asim": {"class": "logging.StreamHandler", "formatter": "asim_formatter"},
    },
    "root": {
        "handlers": ["asim"],
    },
    "loggers": {
        "django": {"handlers": ["asim"], "propagate": False},
    },
}
