#!/usr/bin/env python
import faust

from config import Config
from utils.logger import get_logger


logger = get_logger('app')


config = Config()

app = faust.App('web-api', broker=config.KAFKA_BROKER_URL,
                debug=True,
                web_port=8089,
                autodiscover=True,
                origin='src'
                )
config.init_app(app)


if __name__ == '__main__':
    app.main()
