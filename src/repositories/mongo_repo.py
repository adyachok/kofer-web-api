from bson import ObjectId

from src.models.faust_dao import ModelMetadata, ModelTask
from src.utils.logger import get_logger


logger = get_logger('mongo-repo')


class BaseMongoRepository:

    def __init__(self, db):
        self.db = db

    async def convert_id(method):
        async def inner(*args, **kwargs):
            doc = await method(*args, **kwargs)
            if doc:
                doc['_id'] = str(doc.get('_id'))
            return doc
        return inner

    async def do_insert(self, collection, document):
        document.pop('_id', None)
        result = await self.db[collection].insert_one(document)
        # returns ObjectId object
        return result.inserted_id

    async def do_find_one(self, collection, condition):
        doc = await self.db[collection].find_one(condition)
        if doc:
            doc['_id'] = str(doc.get('_id'))
        return doc

    async def do_find_all(self, collection):
        cursor = self.db[collection].find()
        async for document in cursor:
            document['_id'] = str(document.get('_id'))
            yield document

    async def do_update(self, collection, _id, document):
        document.pop('_id', None)
        result = await self.db[collection].replace_one(
            {'_id': ObjectId(_id)}, document)
        return result.matched_count, result.modified_count


class MongoRepository(BaseMongoRepository):

    async def create_update_model_metadata(self, metadata):
        collection = 'model_metadata'
        assert isinstance(metadata, ModelMetadata)
        old_doc = await self.do_find_one(collection, {'name': metadata.name})
        if old_doc:
            _id = old_doc.get('_id')
            metadata._id = _id
            matched_count, updated_count = await self.do_update(
                collection, _id, metadata.asdict())
            if matched_count and updated_count and \
                    matched_count == updated_count:
                logger.info(f'Model {metadata.name} was successfully updated.')
            else:
                logger.info(f'Model {metadata.name} update fail.')
        else:
            return await self.do_insert(collection, metadata.asdict())

    async def create_task(self, task):
        collection = 'tasks'
        assert isinstance(task, ModelTask)
        return await self.do_insert(collection, task.asdict())

    async def update_task(self, task):
        collection = 'tasks'
        assert isinstance(task, ModelTask)
        doc = await self.find_task_by_id(task.id)
        if not task:
            raise Exception(f'Task with id {task.id} not found.')
        matched_count, updated_count = await self.do_update(
            collection, doc.get('_id'), task.asdict())
        if matched_count and updated_count and \
                matched_count == updated_count:
            logger.info(f'Task {task.id} was successfully updated.')
        else:
            logger.info(f'Task {task.id} update fail.')

    async def find_task_by_id(self, task_id):
        return await self.do_find_one('tasks', {'_id': ObjectId(task_id)})

    async def find_model_metadata_by_id(self, model_id):
        model = await self.do_find_one('model_metadata',
                                       {'_id': ObjectId(model_id)})
        return ModelMetadata.from_data(model)

    async def get_tasks(self):
        tasks = []
        async for task in self.do_find_all('tasks'):
            tasks.append[ModelTask.from_data(task)]
        return tasks

    async def get_models(self):
        models = []
        async for model_metadata in self.do_find_all('model_metadata'):
            models.append(ModelMetadata.from_data(model_metadata))
        return models
