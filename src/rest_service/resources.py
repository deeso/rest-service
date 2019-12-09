from quart_openapi import Resource
from quart import Response, jsonify, request
import json


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

    async def get(self):
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
    async def get(self):
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
    async def get(self):
        '''
        Get Example view
        '''
        return Response(json.dumps({'result': 'example works'}), status=300, mimetype='application/json')