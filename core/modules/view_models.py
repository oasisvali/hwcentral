from core.modules.constants import VIEWMODEL_KEY

class BaseViewModel():
    def asContext(self):
        return {VIEWMODEL_KEY: self}
