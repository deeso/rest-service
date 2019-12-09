from .consts import *
import urllib.parse


class DBSettings(object):

    @classmethod
    def get_mongoclient_kargs(cls, **kargs):
        config = {}
        for k, nk in MAP_MONGO_TO_APP.items():
            v = kargs.get(k, '')
            config[nk] = v
        return config

    @classmethod
    def get_mongo_config(cls, **kargs):
        settings = {}
        for k, nk in MAP_MONGO_TO_SETTINGS.items():
            v = kargs.get(k, '')
            if v is None:
                v = ''
            settings[nk] = v
        return settings

    @classmethod
    def get_postgres_config(cls, **kargs):
        config = {}
        for k, nk in MAP_POSTGRES_TO_APP.items():
            v = kargs.get(k, '')
            if v is None:
                v = ''
            config[nk] = v

        if config.get(PASSWORD, None) is not None:
            config[PASSWORD] = urllib.parse.quote_plus(config[PASSWORD])
        config[DIALECT_DRIVER] = POSTGRES_DIALECT
        uri = DB_URI_FMT.format(**config)
        return {SQLALCHEMY_DATABASE_URI: uri}
