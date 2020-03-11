#!/usr/bin/env python
import asyncio
import json
import os

import faust

from config import Config
from utils.logger import get_logger

from models.faust_dao import ModelMetadata, ModelTask
from views import task

logger = get_logger('app')

config = Config()

app = faust.App('scanner', broker=config.KAFKA_BROKER_URL, debug=True)
model_metadata_updates_topic = app.topic('model-metadata-updates',
                                         value_type=ModelMetadata)
model_tasks_do = app.topic('model-tasks-do', value_type=ModelTask)
model_tasks_done = app.topic('model-tasks-done', value_type=ModelTask)


@app.agent(model_metadata_updates_topic)
async def scan(updates):
    """Checks from new updates, picks one and gathers model's metadata.
    :param dc_infos: stream of DeploymentConfigInfo
    """
    async for update in updates:
        logger.info(f'Model {update.name} with version {update.latest_version}'
                    f' is updated.')
        # TODO: save model updates to MongoDB


@app.agent(model_tasks_done)
async def scan(tasks):
    """Checks from new updates, picks one and gathers model's metadata.
    :param dc_infos: stream of DeploymentConfigInfo
    """
    async for task in tasks:
        logger.info(f'Task {task.id} for model {task.model_name} and version '
                    f'{task.latest_version} is done.')
        # TODO: save task updates to MongoDB


task.blueprint.register(app, url_prefix='/task/')


if __name__ == '__main__':
    app.main()
