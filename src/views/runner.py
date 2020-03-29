from faust import web

from src.app import app, config
from src.utils.logger import get_logger
from src.utils.web import to_camel_case

logger = get_logger('runner-view')


@app.page('/runner/')
class RunnerListView(web.View):

    async def get(self, request: web.Request) -> web.Response:
        runners = await config.mongo_repo.get_runners()
        return self.json({
            'payload': [to_camel_case(runner.asdict()) for runner in runners]})


@app.page('/runner/{runner_id}/')
class RunnerDetailView(web.View):

    async def get(self,
                  request: web.Request,
                  runner_id: str) -> web.Response:
        runner = await config.mongo_repo.find_runner_by_id(runner_id)
        return self.json({
            'payload': to_camel_case(runner.asdict()) if runner else None})
