import os
import importlib.resources


_APP_SETTINGS = {
    'name': __package__,
    'log_config_dir': ['config'],
    'log_config': 'logging.yaml',
}


class AppSettings():
    s = _APP_SETTINGS

    def __init__(self):
        self._user_config_dir = None

    @property
    def name(self):
        return self.s.get('name')

    @property
    def log_config(self):
        try:
            module_path = '.'.join([self.s.get('name')] + self.s.get('log_config_dir'))
            with importlib.resources.path(module_path, self.s.get('log_config')) as f:
                return f

        except FileNotFoundError:
            return None

    @property
    def user_config_dir(self):
        if not self._user_config_dir:
            self._user_config_dir = os.path.join(os.path.expanduser('~'), '.{}'.format(self.s.get('name')))

        return self._user_config_dir


APP_SETTINGS = AppSettings()
