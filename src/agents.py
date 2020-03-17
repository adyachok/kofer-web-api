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
        # TODO: save model updates to MongoDB
        logger.info(f'Is about to insert metadata {update.asdict()}')
        await config.mongo_repo.create_update_model_metadata(update)


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
