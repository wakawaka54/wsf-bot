import yaml
import json
import os

from config.types import Config

CONFIG_PATH = 'config.yml'
CONFIG_ENV = 'WSF_BOT_CONFIG'


def read_config() -> Config:
    if os.getenv(CONFIG_ENV) is not None:
        print('Reading configuration from environment: ' + CONFIG_ENV)
        return Config(**json.loads(os.getenv(CONFIG_ENV)))

    if os.path.exists(CONFIG_PATH):
        print('Reading configuration from file: ' + CONFIG_PATH)
        with open(CONFIG_PATH, 'r') as file:
            return Config(**yaml.safe_load(file))

    raise TypeError(f'Could not find config in file {CONFIG_PATH} or environment {CONFIG_ENV}')
