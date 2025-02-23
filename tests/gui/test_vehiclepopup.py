import pytest
import tkinter as tk
from tkinter import ttk
from gui.vehiclepopup import VehiclePopup
from gui.utils.appmessage import AppMessage
from typing import Generator, List, Tuple


class MockVehicleManager:
    """Mock class to replace VehicleManager."""

    def __init__(self) -> None:
        self.vehicles = []
        self.removed_vehicles = []

    def add_vehicle(self, vehicle: dict) -> None:
        self.vehicles.append(vehicle)

    def update_vehicle(self, vehicle_id: int, **updates: dict) -> None:
        pass  # Simulate update without real logic

    def remove_vehicle(self, vehicle_id: int) -> None:
        if vehicle_id == 999:
            raise Exception("Database error")  # Simulated failure
        self.removed_vehicles.append(vehicle_id)


class TestVehiclePopup:
    """Test suite for the VehiclePopup class."""

    @pytest.fixture(scope="module", autouse=True)
    def root_tk(self) -> Generator[tk.Tk, None, None]:
        """Creates a global Tkinter root to avoid multiple root errors."""
        root = tk.Tk()
        root.withdraw()  # Prevent real GUI from showing
        yield root
        root.destroy()  # Ensure Tkinter cleans up after tests

    @pytest.fixture
    def setup(
        self, root_tk: tk.Tk
    ) -> Tuple[tk.Tk, MockVehicleManager, callable]:
        """Fixture to set up a test environment.

        Args:
            root_tk: The Tkinter root instance.

        Returns:
            Tuple containing the Tkinter root, MockVehicleManager instance,
            and a mock list_all_vehicles function.
        """
        manager = MockVehicleManager()

        def mock_list_all_vehicles() -> None:
            pass  # Simulated function

        return root_tk, manager, mock_list_all_vehicles

    @pytest.fixture
    def mock_popup(
        self,
        setup: Tuple[tk.Tk, MockVehicleManager, callable],
        monkeypatch: pytest.MonkeyPatch,
    ) -> Generator[
        Tuple[VehiclePopup, List[Tuple[str, str, str]]], None, None
    ]:
        """Fixture to create a fresh VehiclePopup instance per test.

        Args:
            setup: The setup fixture.
            monkeypatch: Pytest fixture to mock methods.

        Yields:
            Tuple containing the VehiclePopup instance and a list of
            captured messages.
        """
        root, manager, list_all_vehicles = setup
        popup = VehiclePopup(
            tk.Toplevel(root), manager, list_all_vehicles, "add"
        )
        popup.popup.withdraw()  # Prevent UI interference

        # Mock `AppMessage.show()` using monkeypatch
        calls: List[Tuple[str, str, str]] = []
        monkeypatch.setattr(
            AppMessage,
            "show",
            lambda msg_type, msg, e=None: calls.append(
                (msg_type, msg, str(e) if e else None)
            ),
        )

        yield popup, calls
        popup.popup.destroy()  # Ensure cleanup to avoid Tkinter lock issues

    def test_popup_initialization(
        self, mock_popup: Tuple[VehiclePopup, List[Tuple[str, str, str]]]
    ) -> None:
        """Test popup initialization in 'add' mode.

        Args:
            mock_popup: The mock_popup fixture.
        """
        popup, _ = mock_popup
        assert popup.popup is not None
        assert isinstance(popup.inputs, dict)

    def test_create_widgets(
        self, mock_popup: Tuple[VehiclePopup, List[Tuple[str, str, str]]]
    ) -> None:
        """Test widget creation.

        Args:
            mock_popup: The mock_popup fixture.
        """
        popup, _ = mock_popup
        popup.create_widgets()
        assert isinstance(popup.inputs, dict)
        assert len(popup.inputs) > 0  # Ensure widgets were created

    def test_save_changes_success_add_mode(
        self, mock_popup: Tuple[VehiclePopup, List[Tuple[str, str, str]]]
    ) -> None:
        """Test saving changes in 'add' mode.

        Args:
            mock_popup: The mock_popup fixture.
        """
        popup, calls = mock_popup

        popup.inputs["Type"] = ttk.Combobox(
            popup.popup, values=["SUV", "Sedan", "Truck"],
            state="readonly"
        )
        popup.inputs["Manufacture Year"] = ttk.Entry(popup.popup)
        popup.inputs["Registration Number"] = ttk.Entry(popup.popup)
        popup.inputs["Fuel Type"] = ttk.Combobox(
            popup.popup,
            values=["Petrol", "Diesel", "Electric"],
            state="readonly"
        )
        popup.inputs["Tax Type"] = ttk.Combobox(
            popup.popup, values=["Annual", "Monthly"], state="readonly"
        )
        popup.inputs["Tax Status"] = ttk.Combobox(
            popup.popup, values=["Paid", "Unpaid"], state="readonly"
        )
        popup.inputs["Service Status"] = ttk.Combobox(
            popup.popup, values=["Done", "Pending"], state="readonly"
        )
        popup.inputs["Service Status"] = ttk.Combobox(
            popup.popup, values=["Done", "Pending"], state="readonly"
        )
        popup.inputs["Tax Due Date"] = ttk.Entry(popup.popup)
        popup.inputs["Service Due Date"] = ttk.Entry(popup.popup)

        # Place widgets inside the popup
        for field in popup.inputs.values():
            field.grid()  # Ensures they are properly placed in the UI

        # Set values after they exist
        popup.inputs["Type"].set("SUV")  # Use .set() for Combobox
        popup.inputs["Manufacture Year"].insert(0, "2022")
        popup.inputs["Registration Number"].insert(0, "ABC123")
        popup.inputs["Fuel Type"].set("Petrol")
        popup.inputs["Tax Type"].set("SORN")
        popup.inputs["Tax Status"].set("Paid")
        popup.inputs["Service Status"].set("Done")
        popup.inputs["Tax Due Date"].insert(0, "2025-12-01")
        popup.inputs["Service Due Date"].insert(0, "2025-06-15")

        popup.save_changes()

        # Ensure vehicle was added
        assert len(popup.manager.vehicles) == 1

        # Ensure success message was shown
        assert ("info", "Vehicle added successfully!", None) in calls

    def test_save_changes_invalid_data(
        self, mock_popup: Tuple[VehiclePopup, List[Tuple[str, str, str]]]
    ) -> None:
        """Ensure invalid data triggers `AppMessage.show()`.

        Args:
            mock_popup: The mock_popup fixture.
        """
        popup, calls = mock_popup
        popup.inputs["Type"] = ttk.Entry(popup.popup)
        popup.inputs["Type"].insert(0, "NONSENSE")  # Invalid number

        popup.save_changes()

        # Ensure correct error message was displayed
        assert (
            "error",
            "Validation Error",
            "Type must be a valid option."
        ) in calls

    def test_save_changes_invalid_date_format(
        self, mock_popup: Tuple[VehiclePopup, List[Tuple[str, str, str]]]
    ) -> None:
        """Ensure incorrect date format triggers an error message.

        Args:
            mock_popup: The mock_popup fixture.
        """
        popup, calls = mock_popup
        popup.inputs["Type"] = ttk.Combobox(
            popup.popup, values=["SUV", "Sedan", "Truck"], state="readonly"
        )
        popup.inputs["Manufacture Year"] = ttk.Entry(popup.popup)
        popup.inputs["Registration Number"] = ttk.Entry(popup.popup)
        popup.inputs["Fuel Type"] = ttk.Combobox(
            popup.popup,
            values=["Petrol", "Diesel", "Electric"],
            state="readonly"
        )
        popup.inputs["Tax Type"] = ttk.Combobox(
            popup.popup, values=["Annual", "Monthly"], state="readonly"
        )
        popup.inputs["Tax Status"] = ttk.Combobox(
            popup.popup, values=["Paid", "Unpaid"], state="readonly"
        )
        popup.inputs["Service Status"] = ttk.Combobox(
            popup.popup, values=["Done", "Pending"], state="readonly"
        )
        popup.inputs["Tax Due Date"] = ttk.Entry(popup.popup)
        popup.inputs["Service Due Date"] = ttk.Entry(popup.popup)

        # Place widgets inside the popup
        for field in popup.inputs.values():
            field.grid()  # Ensures they are properly placed in the UI

        # Set values after they exist
        popup.inputs["Type"].set("SUV")  # Use .set() for Combobox
        popup.inputs["Manufacture Year"].insert(0, "2022")
        popup.inputs["Registration Number"].insert(0, "ABC123")
        popup.inputs["Fuel Type"].set("Petrol")
        popup.inputs["Tax Type"].set("SORN")
        popup.inputs["Tax Status"].set("Paid")
        popup.inputs["Service Status"].set("Done")
        popup.inputs["Tax Due Date"].insert(0, "2025-1qwed2-01")
        popup.inputs["Service Due Date"].insert(0, "2025-06-15")

        popup.save_changes()

        # Ensure correct error message was displayed
        assert (
            "error",
            "Validation Error",
            "Tax Due Date must be in YYYY-MM-DD format.",
        ) in calls

    def test_save_changes_invalid_dropdown(
        self, mock_popup: Tuple[VehiclePopup, List[Tuple[str, str, str]]]
    ) -> None:
        """Ensure selecting an invalid dropdown option triggers an error
        message.

        Args:
            mock_popup: The mock_popup fixture.
        """
        popup, calls = mock_popup
        popup.inputs["Type"] = ttk.Entry(popup.popup)
        popup.inputs["Type"].insert(0, "InvalidOption")

        popup.save_changes()

        # Ensure correct error message was displayed
        assert (
            "error",
            "Validation Error",
            "Type must be a valid option."
        ) in calls

    def test_delete_vehicle_success(
        self, mock_popup: Tuple[VehiclePopup, List[Tuple[str, str, str]]]
    ) -> None:
        """Ensure vehicle deletion works correctly.

        Args:
            mock_popup: The mock_popup fixture.
        """
        popup, calls = mock_popup
        popup.vehicle_data = {2: 123}  # Simulating ID position

        popup.delete_vehicle()

        # Ensure vehicle was removed
        assert 123 in popup.manager.removed_vehicles

        # Ensure success message was shown
        assert ("info", "Vehicle deleted successfully!", None) in calls

    def test_delete_vehicle_failure(
        self, mock_popup: Tuple[VehiclePopup, List[Tuple[str, str, str]]]
    ) -> None:
        """Simulate a deletion failure and ensure an error message is
        displayed.

        Args:
            mock_popup: The mock_popup fixture.
        """
        popup, calls = mock_popup
        popup.manager.remove_vehicle = lambda x: (_ for _ in ()).throw(
            Exception("Database error")
        )  # Raise error

        popup.vehicle_data = {2: 999}  # ID 999 will trigger failure
        popup.delete_vehicle()

        # Ensure correct error message was displayed
        assert ("error", "Failed to delete vehicle", "Database error") in calls
