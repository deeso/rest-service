from quart_openapi import Resource
from quart import Response, request
from pymongo import MongoClient
from umongo import Instance
import json

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


# from https://www.anserinae.net/using-python-decorators-for-authentication.html
async def check_admin_token(fn):
    def deco(self, *args, **kwargs):
        token = request.headers.get('authorization', None)
        rsp = Response(json.dumps({'result': 'Admin token not valid'}), status=400, mimetype='application/json')
        if token is not None and self.auth_token(token) and \
                self.is_token_admin(token):
            rsp = fn(*args, **kwargs)
        return rsp
    return deco


async def check_token(fn):
    def deco(self, *args, **kwargs):
        token = request.headers.get('authorization', None)
        rsp = Response(json.dumps({'result': 'user token not valid'}), status=400, mimetype='application/json')
        if token is not None and self.is_token_admin(token):
            rsp = fn(*args, **kwargs)
        return rsp
    return deco


def patch_umongo_meta(odm_cls, **kargs):
    meta = getattr(odm_cls, 'Meta')
    if meta is None:
        return False
    connection = kargs.get('mongo_connection', None)
    database = kargs.get('mongo_database', None)
    collection = kargs.get('mongo_collection', None)

    instance = Instance(connection[database])
    if connection is not None and \
        isinstance(connection, MongoClient) and \
        database is not None and \
        collection is not None:
        col = connection[database][collection]
        setattr(odm_cls, 'Meta', col)

    if connection is not None and \
        isinstance(connection, MongoClient) and \
        database is not None:
        instance = instance.register(odm_cls)
        setattr(odm_cls, 'Meta', instance)
    return True


def patch_sqlalchemy_meta(sqla_cls, **kargs):
    table = getattr(sqla_cls, '__table__')
    if table is None:
        return False
    tablename = kargs.get('postgres_tablename', None)
    if table is not None:
        setattr(table, 'name', tablename)
        setattr(table, 'fullname', tablename)
        setattr(table, 'description', tablename)
    return True


class BaseSqla(Base):
    pass

class BaseResource(Resource):
    PATTERNS = ['/', ]
    CLASS_NAME = 'BaseResource'
    NAME = CLASS_NAME
    RESOURCE_HANDLER = None

    @property
    def handler(cls):
        return cls.RESOURCE_HANDLER

    @property
    def name(cls):
        return cls.NAME

    @classmethod
    def bind_application(cls, app):
        for pattern in cls.PATTERNS:
            app.add_url_rule(pattern,
                             view_func=cls.as_view(cls.NAME))

    @classmethod
    def urls(cls):
        r = []
        for i in cls.PATTERNS:
            r.append(i)
            r.append(cls.CLASS_NAME)
        return r

    @classmethod
    def bind_resource(cls, resource):
        cls.RESOURCE_HANDLER = resource

    @classmethod
    def check_can_handle(cls):
        if cls.RESOURCE_HANDLER is None:
            r = {'error': 'service handler not set'}
            return Response(json.dumps(r), status=400, mimetype='application/json')
        return None


class ExampleView(BaseResource):
    PATTERNS = ['/example', ]
    CLASS_NAME = 'ExampleView'
    NAME = CLASS_NAME
    RESOURCE_HANDLER = None

    async def get(self, *args, **kwargs):
        '''
        Get Example view
        '''
        return Response(json.dumps({'result': 'example works'}), status=300, mimetype='application/json')


class ExampleAdminView(BaseResource):
    PATTERNS = ['/example_admin', ]
    CLASS_NAME = 'ExampleAdminView'
    NAME = CLASS_NAME
    RESOURCE_HANDLER = None

    @check_admin_token
    async def get(self, *args, **kwargs):
        '''
        Get Example view
        '''
        return Response(json.dumps({'result': 'admin example works'}), status=300, mimetype='application/json')


class ExampleUserView(BaseResource):
    PATTERNS = ['/example_user', ]
    CLASS_NAME = 'ExampleUserView'
    NAME = CLASS_NAME
    RESOURCE_HANDLER = None

    @check_token
    async def get(self, *args, **kwargs):
        '''
        Get Example view
        '''
        return Response(json.dumps({'result': 'example works'}), status=300, mimetype='application/json')