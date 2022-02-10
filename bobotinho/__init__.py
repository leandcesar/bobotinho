from bobotinho.config import config
from bobotinho.logger import Log

log = Log(
    filename=config.log_filename,
    bugsnag={"key": config.bugsnag_key, "version": __version__, "stage": config.mode},
)

__title__ = "bobotinho-bot"
__author__ = "Leandro César"
__license__ = "GNU"
__copyright__ = "Copyright 2020 bobotinho"
__version__ = config.version
