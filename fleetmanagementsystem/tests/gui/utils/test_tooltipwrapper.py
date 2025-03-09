import pytest
import tkinter as tk
from tkinter import ttk
from time import sleep
from fleetmanagementsystem.gui.utils.tooltipwrapper import Tooltip
from fleetmanagementsystem.gui.utils.tooltipwrapper import TooltipWrapper


class TestTooltip:
    """Test suite for the Tooltip class."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup a root Tk instance and a tooltip instance."""
        self.root = tk.Tk()
        self.root.withdraw()  # Prevent UI from showing
        self.tooltip = Tooltip(self.root, text="Test Tooltip")
        yield
        self.tooltip.destroy()
        self.root.destroy()

    def test_tooltip_initialization(self):
        """Ensure Tooltip initializes correctly."""
        assert isinstance(self.tooltip, Tooltip)
        assert isinstance(self.tooltip.label, ttk.Label)
        assert self.tooltip.label["text"] == "Test Tooltip"

    def test_tooltip_opacity(self):
        """Ensure tooltip supports custom alpha (opacity) values."""
        self.tooltip["alpha"] = 0.5
        assert self.tooltip["alpha"] == 0.5

    def test_tooltip_label_configuration(self):
        """Ensure tooltip label configuration is applied correctly."""
        self.tooltip.configure(text="New Tooltip")

        assert self.tooltip.label["text"] == "New Tooltip"


class TestTooltipWrapper:
    """Test suite for the TooltipWrapper class."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup a root Tk instance and a tooltip wrapper instance."""
        self.root = tk.Tk()
        self.root.withdraw()  # Prevent UI from showing
        self.wrapper = TooltipWrapper(
            self.root, text="Default Tooltip", delay=100
        )
        self.button = tk.Button(self.root, text="Hover Me")
        self.button.pack()
        yield
        self.wrapper.tooltip.destroy()
        self.button.destroy()
        self.root.destroy()

    def test_tooltip_wrapper_initialization(self):
        """Ensure TooltipWrapper initializes correctly."""
        assert isinstance(self.wrapper, TooltipWrapper)
        assert isinstance(self.wrapper.tooltip, Tooltip)

    def test_add_tooltip(self):
        """Ensure tooltips can be added to widgets."""
        self.wrapper.add_tooltip(self.button, "Button Tooltip")
        assert self.wrapper.widgets[str(self.button)] == "Button Tooltip"

    def test_set_tooltip_text(self):
        """Ensure tooltip text can be updated dynamically."""
        self.wrapper.add_tooltip(self.button, "Old Text")
        self.wrapper.set_tooltip_text(self.button, "Updated Text")
        assert self.wrapper.widgets[str(self.button)] == "Updated Text"

    def test_remove_tooltip(self):
        """Ensure tooltips can be removed from widgets."""
        self.wrapper.add_tooltip(self.button, "Test Tooltip")
        self.wrapper.remove_tooltip(self.button)
        assert str(self.button) not in self.wrapper.widgets

    def test_remove_all_tooltips(self):
        """Ensure all tooltips can be removed at once."""
        btn2 = tk.Button(self.root, text="Another Button")
        self.wrapper.add_tooltip(self.button, "Tooltip 1")
        self.wrapper.add_tooltip(btn2, "Tooltip 2")

        self.wrapper.remove_all()
        assert not self.wrapper.widgets  # Dictionary should be empty

    def test_tooltip_disappears_on_leave(self):
        """Ensure tooltip disappears when the mouse leaves the widget."""
        self.wrapper.add_tooltip(self.button, "Hover Tooltip")

        # Simulate mouse entering and leaving the widget
        event = tk.Event()
        event.widget = self.button
        self.wrapper._on_enter(event)
        sleep(0.2)  # Allow tooltip to display

        self.wrapper._on_leave(event)
        assert not self.wrapper.tooltip.winfo_ismapped(), \
            "Tooltip should be hidden after leaving"

    def test_tooltip_not_displayed_for_disabled_widget(self):
        """Ensure tooltips are not displayed for disabled widgets."""
        self.button.config(state="disabled")
        self.wrapper.add_tooltip(self.button, "Disabled Tooltip")

        # Simulate mouse entering the disabled widget
        event = tk.Event()
        event.widget = self.button
        self.wrapper._on_enter(event)
        sleep(0.2)

        assert not self.wrapper.tooltip.winfo_ismapped(), \
            "Tooltip should not be shown for disabled widgets"
