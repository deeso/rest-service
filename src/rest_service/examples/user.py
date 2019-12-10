from src.rest_service.models import BaseSqla, BaseDocument, BaseEmbeddedDocument
from src.rest_service.resources import BaseResource
from sqlalchemy import Column
import sqlalchemy as sqa_fields
from umongo import fields as umo_fields, validate
from quart import Response, request
import json

class MongoUser(BaseDocument):
    uid = umo_fields.StrField(attribute='_id')
    username = umo_fields.StringField(required=True)
    email = umo_fields.EmailField(required=True, unique=True)

# TODO create a class that encapsulates the business logic of user
# TODO create a class that encapsulates the resource of user
# TODO create a class that encapsulates the odm and orm object
class ExampleUserODM(object):
    APPLICATION = None
    RESOURCE = None


class ExampleUserRsrc(BaseResource):
    PATTERNS = ['/user/id/<int:user_id>',
                '/user/user/<str:username>',
                '/user/add'
                ]

    async def get(self, *args, **kwargs):
        '''
        Get Example view
        '''
        return Response(json.dumps({'result': 'admin example works'}), status=300, mimetype='application/json')


    async def post(self, *args, **kwargs):
        '''
        Get Example view
        '''
        return Response(json.dumps({'result': 'admin example works'}), status=300, mimetype='application/json')

    async def put(self, *args, **kwargs):
        '''
        Get Example view
        '''
        return Response(json.dumps({'result': 'admin example works'}), status=300, mimetype='application/json')

    async def delete(self, *args, **kwargs):
        '''
        Get Example view
        '''
        return Response(json.dumps({'result': 'admin example works'}), status=300, mimetype='application/json')

