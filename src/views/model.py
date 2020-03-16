from typing import Any

from faust import web
# LOOK:
#   https://faust.readthedocs.io/en/latest/_modules/faust/web/blueprints.html
from src.app import app, config


# blueprint = web.Blueprint('models')


@app.page('model/', name='list')
class ModelListView(web.View):

    async def get(self, request: web.Request) -> web.Response:
        models = await config.mongo_repo.get_models()
        # TODO: get list of models
        return self.json({'payload': [model.asdict() for model in models]})

    async def post(self, request: web.Request) -> web.Response:
        data: Any = request.query['data']
        # TODO: Verify and save data
        return self.json({'payload': 'Your model was created'})


@app.page('model/{model_id}/', name='detail')
class ModelDetailView(web.View):

    async def get(self,
                  request: web.Request,
                  model_id: str) -> web.Response:
        model = await config.mongo_repo.find_model_metadata_by_id(model_id)
        return self.json({'payload': model.asdict() if model else None})
