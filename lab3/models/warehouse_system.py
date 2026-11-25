"""Top-level facade coordinating all warehouse management subsystems."""

from typing import Dict

from exceptions import InvalidDataError
from .client import Client
from .equipment_fleet import EquipmentFleet
from .inventory_batch import InventoryBatch
from .operation_dispatcher import OperationDispatcher
from .product import Product
from .staff_scheduler import StaffScheduler
from .supplier import Supplier
from .warehouse import Warehouse
from .warehouse_budget import WarehouseBudget


class WarehouseSystem:
    """Central entry point uniting infrastructure, inventory, staff, and finance."""

    def __init__(
        self,
        warehouse: Warehouse,
        fleet: EquipmentFleet,
        scheduler: StaffScheduler,
        dispatcher: OperationDispatcher,
        budget: WarehouseBudget,
    ) -> None:
        self.warehouse = warehouse
        self.fleet = fleet
        self.scheduler = scheduler
        self.dispatcher = dispatcher
        self.budget = budget
        self.products: Dict[str, Product] = {}
        self.batches: Dict[str, InventoryBatch] = {}
        self.suppliers: Dict[str, Supplier] = {}
        self.clients: Dict[str, Client] = {}

    def register_product(self, product: Product) -> None:
        """Add a product to the system catalog."""
        if product.sku in self.products:
            raise InvalidDataError(f"Product SKU {product.sku} is already registered.")
        self.products[product.sku] = product

    def register_batch(self, batch: InventoryBatch) -> None:
        """Register an incoming inventory batch in the system."""
        self.batches[batch.batch_id] = batch

    def register_supplier(self, supplier: Supplier) -> None:
        """Register a supplier in the partner directory."""
        self.suppliers[supplier.supplier_id] = supplier

    def register_client(self, client: Client) -> None:
        """Register a client in the partner directory."""
        self.clients[client.client_id] = client

    def calculate_total_inventory_value(self) -> float:
        """Compute total monetary value of all non-quarantined batches."""
        total = 0.0
        for batch in self.batches.values():
            if not batch.is_quarantined:
                total += batch.product.calculate_total_value(batch.quantity)
        return round(total, 2)