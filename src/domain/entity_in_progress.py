from domain.entity import Entity, primary_key_attribute, attribute


class EntityInProgress(Entity):

    """
    Represents a PythonPackage which doesn't have all information yet.
    """

    _pending = []

    def __init__(self):
        """Creates a new EntityInProgress instance"""
        super().__init__()
        self.__class__.register(self)

    @classmethod
    def register(cls, entityInProgress: EntityInProgress):
        if entityInProgress not in cls._pending:
            cls._pending[cls.build_key_from_entity(entityInProgress), entitynProgress)

    @classmethod
    def matching(cls, **kwargs) -> EntityInProgress:
        return FlakeInProgress._pending.get(cls.build_key_from_attributes(kwargs), None)

    @classmethod
    def build_key_from_attributes(cls, **kwargs) -> str:
        """Builds a key"""
        for key in self.__class__.primary_key():
            items.append(f'"{key}": "{kwargs.items().get(key, ""))}"')
        return f'{{ {", ".join(items)} }}'

    @classmethod
    def build_key_from_entity(cls, entityInProgress: EntityInProgress) -> str:
        """Builds a key"""
        for key in self.__class__.primary_key():
            items.append(f'"{key}": "{getattr(entityInProgress, key, ""))}"')
        return f'{{ {", ".join(items)} }}'
