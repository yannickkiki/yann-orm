from .manager import BaseManager


class MetaModel(type):
    manager_class = BaseManager

    @property
    def objects(cls):
        return cls.manager_class(model_class=cls)


class BaseModel(metaclass=MetaModel):

    def __init__(self, **row_data):
        for field_name, value in row_data.items():
            setattr(self, field_name, value)

    def __repr__(self):
        return str(self.__dict__)
