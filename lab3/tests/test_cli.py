"""Unit tests for the interactive WarehouseCLI controller."""

from main import WarehouseCLI, build_demo_system


def test_cli_full_workflow(monkeypatch, capsys) -> None:
    """Simulate a user session covering all CLI menu options."""
    inputs = iter(
        [
            "1",
            "2",
            "SKU-10",
            "Laptop",
            "4810001234567",
            "2.0",
            "0.05",
            "1000.0",
            "3",
            "BAT-10",
            "SKU-10",
            "5",
            "4",
            "ORD-10",
            "CL-10",
            "SKU-10",
            "2",
            "5",
            "ORD-10",
            "6",
            "Packaging supplies",
            "500.0",
            "99",
            "0",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    cli = WarehouseCLI(build_demo_system())
    cli.run()

    output = capsys.readouterr().out
    assert "Central Logistics Hub" in output
    assert "Registered product SKU-10" in output
    assert "Batch BAT-10 placed in BIN-A1" in output
    assert "Order ORD-10 marked as shipped" in output
    assert "Expense recorded" in output
    assert "Invalid option" in output
    assert "Exiting Warehouse Management System" in output