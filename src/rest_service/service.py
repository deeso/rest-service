from .config import Config
from .consts import *
from .standard_logger import Logger
from quart_openapi import Pint
from .db import DBSettings
import importlib
import traceback
from flask_sqlalchemy import SQLAlchemy


class RestService(object):
    DEFAULT_VALUES = REST_SERVICE_CONFIGS
    NAME = REST_SERVICE_BLOCK

    def __init__(self, **kwargs):
        self.init_keys = set()

        for k, v in kwargs.items():
            setattr(self, k, v)
            self.init_keys.add(k)

        for k, v in self.DEFAULT_VALUES.items():
            if k not in kwargs:
                setattr(self, k, v)
            else:
                setattr(self, k, kwargs.get(k))

        self.logger = Logger(self.NAME)

        self.app = Pint(self.NAME)
        self.app.config.update(DBSettings.get_mongo_config(**kwargs))
        self.app.config.update(DBSettings.get_postgres_config(**kwargs))

        self.mongddb = None
        self.postgresdb = None

        #TODO figure out how to distinguish between Models in Mongo and Postgres
        if self.get_using_mongo():
            self.mongddb = SQLAlchemy(self.app)
        if self.get_using_postgres():
            self.postgresdb = SQLAlchemy(self.app)

        self.views = []

        if isinstance(kwargs.get(VIEWS, list()), list):
            for v in kwargs.get(VIEWS, list()):
                self.import_add_view(v)

    def import_add_view(self, fq_python_class_view: str) -> bool:
        '''
        Import a module and load the class for a provided view
        :param view: Python module in dot'ted notation, e.g. `foo.views.ViewX`
        :return: bool
        '''

        blah = fq_python_class_view.split('.')
        if len(blah) <= 1:
            raise Exception("Expecting a python_module.Class got {}".format(view))

        mn = '.'.join(blah[:-1])
        cn = blah[-1]
        mi = None
        python_class = None

        try:
            mi = importlib.import_module(mn)
        except:
            msg = "{} is not a valid Python module: \n{}".format(mn, traceback.format_exc())
            raise Exception(msg)

        try:
            python_class = getattr(mn, cn, None)
        except:
            msg = "{} is not a valid Python class in {}: \n{}".format(cn, mn, traceback.format_exc())
            raise Exception(msg)

        self.add_view(python_class)
        return True

    @classmethod
    def from_config(cls):

        cdict = Config.get_value(REST_SERVICE_BLOCK)
        if cdict is None:
            cdict = {}

        kwargs = {}
        for k, v in cls.DEFAULT_VALUES.items():
            kwargs[k] = cdict.get(k, v)
        return cls(**kwargs)

    def run(self, debug=False):
        ssl_context = None
        if self.get_key_pem() is not None and \
                self.get_cert_pem() is not None:
            ssl_context = (self.get_cert_pem(), self.get_key_pem())

        if self.get_use_uwsgi():
            return self.app.run(port=self.get_listening_port(),
                                host=self.get_listening_host(),
                                debug=debug,
                                ssl_context=ssl_context)
        return self.app.run(port=self.get_listening_port(),
                            host=self.get_listening_host(),
                            debug=debug,
                            ssl_context=ssl_context)

    def has_view(self, view):
        if view is not None:
            return view.name in set([i.name for i in self.views])
        return False

    def get_json(self, the_request):
        try:
            return the_request.json()
        except:
            return None

    def add_view(self, view):
        self.views.append(view)
        view.update_app(self.app)

    def get_using_postgres(self):
        return getattr(self, USING_POSTGRES, False)

    def get_using_mongo(self):
        return getattr(self, USING_MONGO, False)

    def get_listening_host(self):
        return getattr(self, HOST)

    def get_listening_port(self):
        return getattr(self, PORT)

    def get_validate_ssl(self):
        return getattr(self, VALIDATE_SSL)

    def get_cert_pem(self):
        return getattr(self, CERT_PEM)

    def get_key_pem(self):
        return getattr(self, KEY_PEM)

    def get_use_uwsgi(self):
        return getattr(self, USE_UWSGI)

    def get_host(self):
        return getattr(self, HOST)

    def get_port(self):
        return getattr(self, PORT)

    def get_use_ssl(self):
        return getattr(self, USE_SSL)

