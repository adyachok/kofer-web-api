from typing import Any

from bson import ObjectId
from faust import web
# LOOK:
#   https://faust.readthedocs.io/en/latest/_modules/faust/web/blueprints.html
from src.models.faust_dao import ModelTask
from src.app import app, config
from src.utils.logger import get_logger


logger = get_logger('task-view')


@app.page('/task/')
class TaskListView(web.View):

    async def get(self, request: web.Request) -> web.Response:
        tasks = await config.mongo_repo.get_tasks()
        return self.json({'payload': [task.asdict() for task in tasks]})

    async def post(self, request: web.Request) -> web.Response:
        data: dict = await request.json()
        task = ModelTask.from_data(data)
        # todo: save task to db and to kafka
        result = await config.mongo_repo.create_task(task=task)
        if result and isinstance(result, ObjectId):
            task._id = str(result)
            await config.topics['model-tasks-do'].send(value=task)
            msg = f'Task {task._id} successfully submitted for processing.'
            logger.info(msg)
        else:
            msg = f'Task {task._id} was failed to submit.'
        return self.json({'payload': {
            'task_id': task._id
        }})


@app.page('/task/{task_id}/')
class TaskDetailView(web.View):

    async def get(self,
                  request: web.Request,
                  task_id: str) -> web.Response:
        task = await config.mongo_repo.find_task_by_id(task_id)
        return self.json({'payload': task.asdict() if task else None})
