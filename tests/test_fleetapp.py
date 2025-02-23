import pytest
import tkinter as tk
from gui.tkfiltermanager import TkFilterManager
from gui.fleetapp import FleetApp
from gui.utils.appmessage import AppMessage
from typing import List, Tuple, Generator


class TestFleetApp:
    """Test suite for the FleetApp class."""

    @pytest.fixture(autouse=True)
    def setup(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> Generator[None, None, None]:
        """Fixture to set up the Tkinter root and FleetApp instance.

        Args:
            monkeypatch: Pytest fixture to mock methods.
        """
        self.root = tk.Tk()
        self.root.withdraw()  # Prevent GUI from showing
        self.app = FleetApp(self.root)

        # Mock VehicleManager methods
        monkeypatch.setattr(
            self.app.manager, "search_vehicles", lambda *args: []
        )
        monkeypatch.setattr(
            self.app.manager, "remove_vehicle", lambda reg: None
        )
        monkeypatch.setattr(
            self.app.manager, "add_vehicle",
            lambda vehicle: None
        )
        monkeypatch.setattr(
            self.app.manager, "update_vehicle", lambda reg, **kwargs: None
        )

        # Mock AppMessage to prevent blocking popups
        self.captured_messages: List[Tuple[str, str, str]] = []

        def mock_show(level: str, title: str, message: str = "") -> None:
            self.captured_messages.append((level, title, message))

        monkeypatch.setattr(AppMessage, "show", mock_show)

        yield
        self.root.destroy()

    def test_initialization(self) -> None:
        """Test that FleetApp initializes correctly."""
        assert isinstance(self.app, FleetApp)
        assert self.app.root.title() == "Fleet Management System"

    def test_open_add_vehicle_popup(self) -> None:
        """Ensure add vehicle popup opens without error."""
        self.app.open_add_vehicle_popup()
        assert len(self.captured_messages) == 0  # No errors should occur

    def test_edit_vehicle_popup_no_selection(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Ensure edit popup does nothing if no vehicle is selected.

        Args:
            monkeypatch: Pytest fixture to mock methods.
        """
        monkeypatch.setattr(self.app.tree, "identify_row", lambda y: "")

        class MockEvent:
            def __init__(self) -> None:
                self.y = 0

        self.app.edit_vehicle_popup(event=MockEvent())
        assert len(self.captured_messages) == 0  # No error should occur

    def test_edit_vehicle_popup_vehicle_not_found(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Ensure edit popup shows an error when vehicle not found.

        Args:
            monkeypatch: Pytest fixture to mock methods.
        """
        monkeypatch.setattr(self.app.tree, "identify_row", lambda y: "row1")

        # Ensure values contain less than 3 elements to simulate missing data
        monkeypatch.setattr(
            self.app.tree, "item",
            lambda item, option: {"values": ["", ""]}
        )
        monkeypatch.setattr(
            self.app.manager, "search_vehicles", lambda *args: []
        )

        class MockEvent:
            def __init__(self) -> None:
                self.y = 100

        self.app.edit_vehicle_popup(event=MockEvent())

        # Now assert the correct expected message
        assert len(self.captured_messages) > 0, (
            f"Expected at least one error message, got: "
            f"{self.captured_messages}"
        )
        assert any("Invalid row data. Cannot edit vehicle." in msg[1]
                   for msg in self.captured_messages), (
            "Expected 'Invalid row data. Cannot edit vehicle.', but got: "
            f"{self.captured_messages}")

    def test_apply_filters(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Ensure filters are applied correctly without errors.

        Args:
            monkeypatch: Pytest fixture to mock methods.
        """
        monkeypatch.setattr(
            TkFilterManager,
            "apply_filters",
            lambda self: ("SELECT * FROM Vehicles", ())
        )
        monkeypatch.setattr(
            self.app.manager,
            "search_vehicles",
            lambda query, values: [
                ["Toyota", "Camry", "ABC123"]
            ]
        )

        self.app.apply_filters()
        assert len(self.captured_messages) == 0, (
            f"Unexpected error messages: {self.captured_messages}"
        )

    def test_apply_filters_with_error(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Ensure an error message is shown if filtering fails.

        Args:
            monkeypatch: Pytest fixture to mock methods.
        """
        monkeypatch.setattr(
            TkFilterManager,
            "apply_filters",
            lambda self: ("SELECT * FROM Vehicles", ())
        )

        def mock_search_vehicles(
            query: str, values: Tuple
        ) -> None:
            raise ValueError("Invalid query")

        monkeypatch.setattr(
            self.app.manager, "search_vehicles", mock_search_vehicles
        )

        self.app.apply_filters()
        assert len(self.captured_messages) == 1, (
            "Expected an error message but none was captured."
        )
        assert len(self.captured_messages) == 1, (
            "Expected an error message but none was captured."
        )

    def test_clear_filters(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Ensure clearing filters resets the vehicle list.

        Args:
            monkeypatch: Pytest fixture to mock methods.
        """
        monkeypatch.setattr(
            TkFilterManager, "clear_filters", lambda self: None
        )
        monkeypatch.setattr(self.app, "list_all_vehicles", lambda: None)
        self.app.clear_filters()
        assert len(self.captured_messages) == 0  # No errors expected

    def test_list_all_vehicles(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Ensure vehicle list updates correctly.

        Args:
            monkeypatch: Pytest fixture to mock methods.
        """
        monkeypatch.setattr(
            self.app.manager, "search_vehicles", lambda query: [["Vehicle1"]]
        )
        monkeypatch.setattr(self.app, "update_treeview", lambda records: None)
        self.app.list_all_vehicles()
        assert len(self.captured_messages) == 0  # No errors expected
