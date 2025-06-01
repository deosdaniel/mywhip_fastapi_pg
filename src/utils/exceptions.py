class VinBusyException(Exception):
    pass


class EntityNotFoundException(Exception):
    def __init__(self, entity: str):
        self.entity = entity
