import tkinter as tk


class ToolTip:
    """
    A class to create a dynamic tooltip that adjusts to the 
    available screen space.
    """

    def __init__(
        self, widget: tk.Widget, text: str, max_width: int = 300
    ) -> None:
        """
        Initialize the tooltip.

        Args:
            widget (tk.Widget): The widget to attach the tooltip to.
            text (str): The tooltip text to display.
            max_width (int): Maximum width of the tooltip in pixels.
                Defaults to 300.
        """
        self.widget = widget
        self.text = text
        self.max_width = max_width
        self.tooltip_window = None

        # Bind events for displaying and hiding the tooltip
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event: tk.Event) -> None:
        """
        Display the tooltip near the widget when the mouse enters.

        Args:
            event (tk.Event): The event object triggered by the mouse 
                entering the widget.
        """
        if self.tooltip_window:
            return  # Prevent multiple tooltip windows

        # Create the tooltip window
        self.tooltip_window = tk.Toplevel(self.widget)
        # Remove window decorations
        self.tooltip_window.wm_overrideredirect(True)
        # Keep it on top
        self.tooltip_window.attributes("-topmost", True)

        # Create and configure the tooltip label
        label = tk.Label(
            self.tooltip_window,
            text=self.text,
            justify="left",
            wraplength=self.max_width,
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            padx=0,
            pady=0,
        )
        label.pack()

        # Get the mouse pointer's position
        x = self.widget.winfo_pointerx() + 10
        y = self.widget.winfo_pointery() + 10

        # Adjust placement to fit within screen bounds
        screen_width = self.widget.winfo_screenwidth()
        screen_height = self.widget.winfo_screenheight()
        tooltip_width = self.tooltip_window.winfo_reqwidth()
        tooltip_height = self.tooltip_window.winfo_reqheight()

        if x + tooltip_width > screen_width:
            x = x - tooltip_width - 10
        if y + tooltip_height > screen_height:
            y = y - tooltip_height - 10

        # Set the position of the tooltip window
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

    def hide_tooltip(self, event: tk.Event) -> None:
        """
        Hide the tooltip when the mouse leaves the widget.

        Args:
            event (tk.Event): The event object triggered by the mouse 
            leaving the widget.
        """
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

    def update_text(self, new_text: str) -> None:
        """
        Update the tooltip text dynamically.

        Args:
            new_text (str): The new text to display in the tooltip.
        """
        self.text = new_text
