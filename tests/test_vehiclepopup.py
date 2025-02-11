# import pytest
# import tkinter as tk
# from vehiclepopup import VehiclePopup
# from utils.customdatepicker import CustomDatePicker
# from vehiclemanager import VehicleManager
# from appmessage import AppMessage
# from customtypes import VehiclePopupAction
# import datetime


# @pytest.fixture
# def mock_vehicle_manager(mocker):
#     """Fixture to create a mock VehicleManager."""
#     return mocker.MagicMock(spec=VehicleManager)


# @pytest.fixture
# def mock_root():
#     """Fixture to create a mock Tkinter root window."""
#     root = tk.Tk()
#     yield root
#     root.destroy()


# @pytest.fixture
# def mock_appmessage(mocker):
#     """Fixture to mock the AppMessage.show function to suppress UI popups."""
#     return mocker.patch.object(AppMessage, "show")


# @pytest.fixture
# def vehicle_popup_add(mock_root, mock_vehicle_manager):
#     """Fixture to create a VehiclePopup instance in 'add' mode."""
#     return VehiclePopup(mock_root, mock_vehicle_manager, lambda: None, VehiclePopupAction.ADD)


# @pytest.fixture
# def vehicle_popup_edit(mock_root, mock_vehicle_manager):
#     """Fixture to create a VehiclePopup instance in 'edit' mode with test data."""
#     vehicle_data = {
#         "Registration Number": "ABC123",
#         "Manufacture Year": "2020",
#         "Type": "Car",
#         "Tax Due Date": "2025-05-10",
#         "Service Date": "2025-06-15",
#         "Tax Status": "Valid",
#         "Tax Type": "Annual",
#         "Fuel Type": "Petrol",
#     }
#     return VehiclePopup(mock_root, mock_vehicle_manager, lambda: None, VehiclePopupAction.EDIT, vehicle_data)


# def test_vehicle_popup_initialization(vehicle_popup_add, vehicle_popup_edit):
#     """Test initialization of VehiclePopup in both add and edit modes."""
#     assert vehicle_popup_add.popup.title() == "Add Vehicle"
#     assert vehicle_popup_edit.popup.title() == "Edit Vehicle"
#     assert vehicle_popup_add.mode == VehiclePopupAction.ADD
#     assert vehicle_popup_edit.mode == VehiclePopupAction.EDIT
#     assert "Registration Number" in vehicle_popup_add.inputs
#     assert "Manufacture Year" in vehicle_popup_edit.inputs


# def test_create_widgets_creates_correct_fields(vehicle_popup_add):
#     """Test that all expected widgets are created in the popup."""
#     fields = [
#         "Registration Number",
#         "Manufacture Year",
#         "Type",
#         "Tax Due Date",
#         "Service Date",
#         "Tax Status",
#         "Tax Type",
#         "Fuel Type",
#     ]
#     for field in fields:
#         assert field in vehicle_popup_add.inputs


# def test_datepicker_widget_initialization(vehicle_popup_add):
#     """Ensure that the date picker widget is correctly instantiated."""
#     assert isinstance(vehicle_popup_add.inputs["Tax Due Date"], CustomDatePicker)
#     assert isinstance(vehicle_popup_add.inputs["Service Date"], CustomDatePicker)


# @pytest.mark.parametrize(
#     "field,value,expected",
#     [
#         ("Manufacture Year", "2020", 2020),
#         ("Manufacture Year", "abc", "error"),  # Invalid integer
#         ("Tax Due Date", "2025-05-10", "2025-05-10"),
#         ("Tax Due Date", "invalid_date", "error"),  # Invalid date
#         ("Registration Number", "ABC123", "ABC123"),
#         ("Registration Number", "", "error"),  # Empty string
#     ],
# )
# def test_save_changes_validation(
#     vehicle_popup_add, mock_appmessage, field, value, expected
# ):
#     """Test validation in save_changes method for different input fields."""
#     vehicle_popup_add.inputs[field].delete(0, tk.END)
#     vehicle_popup_add.inputs[field].insert(0, value)

#     if expected == "error":
#         with pytest.raises(Exception):
#             vehicle_popup_add.save_changes()
#             assert mock_appmessage.call_count == 1
#             assert "Validation Error" in mock_appmessage.call_args[0][1]


# def test_save_changes_calls_manager_correctly(vehicle_popup_add, mock_vehicle_manager):
#     """Ensure that the VehicleManager method is called when saving."""
#     vehicle_popup_add.inputs["Registration Number"].insert(0, "XYZ789")
#     vehicle_popup_add.inputs["Manufacture Year"].insert(0, "2019")

#     vehicle_popup_add.save_changes()

#     assert mock_vehicle_manager.add_vehicle.call_count == 1


# def test_delete_vehicle_calls_manager_correctly(vehicle_popup_edit, mock_vehicle_manager):
#     """Ensure that the delete function calls the correct VehicleManager method."""
#     vehicle_popup_edit.delete_vehicle()

#     assert mock_vehicle_manager.remove_vehicle.call_count == 1


# def test_delete_vehicle_shows_success_message(vehicle_popup_edit, mock_appmessage):
#     """Ensure a success message is displayed after deleting a vehicle."""
#     vehicle_popup_edit.delete_vehicle()

#     assert mock_appmessage.call_count == 1
#     assert "Vehicle deleted successfully" in mock_appmessage.call_args[0][1]
