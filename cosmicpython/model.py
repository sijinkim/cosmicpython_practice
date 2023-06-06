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
        self.allocated_lines: list[str] = []

    def allocate(self, line: OrderLine) -> None:
        if self.can_allocate(line):
            self.available_quantity -= line.qty
            self.allocated_lines.append(line.orderid)

    def can_allocate(self, line: OrderLine) -> bool:
        return (
            self.sku == line.sku
            and self.available_quantity >= line.qty
            and line.orderid not in self.allocated_lines
        )

    def deallocate(self, line: OrderLine) -> None:
        if line.orderid in self.allocated_lines:
            self.available_quantity += line.qty
            self.allocated_lines.remove(line.orderid)
