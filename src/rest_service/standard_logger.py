import logging
import sys
import traceback
import inspect

LOGGER = None

LOCATION_FMT = "{filename}.{name}:{number}"
class Logger(object):
    FMT = '[%(asctime)s - %(name)s] %(message)s'
    DEFAULT_LEVEL = logging.DEBUG
    AUTHN_FMT = "{username} (from group:{group}) authenticated {source}: {success}"
    AUTHZ_FMT = "{principal} (using role {role}) performed {action} on {object}: {success}"
    ACTION_FMT = "{principal} performed {action} (details: {details})"
    EXC_FMT = "exception {exc} (details: {details})"

    def __init__(self, name, level=DEFAULT_LEVEL, fmt=FMT):
        self.name = name
        self.logger = logging.getLogger(name)
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        self.logger.setLevel(level)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(level)
        formatter = logging.Formatter(fmt)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def get_location(self, n=3):
        fr = inspect.currentframe()
        fn = fr.f_back
        while n > 0:
            try:
                fn = fn.f_back
            except:
                break
            n += -1
        return fn

    def _location_string(self, n=2):
        return self.get_location_string(self.get_location(n))

    def get_location_string(self, frame):
        kargs = {'name':frame.f_code.co_name, 'filename':frame.f_code.co_name, 'number':frame.f_lineno}
        return LOCATION_FMT.format(**kargs)

    def info(self, msg):
        self.logger.info(self._location_string() + " " +msg)

    def debug(self, msg):
        self.logger.debug(self._location_string() + " " +msg)

    def error(self, msg):
        self.logger.error(self._location_string() + " " +msg)

    def critical(self, msg):

        self.logger.critical(self._location_string() + " " + msg)

    def authenticate_user(self, username, success=False, source='', group=None):
        msg = self.AUTHN_FMT.format(**{
            'username': username,
            # 'location': location,
            'success': success,
            'source': source,
            'group': group,})
        return self.info(msg)


    def authenticate_token(self, token_name, success=False, source='', group=None):
        msg = self.AUTHN_FMT.format(**{
            'username':token_name,
            # 'location':location,
            'success':success,
            'source':source,
            'group':group,
        })
        return self.info(msg)

    def authorize_user(self, principal, action, object_, success=False, role=None):
        msg = self.AUTHZ_FMT.format(**{
            'principal':principal,
            'action':action,
            'success':success,
            'object':object_,
            # 'location':location,
            'role':role,
        })
        return self.info(msg)

    def action(self, principal, action, details=None):
        msg = self.ACTION_FMT.format(**{
            'principal':principal,
            'action':action,
            'details':details,
            # 'location':location,
        })
        return self.info(msg)

    def exception(self, details):
        msg = self.EXC_FMT.format(**{
            # 'location':location,
            'details':details,
            'exc':traceback.format_exc()})
        return self.error(msg)

