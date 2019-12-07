USER_TOKENS = 'user_tokens'
ADMIN_TOKENS = 'admin_tokens'
TOKEN_VALUE = 'token_value'
USERNAME = 'username'
NAME = 'name'
EMAIL = 'email'
TOKENS = 'tokens'
UNKNOWN = 'unknown'
HOST = 'host'
PORT = 'port'
USE_SSL = 'use_ssl'
USE_WSGI = 'use_wsgi'
VALIDATE_SSL = 'validate_ssl'
USE_UWSGI = 'use_uwsgi'
CERT_PEM = 'cert_pem'
KEY_PEM = 'key_pem'

USER = 'user'
PASSWORD = 'password'
DB = 'db'
USING_POSTGRES = 'using_postgres'
POSTGRES_HOST = 'postgres_host'
POSTGRES_PORT = 'postgres_port'
POSTGRES_USER = 'postgres_user'
POSTGRES_PASS = 'postgres_password'
POSTGRES_USE_SSL = 'postgres_use_ssl'
POSTGRES_DB = 'postgres_db'

USING_MONGO = 'using_mongo'
MONGO_HOST = 'mongo_host'
MONGO_PORT = 'mongo_port'
MONGO_USER = 'mongo_user'
MONGO_PASS = 'mongo_password'
MONGO_USE_SSL = 'mongo_use_ssl'
MONGO_DB = 'mongo_db'

VIEWS = 'views'


REST_SERVICE_BLOCK = 'rest-service-block'

REST_SERVICE_CONFIGS = {
    USE_SSL: False,
    USE_UWSGI: False,
    HOST: '127.0.0.1',
    PORT: 8000,
    VALIDATE_SSL: False,
    CERT_PEM: None,
    KEY_PEM: None,

    # Mongo related
    USING_MONGO: False,
    MONGO_HOST: None,
    MONGO_PORT: None,
    MONGO_USER: None,
    MONGO_PASS: None,
    MONGO_USE_SSL: False,
    MONGO_DB: None,

    # Postgres related
    USING_POSTGRES: False,
    POSTGRES_HOST: None,
    POSTGRES_PORT: None,
    POSTGRES_USER: None,
    POSTGRES_PASS: None,
    POSTGRES_USE_SSL: False,
    POSTGRES_DB: None,

}

MONGODB_SETTINGS = 'MONGODB_SETTINGS'
MAP_MONGO_TO_APP = {
    MONGO_HOST: HOST,
    MONGO_PORT: PORT,
    MONGO_USER: USER,
    MONGO_PASS: PASSWORD,
    MONGO_DB: DB,
}

POSTGRESDB_SETTINGS = 'POSTGRESDB_SETTINGS'
MAP_POSTGRES_TO_APP = {
    POSTGRES_HOST: HOST,
    POSTGRES_PORT: PORT,
    POSTGRES_USER: USER,
    POSTGRES_PASS: PASSWORD,
    POSTGRES_DB: DB,
}

DIALECT_DRIVER = 'dialect_driver'
POSTGRES_DIALECT = 'postgresql+psycopg2'
MONGODB_DIALECT = 'mongodb'
SQLALCHEMY_DATABASE_URI ='SQLALCHEMY_DATABASE_URI'

DB_URI_FMT = '{dialect_driver}://{username}:{password}@{host}:{port}/{database}'

