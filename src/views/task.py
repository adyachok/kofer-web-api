from typing import Any

from faust import web
# LOOK:
#   https://faust.readthedocs.io/en/latest/_modules/faust/web/blueprints.html


blueprint = web.Blueprint('tasks')


@blueprint.route('/', name='list')
class TaskListView(web.View):

    async def get(self, request: web.Request) -> web.Response:
        return self.json({'hi': 'There!'})

    async def post(self, request: web.Request) -> web.Response:
        data: Any = request.query['data']
        return self.json({'hi': 'There!'})


@blueprint.route('/{task_id}/', name='detail')
class TaskDetailView(web.View):

    async def get(self,
                  request: web.Request,
                  task_id: str) -> web.Response:
        return self.json({'Bye': 'Here'})
