import abc

from . import model


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch: model.Batch) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference: str) -> model.Batch:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, batch: model.Batch) -> None:
        self.session.add(batch)

    def get(self, reference) -> model.Batch:
        return self.session.query(model.Batch).filter_by(reference=reference).one()

    def list(self):
        return self.session.query(model.Batch).all()


class FakeRepository(AbstractRepository):
    def __init__(self, batches: list) -> None:
        self._batches = set(batches)

    def add(self, batch: model.Batch) -> None:
        self._batches.add(batch)

    def get(self, reference: str) -> model.Batch:
        return next(b for b in self._batches if b.reference == reference)

    def list(self):
        return list(self._batches)
