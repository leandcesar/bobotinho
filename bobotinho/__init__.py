from bobotinho.config import config
from bobotinho.logger import Log

__title__ = "bobotinho-bot"
__author__ = "Leandro César"
__license__ = "GNU"
__copyright__ = "Copyright 2020 bobotinho"
__version__ = config.version

log = Log(
    filename=config.log_filename,
    level=config.log_level,
    bugsnag={"key": config.bugsnag_key, "version": __version__, "stage": config.stage},
)
