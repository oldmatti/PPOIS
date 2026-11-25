"""Domain models package for the warehouse management system (52 classes)."""

from .access_badge import AccessBadge
from .address import Address
from .analytics_report import AnalyticsReport
from .barcode import Barcode
from .barcode_scanner import BarcodeScanner
from .carrier import Carrier
from .client import Client
from .conveyor_belt import ConveyorBelt
from .employee import Employee
from .equipment_fleet import EquipmentFleet
from .forklift import Forklift
from .forklift_operator import ForkliftOperator
from .fragile_product import FragileProduct
from .hazardous_product import HazardousProduct
from .inbound_order import InboundOrder
from .inventory_audit import InventoryAudit
from .inventory_batch import InventoryBatch
from .invoice import Invoice
from .loading_dock import LoadingDock
from .maintenance_record import MaintenanceRecord
from .operation_dispatcher import OperationDispatcher
from .order_item import OrderItem
from .outbound_order import OutboundOrder
from .packing_station import PackingStation
from .pallet import Pallet
from .perishable_product import PerishableProduct
from .picking_task import PickingTask
from .product import Product
from .product_category import ProductCategory
from .quality_check import QualityCheck
from .quality_inspector import QualityInspector
from .rack import Rack
from .return_request import ReturnRequest
from .security_checkpoint import SecurityCheckpoint
from .shelf import Shelf
from .shift import Shift
from .shipment import Shipment
from .staff_scheduler import StaffScheduler
from .stock_record import StockRecord
from .stock_transfer import StockTransfer
from .storage_bin import StorageBin
from .storage_condition import StorageCondition
from .storage_zone import StorageZone
from .storekeeper import Storekeeper
from .supplier import Supplier
from .temperature_sensor import TemperatureSensor
from .warehouse import Warehouse
from .warehouse_budget import WarehouseBudget
from .warehouse_equipment import WarehouseEquipment
from .warehouse_manager import WarehouseManager
from .warehouse_system import WarehouseSystem
from .weighing_scale import WeighingScale

__all__ = [
    "AccessBadge",
    "Address",
    "AnalyticsReport",
    "Barcode",
    "BarcodeScanner",
    "Carrier",
    "Client",
    "ConveyorBelt",
    "Employee",
    "EquipmentFleet",
    "Forklift",
    "ForkliftOperator",
    "FragileProduct",
    "HazardousProduct",
    "InboundOrder",
    "InventoryAudit",
    "InventoryBatch",
    "Invoice",
    "LoadingDock",
    "MaintenanceRecord",
    "OperationDispatcher",
    "OrderItem",
    "OutboundOrder",
    "PackingStation",
    "Pallet",
    "PerishableProduct",
    "PickingTask",
    "Product",
    "ProductCategory",
    "QualityCheck",
    "QualityInspector",
    "Rack",
    "ReturnRequest",
    "SecurityCheckpoint",
    "Shelf",
    "Shift",
    "Shipment",
    "StaffScheduler",
    "StockRecord",
    "StockTransfer",
    "StorageBin",
    "StorageCondition",
    "StorageZone",
    "Storekeeper",
    "Supplier",
    "TemperatureSensor",
    "Warehouse",
    "WarehouseBudget",
    "WarehouseEquipment",
    "WarehouseManager",
    "WarehouseSystem",
    "WeighingScale",
]