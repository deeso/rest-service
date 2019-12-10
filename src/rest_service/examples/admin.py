from src.rest_service.models import BaseSqla, BaseDocument, BaseEmbeddedDocument
from src.rest_service.resources import BaseResource
from sqlalchemy import Column
import sqlalchemy as sqa_fields
from umongo import fields as umo_fields, validate
from quart import Response, request
import json

class PostgresAdmin(BaseSqla):
    uid = Column(sqa_fields.String(64), primary_key=True)
    username = Column(sqa_fields.String(4096), nullable=False)
    email = Column(sqa_fields.String(4096), nullable=False, unique=True)

# TODO create a class that encapsulates the business logic of user
# TODO create a class that encapsulates the resource of user
# TODO create a class that encapsulates the odm and orm object
class ExampleAdminORM(object):
    APPLICATION = None
    RESOURCE = None


class ExampleAdminRsrc(BaseResource):
    PATTERNS = ['/admin/id/<int:user_id>',
                '/admin/user/<str:username>',
                '/admin/add'
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


