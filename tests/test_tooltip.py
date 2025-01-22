import tkinter as tk
import pytest

from tooltip import ToolTip

class TestToolTip:
    """Test suite for the ToolTip class."""

    @pytest.fixture
    def setup_tooltip(self):
        """Set up a tkinter root, widget, and tooltip instance."""
        root = tk.Tk()
        widget = tk.Label(root, text="Hover over me")
        widget.pack()
        tooltip = ToolTip(widget, text="This is a tooltip", max_width=300)
        return root, widget, tooltip

    def test_tooltip_initialization(self, setup_tooltip):
        """Test if the ToolTip initializes with correct attributes."""
        _, _, tooltip = setup_tooltip
        assert tooltip.text == "This is a tooltip"
        assert tooltip.max_width == 300
        assert tooltip.tooltip_window is None

    def test_show_tooltip_creates_window(self, setup_tooltip):
        """Test if the tooltip window is created on hover."""
        root, widget, tooltip = setup_tooltip

        # Simulate hover event
        event = tk.Event()
        event.x, event.y = 10, 10
        tooltip.show_tooltip(event)

        assert tooltip.tooltip_window is not None
        assert isinstance(tooltip.tooltip_window, tk.Toplevel)

        root.destroy()

    def test_hide_tooltip_destroys_window(self, setup_tooltip):
        """Test if the tooltip window is destroyed on mouse leave."""
        root, widget, tooltip = setup_tooltip

        # Simulate hover and leave events
        event = tk.Event()
        event.x, event.y = 10, 10
        tooltip.show_tooltip(event)
        assert tooltip.tooltip_window is not None

        tooltip.hide_tooltip(event)
        assert tooltip.tooltip_window is None

        root.destroy()

    def test_tooltip_positioning(self, setup_tooltip):
        """Test if the tooltip adjusts to screen bounds."""
        root, widget, tooltip = setup_tooltip

        # Simulate hover event
        event = tk.Event()
        event.x, event.y = 10, 10
        tooltip.show_tooltip(event)

        screen_width = widget.winfo_screenwidth()
        screen_height = widget.winfo_screenheight()
        tooltip_width = tooltip.tooltip_window.winfo_reqwidth()
        tooltip_height = tooltip.tooltip_window.winfo_reqheight()

        x = widget.winfo_pointerx() + 10
        y = widget.winfo_pointery() + 10

        if x + tooltip_width > screen_width:
            x = screen_width - tooltip_width - 10
        if y + tooltip_height > screen_height:
            y = screen_height - tooltip_height - 10

        tooltip_x, tooltip_y = map(int, tooltip.tooltip_window.geometry().split("+")[1:])

        assert tooltip_x == x
        assert tooltip_y == y

        root.destroy()

    def test_update_text(self, setup_tooltip):
        """Test if the tooltip text can be updated dynamically."""
        root, widget, tooltip = setup_tooltip

        # Update text
        new_text = "New tooltip text"
        tooltip.update_text(new_text)
        assert tooltip.text == new_text

        # Simulate hover and check tooltip content
        event = tk.Event()
        event.x, event.y = 10, 10
        tooltip.show_tooltip(event)

        label = tooltip.tooltip_window.winfo_children()[0]
        assert label.cget("text") == new_text

        root.destroy()
