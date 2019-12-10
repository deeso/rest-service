
class BaseController(object):

    APPLICATION = None
    RESOURCE = None
    ENVIRONMENT = {}

    @classmethod
    def set_resource_class(cls, rsrc_class):
        # enable access to the Class of the caller
        cls.RESOURCE = rsrc_class

    @classmethod
    def set_application(cls, app_instance):
        # enable access to application resources
        cls.APPLICATION = app_instance

    async def get(self, *args, **kwargs):
        raise Exception("Not implemented")

    async def post(self, *args, **kwargs):
        raise Exception("Not implemented")

    async def put(self, *args, **kwargs):
        raise Exception("Not implemented")

    async def delete(self, *args, **kwargs):
        raise Exception("Not implemented")
