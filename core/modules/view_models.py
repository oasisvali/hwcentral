from core.modules.constants import VIEWMODEL_KEY

# Abstract class that is used to provide asContext functionality to all view models
class BaseViewModel():
    def asContext(self):
        return {VIEWMODEL_KEY: self}
