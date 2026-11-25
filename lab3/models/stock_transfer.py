"""Internal stock transfer model between two storage bins."""

from constants import STATUS_COMPLETED, STATUS_CREATED
from exceptions import InvalidDataError, InvalidOrderStateError
from .storage_bin import StorageBin


class StockTransfer:
    """Moves a quantity of a product from a source bin to a destination bin."""

    def __init__(
        self,
        transfer_id: str,
        source_bin: StorageBin,
        destination_bin: StorageBin,
        sku: str,
        quantity: int,
    ) -> None:
        if not transfer_id or not sku or quantity <= 0:
            raise InvalidDataError("Transfer requires ID, SKU, and positive quantity.")
        if source_bin.bin_code == destination_bin.bin_code:
            raise InvalidDataError("Source and destination bins must be different.")
        self.transfer_id = transfer_id
        self.source_bin = source_bin
        self.destination_bin = destination_bin
        self.sku = sku
        self.quantity = quantity
        self.status = STATUS_CREATED

    def execute(self, unit_weight_kg: float, unit_volume_m3: float) -> None:
        """Perform the physical transfer between bins."""
        if self.status != STATUS_CREATED:
            raise InvalidOrderStateError("Transfer has already been executed.")
        total_weight = unit_weight_kg * self.quantity
        total_volume = unit_volume_m3 * self.quantity
        self.destination_bin.add_item(self.sku, self.quantity, total_weight, total_volume)
        self.source_bin.remove_item(self.sku, self.quantity, total_weight, total_volume)
        self.status = STATUS_COMPLETED