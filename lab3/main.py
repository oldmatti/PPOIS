"""Interactive CLI for the Warehouse Management System."""

import sys
from pathlib import Path
from typing import Callable, Dict

# Ensure imports work when running from repository root or inside lab3
sys.path.insert(0, str(Path(__file__).resolve().parent))

from exceptions import WarehouseException
from models import (
    Address,
    AnalyticsReport,
    Barcode,
    EquipmentFleet,
    Forklift,
    InventoryBatch,
    LoadingDock,
    OperationDispatcher,
    OrderItem,
    OutboundOrder,
    Product,
    ProductCategory,
    Rack,
    Shelf,
    StaffScheduler,
    StorageBin,
    StorageCondition,
    StorageZone,
    Warehouse,
    WarehouseBudget,
    WarehouseSystem,
)

DEFAULT_FISCAL_YEAR = 2026
DEFAULT_INITIAL_BUDGET = 100000.0
DEFAULT_SHELF_CAPACITY = 4
DEFAULT_RACK_CAPACITY = 3


def build_demo_system() -> WarehouseSystem:
    """Initialize a pre-populated warehouse system for interactive use."""
    address = Address("Belarus", "Minsk", "Nezavisimosti Ave", "58", "220013")
    warehouse = Warehouse("WH-01", "Central Logistics Hub", address)
    zone = StorageZone("Z-A", "General Dry Storage", StorageCondition())
    rack = Rack("R-01", "Aisle-1", DEFAULT_RACK_CAPACITY)
    shelf = Shelf("S-01", 1, DEFAULT_SHELF_CAPACITY)
    shelf.add_bin(StorageBin("BIN-A1"))
    rack.add_shelf(shelf)
    zone.add_rack(rack)
    warehouse.add_zone(zone)
    warehouse.add_dock(LoadingDock("D-01", "universal"))

    fleet = EquipmentFleet("WH-01")
    fleet.register_equipment(Forklift("FL-01", "Toyota 8FBE"))
    scheduler = StaffScheduler("WH-01")
    dispatcher = OperationDispatcher("DISP-01")
    budget = WarehouseBudget(DEFAULT_FISCAL_YEAR, DEFAULT_INITIAL_BUDGET)
    return WarehouseSystem(warehouse, fleet, scheduler, dispatcher, budget)


class WarehouseCLI:
    """Console menu controller separated from domain models."""

    def __init__(self, system: WarehouseSystem) -> None:
        self.system = system
        self.default_category = ProductCategory("CAT-GEN", "General Goods", StorageCondition())
        self.is_running = True
        self.actions: Dict[str, Callable[[], None]] = {
            "1": self.show_analytics_report,
            "2": self.add_product,
            "3": self.receive_batch,
            "4": self.create_outbound_order,
            "5": self.ship_outbound_order,
            "6": self.allocate_budget_expense,
            "0": self.exit_cli,
        }

    def print_menu(self) -> None:
        """Display available console operations."""
        print("\n=== Warehouse Management System ===")
        print("1. Show analytics report & inventory value")
        print("2. Register new product")
        print("3. Receive inventory batch into BIN-A1")
        print("4. Create outbound order")
        print("5. Ship outbound order")
        print("6. Record operational budget expense")
        print("0. Exit")

    def show_analytics_report(self) -> None:
        """Print warehouse KPIs and total inventory value."""
        report = AnalyticsReport(
            "REP-LIVE",
            self.system.warehouse,
            self.system.dispatcher,
            self.system.budget,
        )
        print("\n" + report.generate_summary())
        print(f"Budget utilization: {report.calculate_budget_utilization_percent()}%")
        print(f"Total inventory value: {self.system.calculate_total_inventory_value()}")

    def add_product(self) -> None:
        """Prompt for product details and register it in the catalog."""
        sku = input("SKU: ").strip()
        name = input("Product name: ").strip()
        barcode_val = input("Barcode (digits, e.g. 4810001234567): ").strip()
        weight = float(input("Unit weight (kg): "))
        volume = float(input("Unit volume (m3): "))
        price = float(input("Unit price: "))
        barcode = Barcode(barcode_val, "EAN13")
        product = Product(sku, name, self.default_category, barcode, weight, volume, price)
        self.system.register_product(product)
        print(f"Registered product {sku} ({name}).")

    def receive_batch(self) -> None:
        """Receive a batch of an existing product and place it into BIN-A1."""
        batch_id = input("Batch ID: ").strip()
        sku = input("Product SKU: ").strip()
        quantity = int(input("Quantity: "))
        if sku not in self.system.products:
            print(f"Product {sku} not found. Register it first.")
            return
        product = self.system.products[sku]
        target_bin = self.system.warehouse.zones[0].racks[0].shelves[0].bins[0]
        target_bin.add_item(
            sku,
            quantity,
            product.calculate_total_weight(quantity),
            product.volume_m3 * quantity,
        )
        self.system.register_batch(InventoryBatch(batch_id, product, quantity))
        print(f"Batch {batch_id} placed in {target_bin.bin_code}.")

    def create_outbound_order(self) -> None:
        """Create a new outbound order with a single product line."""
        order_id = input("Order ID: ").strip()
        client_id = input("Client ID: ").strip()
        sku = input("Product SKU: ").strip()
        quantity = int(input("Quantity: "))
        if sku not in self.system.products:
            print(f"Product {sku} not found.")
            return
        order = OutboundOrder(order_id, client_id)
        order.add_item(OrderItem(self.system.products[sku], quantity))
        order.start_fulfillment()
        self.system.dispatcher.register_outbound_order(order)
        print(f"Outbound order {order_id} created and moved to fulfillment.")

    def ship_outbound_order(self) -> None:
        """Mark an existing outbound order as shipped."""
        order_id = input("Order ID to ship: ").strip()
        order = self.system.dispatcher.get_outbound_order(order_id)
        order.mark_shipped()
        print(f"Order {order_id} marked as shipped.")

    def allocate_budget_expense(self) -> None:
        """Deduct an operational expense from the warehouse budget."""
        description = input("Expense description: ").strip()
        amount = float(input("Amount: "))
        remaining = self.system.budget.allocate_expense(description, amount)
        print(f"Expense recorded. Remaining budget: {remaining}")

    def exit_cli(self) -> None:
        """Stop the interactive menu loop."""
        self.is_running = False
        print("Exiting Warehouse Management System.")

    def run(self) -> None:
        """Run the main interactive command loop."""
        while self.is_running:
            self.print_menu()
            choice = input("Select option: ").strip()
            action = self.actions.get(choice)
            if action is None:
                print("Invalid option. Please try again.")
                continue
            try:
                action()
            except (WarehouseException, ValueError) as error:
                print(f"Error: {error}")


def main() -> None:
    """Entry point for running the warehouse CLI."""
    system = build_demo_system()
    cli = WarehouseCLI(system)
    cli.run()


if __name__ == "__main__":
    main()