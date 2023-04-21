class Repo:
    def __init__(self, entity_class):
        self._entity_class = entity_class


    @property
    def entity_class(self):
        return self._entity_class

