from domain.entity import Entity
from domain.value_object import attribute, primary_key_attribute


class EntityInProgress(Entity):

    """
    Represents an Entity which doesn't have all information yet.
    """

    _pending = []

    def __init__(self):
        """Creates a new EntityInProgress instance"""
        super().__init__()
        self.__class__.register(self)

    @classmethod
    def register(cls, entityInProgress):
        if entityInProgress not in cls._pending:
            cls._pending[cls.build_key_from_entity(entityInProgress), entityInProgress]

    @classmethod
    def matching(cls, **kwargs):
        return FlakeInProgress._pending.get(cls.build_key_from_attributes(kwargs), None)

    @classmethod
    def build_key_from_attributes(cls, **kwargs) -> str:
        """Builds a key"""
        for key in self.__class__.primary_key():
            items.append(f'"{key}": "{kwargs.items().get(key, "")}"')
        return f'{{ {", ".join(items)} }}'

    @classmethod
    def build_key_from_entity(cls, entityInProgress) -> str:
        """Builds a key"""
        for key in self.__class__.primary_key():
            items.append(f'"{key}": "{getattr(entityInProgress, key, "")}"')
        return f'{{ {", ".join(items)} }}'
