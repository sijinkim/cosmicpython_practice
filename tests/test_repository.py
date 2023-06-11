import pytest
from sqlalchemy.orm import Session

from cosmicpython.model import Batch, OrderLine
from cosmicpython.repository import SqlAlchemyRepository


@pytest.fixture
def session():
    pass


def test_repository_can_save_a_batch(session):
    batch = Batch("batch1", "RUSTY-SOAPDISH", 100, eta=None)

    repo = SqlAlchemyRepository(session)
    repo.add(batch)
    session.commit()

    rows = list(
        session.execute(
            'SELECT reference, sku, _purchased_quantiry, eta FROM "batches"'
        )
    )
    assert rows == [("batch1", "RUSTRY-SOAPDISH", 100, None)]


def insert_order_line(session):
    session.execute(
        'INSERT INTO order_lines (orderid, sku, qty)'
        ' VALUES ("order1", "GENERIC-SOFA", 12)'
    )
    [[orderline_id]] = session.execute(
        'SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku',
        dict(orderid="order1", sku="GENERIC-SOFA")
    )
    return orderline_id

def insert_batch(session, batch_id):
    # 배치 생성
    pass

def insert_allocation(session, orderline_id, batch_id):
    # 배치에 할당된 orderline 생성
    pass

def test_repository_can_retrieve_a_batch_with_allocations(session):
    orderline_id = insert_order_line(session)
    batch1_id = insert_batch(session, "batch1")
    insert_batch(session, "batch2")
    insert_allocation(session, orderline_id, batch1_id)

    repo = SqlAlchemyRepository(session)
    retrieved = repo.get("batch1")

    expected = Batch("batch1", "GENERIC-SOFA", 100, eta=None)
    assert retrieved == expected
    assert retrieved.sku == expected.sku
    assert retrieved._purchased_quantity == expected._purchased_quantity
    assert retrieved._allocations == {
        OrderLine("order1", "GENERIC-SOFA", 12),
    }