from environs import Env

from app.common.parser.yaml import load_yaml
from app.common.parser.config_parser import ConfigParser

_settings = ConfigParser()


class Config:
    # 基础配置
    PROJECT_DIR = ''
    APPENV_FILE = ''
    YAML_FILE = 'databases.yaml'
    env = Env()
    env.read_env(APPENV_FILE)
    DEPLOY_ENV = env('env')

    DATASOURCE = load_yaml(PROJECT_DIR, YAML_FILE)

    A = _settings.as_int('A', default='10')


class DevConfig(Config):
    DEBUG = True
    NAME = 'DevConfig'


class TestConfig(Config):
    DEBUG = True
    NAME = 'TestConfig'


class ProdConfig(Config):
    DEBUG = True
    NAME = 'ProdConfig'


configurations = dict(dev=DevConfig, test=TestConfig, prod=ProdConfig)

flask_config = configurations.get(Config.DEPLOY_ENV)

