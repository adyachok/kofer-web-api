import json

from models.faust_dao import ModelMetadata
from src.app import app, config
from src.utils.logger import get_logger


logger = get_logger('zz-agents')


@app.agent(config.topics['model-metadata-updates'])
async def metadata_update_listener(updates):
    """Checks for new model metadata updates and saves them to MomgoDB
    :param updates: stream of ModelMetadata
    """
    async for update in updates:
        logger.info(f'Model {update.name} with version {update.latest_version}'
                    f' is updated.')
        prepared_update = _parse_business_metadata(update)
        if not prepared_update:
            logger.error(f'Update for model {update.name} cannot be saved.')
            continue
        logger.info(f'Is about to insert metadata {prepared_update.asdict()}')
        await config.mongo_repo.create_update_model_metadata(prepared_update)


def _parse_business_metadata(update: ModelMetadata) -> ModelMetadata:
    """ModelMetadata comes from TensorFlow Server as a dict {"outputs": str}.
    This function extracts string from the dict and decodes it back to JSON
    format.
    :param update: ModelMetadata
    :return: ModelMetadata
    """
    metadata = update.business_metadata.get('outputs')
    if not metadata:
        logger.error(f'No business metadata found for the '
                     f'model with name {update.name}.')
        return
    try:
        update.business_metadata = json.loads(metadata)
        return update
    except json.decoder.JSONDecodeError as e:
        logger.error(f'Model {update.name} cannot convert a business '
                     f'metadata to JSON format.')


@app.agent(config.topics['model-tasks-done'])
async def done_tasks_listener(tasks):
    """Checks for tasks to be done and saves result to MongoDB
    :param tasks: stream of ModelTask
    """
    async for task in tasks:
        logger.info(f'Task {task._id} for model name {task.model_name} '
                    f' is in state {task.state}.')
        # TODO: save task updates to MongoDB
        await config.mongo_repo.update_task(task)
