class NoModificationMeta(type):
    
    def __setattr__(self, name, value):
        # don't allow changing the value of any attribute
        if hasattr(self, name):
            raise ValueError(f"Cannot reassign {name}")
        super().__setattr__(name, value)
    
    def __delattr__(self, name):
        # don't allow deleting any attribute
        raise ValueError(f"Cannot delete {name}")


class BaseEnum(metaclass=NoModificationMeta):
    """Inherit this class for creating enum in the system"""


class EmailStatus(BaseEnum):
    PENDING = 0
    SUCCESS = 1
    ERROR = 2
