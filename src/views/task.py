from typing import Any

from faust import web
# LOOK:
#   https://faust.readthedocs.io/en/latest/_modules/faust/web/blueprints.html
from src.app import app, config


# blueprint = web.Blueprint('tasks')


@app.page('/task/')
class TaskListView(web.View):

    async def get(self, request: web.Request) -> web.Response:
        tasks = await config.mongo_repo.get_tasks()
        return self.json({'payload': [task.asdict() for task in tasks]})

    async def post(self, request: web.Request) -> web.Response:
        data: Any = request.query['data']
        # todo: save task to db and to kafka
        return self.json({'payload': 'Task POST done!'})


@app.page('/task/{task_id}/')
class TaskDetailView(web.View):

    async def get(self,
                  request: web.Request,
                  task_id: str) -> web.Response:
        task = await config.mongo_repo.find_task_by_id(task_id)
        return self.json({'payload': task.asdict() if task else None})
