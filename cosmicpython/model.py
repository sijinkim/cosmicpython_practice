from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: date | None) -> None:
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self.available_quantity = qty

    def allocate(self, line: OrderLine) -> None:
        if self.sku == line.sku:
            self.available_quantity -= line.qty
