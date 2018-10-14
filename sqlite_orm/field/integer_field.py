from .base_field import BaseField


class IntegerField(BaseField):
    __type_name__ = 'INTEGER'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
