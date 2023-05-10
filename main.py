
from logging import Logger, getLogger

from src.components.application import Application

logger: Logger = getLogger(name=__name__)

if __name__ == '__main__':
    app: Application = Application()
    try:
        app.mainloop()
    except Exception:
        logger.exception(msg='Fatal error occurred when running calculator application')
