# Лабораторная работа №3: Крупный ООП-проект (Домен: Система управления складом)

## Спецификация классов

| Класс | Поля | Методы | Ассоциации (связанные классы) |
| :--- | :--- | :--- | :--- |
| AccessBadge | 3 | 2 | — |
| Address | 5 | 3 | — |
| AnalyticsReport | 4 | 2 | Warehouse, OperationDispatcher, WarehouseBudget |
| Barcode | 3 | 2 | — |
| BarcodeScanner | 5 | 2 | WarehouseEquipment, Barcode |
| Carrier | 5 | 2 | — |
| Client | 5 | 2 | Address |
| ConveyorBelt | 7 | 3 | WarehouseEquipment |
| Employee | 6 | 3 | AccessBadge |
| EquipmentFleet | 2 | 3 | WarehouseEquipment |
| Forklift | 6 | 2 | WarehouseEquipment, Pallet |
| ForkliftOperator | 9 | 2 | Employee, AccessBadge |
| FragileProduct | 9 | 2 | Product, ProductCategory, Barcode |
| HazardousProduct | 9 | 2 | Product, ProductCategory, Barcode |
| InboundOrder | 4 | 5 | OrderItem |
| InventoryAudit | 5 | 2 | StorageBin |
| InventoryBatch | 5 | 3 | Product |
| Invoice | 5 | 3 | Client, OutboundOrder |
| LoadingDock | 4 | 3 | — |
| MaintenanceRecord | 5 | 2 | — |
| OperationDispatcher | 3 | 4 | InboundOrder, OutboundOrder |
| OrderItem | 2 | 2 | Product |
| OutboundOrder | 5 | 5 | OrderItem |
| PackingStation | 4 | 2 | Pallet |
| Pallet | 4 | 3 | InventoryBatch |
| PerishableProduct | 8 | 2 | Product, ProductCategory, Barcode |
| PickingTask | 5 | 2 | OutboundOrder, StorageBin, Storekeeper |
| Product | 7 | 3 | ProductCategory, Barcode |
| ProductCategory | 4 | 2 | StorageCondition |
| QualityCheck | 5 | 1 | InventoryBatch, QualityInspector |
| QualityInspector | 8 | 1 | Employee, AccessBadge, InventoryBatch |
| Rack | 4 | 3 | Shelf, StorageBin |
| ReturnRequest | 6 | 2 | OutboundOrder |
| SecurityCheckpoint | 4 | 2 | — |
| Shelf | 4 | 3 | StorageBin |
| Shift | 4 | 2 | — |
| Shipment | 5 | 3 | OutboundOrder, Carrier, Pallet |
| StaffScheduler | 2 | 2 | Shift, Employee |
| StockRecord | 4 | 3 | Product, StorageBin |
| StockTransfer | 6 | 1 | StorageBin |
| StorageBin | 6 | 3 | — |
| StorageCondition | 4 | 2 | — |
| StorageZone | 5 | 3 | StorageCondition, Rack |
| Storekeeper | 8 | 2 | Employee, AccessBadge, StorageBin |
| Supplier | 5 | 2 | — |
| TemperatureSensor | 6 | 2 | WarehouseEquipment, StorageZone |
| Warehouse | 6 | 4 | Address, StorageZone, LoadingDock, SecurityCheckpoint |
| WarehouseBudget | 4 | 2 | — |
| WarehouseEquipment | 5 | 4 | MaintenanceRecord |
| WarehouseManager | 8 | 3 | Employee, AccessBadge |
| WarehouseSystem | 9 | 5 | Warehouse, EquipmentFleet, StaffScheduler, OperationDispatcher, WarehouseBudget, Product, InventoryBatch, Supplier, Client |
| WeighingScale | 6 | 2 | WarehouseEquipment, Pallet |

## Исключения (14)
- `WarehouseException`
- `InvalidDataError`
- `InsufficientStockError`
- `BinCapacityExceededError`
- `TemperatureViolationError`
- `ExpiredProductError`
- `EquipmentUnavailableError`
- `EquipmentOverloadError`
- `UnauthorizedAccessError`
- `OrderNotFoundError`
- `InvalidOrderStateError`
- `DockOccupiedError`
- `QualityCheckFailedError`
- `BudgetExceededError`

## Итоговая статистика
- **Поля:** 272
- **Поведения (методы):** 130
- **Ассоциации:** 76
- **Исключения:** 14
- **Покрытие тестами:** 98%