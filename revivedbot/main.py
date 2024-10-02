import logging.config

from src.bot import Bot
from src.config import config

FORMAT = "%(levelname)s: %(message)s"


def main():
    logging.basicConfig(level=config["logging"]["level"], format=FORMAT),
    logging.getLogger("telegram.bot").setLevel(logging.ERROR)
    logging.getLogger("telegram.ext").setLevel(logging.ERROR)

    Bot().run()


if __name__ == "__main__":
    main()
