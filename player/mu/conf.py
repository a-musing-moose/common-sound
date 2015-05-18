import os
import json


class Settings(object):

    def __init__(self):
        source = os.environ.get("MU_SETTINGS", None)
        if source is None:
            raise Exception("MU_SETTINGS has not been defined")
        try:
            self.json = json.loads(source)
        except ValueError:
            with open(source, 'r') as f:
                self.json = json.load(f)

    def __getattr__(self, key):
        try:
            value = self.json[key]
        except KeyError:
            raise AttributeError(key)
        if isinstance(value, dict) and 'env' in value:
            default = value.get('default', None)
            value = self._from_environment(
                value['env'],
                default
            )
        setattr(self, key, value)
        return value

    def _from_environment(self, key, default=None):
        try:
            return os.environ[key]
        except KeyError:
            return default


settings = Settings()
