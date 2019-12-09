from .config import Config
from .consts import *
from .standard_logger import Logger
from quart_openapi import Pint
from .db import DBSettings
import importlib
import traceback
from flask_sqlalchemy import SQLAlchemy
import threading
import asyncio
import signal
from multiprocessing import Process
from hypercorn.config import Config as HyperConfig
from hypercorn.asyncio import serve

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

        self.shutdown_event = None
        self.bg_thread = None

    def import_add_view(self, fq_python_class_view: str) -> bool:
        '''
        Import a module and load the class for a provided view
        :param view: Python module in dot'ted notation, e.g. `foo.views.ViewX`
        :return: bool
        '''
        self.logger.debug("Adding view ({}) to rest-service".format(fq_python_class_view))
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
            self.logger.exception(msg)
            return False

        try:
            python_class = getattr(mi, cn, None)
        except:
            msg = "{} is not a valid Python class in {}: \n{}".format(cn, mn, traceback.format_exc())
            self.logger.exception(msg)
            return False

        if python_class is not None:
            self.add_view(python_class)
            self.logger.debug("Finished adding view ({}) to rest-service".format(fq_python_class_view))
            return True

        self.logger.debug("Failed tp add view ({}) to rest-service".format(fq_python_class_view))
        return False

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
        self.logger.debug("Preparing to start rest-service")
        if self.get_use_ssl() and self.get_key_pem() is not None and \
                self.get_cert_pem() is not None:
            self.logger.debug("Preparing ssl_context with cert:{} and key:{}".format(self.get_cert_pem(),
                                                                                     self.get_key_pem()))
            ssl_context = (self.get_cert_pem(), self.get_key_pem())

        # if self.get_use_uwsgi():
        #     self.logger.info("Starting the application using WSGI {}:{} using ssl? {}".format(self.get_listening_host(),
        #                                                                            self.get_listening_port(),
        #                                                                            ssl_context is None))
        #
        #     kargs = {
        #         'port': self.get_listening_port(),
        #         'host': self.get_listening_host(),
        #         'debug': debug,
        #         'ssl_context': ssl_context,
        #         'shutdown_trigger': self.shutdown_event.wait
        #     }
        #     self.bg_thread = threading.Thread(target=self.app.run, kwargs=kargs)
        #     self.bg_thread.start()
        #     return self.bg_thread
        # self.logger.info("Starting the application {}:{} using ssl? {}".format(self.get_listening_host(),
        #                                                                        self.get_listening_port(),
        #                                                                        ssl_context is None))
        #
        # kargs = {
        #     'port': self.get_listening_port(),
        #     'host': self.get_listening_host(),
        #     'debug': debug,
        #     'ssl_context': ssl_context,
        #     'shutdown_trigger': self.shutdown_event.wait
        # }
        self.logger.info("Starting the application {}:{} using ssl? {}".format(self.get_listening_host(),
                                                                               self.get_listening_port(),
                                                                               ssl_context is None))
        # kargs = {
        #     'port': self.get_listening_port(),
        #     'host': self.get_listening_host(),
        #     'debug': debug,
        #     'ssl_context': ssl_context,
        #     'shutdown_trigger': self.shutdown_event.wait
        # }
        self.bg_thread = Process(target=self.start_app, args=(debug,))
        self.bg_thread.start()
        # self.app.run(**kargs)
        return True

    def start_app(self, debug):
        ssl_context = None
        self.logger.debug("Preparing to start rest-service")
        if self.get_use_ssl() and self.get_key_pem() is not None and \
                self.get_cert_pem() is not None:
            self.logger.debug("Preparing ssl_context with cert:{} and key:{}".format(self.get_cert_pem(),
                                                                                     self.get_key_pem()))
            ssl_context = (self.get_cert_pem(), self.get_key_pem())
        self.logger.info("Starting the application {}:{} using ssl? {}".format(self.get_listening_host(),
                                                                               self.get_listening_port(),
                                                                               ssl_context is None))


        kargs = {
            'port': self.get_listening_port(),
            'host': self.get_listening_host(),
            'debug': debug,
            'ssl_context': ssl_context,
            # 'shutdown_trigger': self.shutdown_event.wait
        }

        self.app.debug = debug
        loop = asyncio.get_event_loop()
        config = HyperConfig()
        config.debug = debug
        config.access_log_format = "%(h)s %(r)s %(s)s %(b)s %(D)s"
        config.accesslog = self.logger.logger
        config.bind = ["{host}:{port}".format(**{'host':self.get_listening_host(),
                                                 'port':self.get_listening_port()})]
        config.certfile = self.get_cert_pem() if self.get_use_ssl() else None
        config.keyfile = self.get_key_pem() if self.get_use_ssl() else None

        config.errorlog = config.accesslog
        config.use_reloader = True

        scheme = "https" if config.ssl_enabled else "http"
        self.logger.info("Running on {}://{} (CTRL + C to quit)".format(scheme, config.bind[0]))

        loop = asyncio.get_event_loop()
        self.shutdown_event = asyncio.Event()

        if loop is not None:
            loop.set_debug(debug or False)
            loop.run_until_complete(serve(self.app, config, shutdown_trigger=self.shutdown_event.wait))
        else:
            asyncio.run(serve(self.app, config, shutdown_trigger=self.shutdown_event.wait), debug=config.debug)

        loop.run_until_complete(
            serve(self.app, config, shutdown_trigger=self.shutdown_event.wait)
        )

    def stop(self):
        if self.bg_thread is not None:
            self.bg_thread.terminate()
            self.bg_thread.join()

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
        view.bind_application(self.app)

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

