import tkinter as tk
from tkinter import ttk
from appmessage import AppMessage
import datetime


class CustomDatePicker(tk.Frame):
    popup_instance = None

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        try:
            self.parent = parent

            self.month_short_names = [
                "Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
            ]

            self.month_days = {
                "Jan": 31, "Feb": 28, "Mar": 31, "Apr": 30,
                "May": 31, "Jun": 30, "Jul": 31, "Aug": 31,
                "Sep": 30, "Oct": 31, "Nov": 30, "Dec": 31
            }

            # Entry field with dropdown arrow
            self.date_var = tk.StringVar()
            self.entry = ttk.Combobox(
                self, textvariable=self.date_var, width=20, state="readonly"
            )
            self.entry.pack(fill=tk.X, expand=True)
            # Open popup when clicked
            self.entry.bind("<Button-1>", self.open_date_picker)

            # Initialize variables to prevent AttributeError
            self.year_var = tk.IntVar()
            self.month_var = tk.StringVar()
            self.day_var = tk.IntVar()

            # Set default date to current date
            self.set_date_to_current()
        except Exception as e:
            AppMessage.show("error", "Failed to initialize date picker", e)

    def set_date_to_current(self):
        """Sets the date picker to the current date."""
        try:
            today = datetime.datetime.now()
            self.year_var.set(today.year)
            month_name = self.month_short_names[today.month - 1]
            self.month_var.set(month_name)
            self.day_var.set(today.day)
            formatted_date = today.strftime("%Y-%m-%d")
            self.date_var.set(formatted_date)
        except Exception as e:
            AppMessage.show("error", "Failed to set date to current", e)

    def insert(self, index, value):
        """Allows setting the value similar to an Entry widget."""
        try:
            self.date_var.set(value)
        except Exception as e:
            AppMessage.show("error", "Failed to insert date", e)

    def get(self) -> str:
        """Allows retrieving the value similar to an Entry widget."""
        try:
            return self.date_var.get()
        except Exception as e:
            AppMessage.show("error", "Failed to get date", e)

    def delete(self) -> None:
        """Clears the date value."""
        try:
            self.date_var.set("")
        except Exception as e:
            AppMessage.show("error", "Failed to delete date", e)

    def open_date_picker(self, event=None) -> None:
        """Opens a popup window to select a date."""
        try:
            if CustomDatePicker.popup_instance:  # Close any existing popup
                CustomDatePicker.popup_instance.destroy()
                CustomDatePicker.popup_instance = None

            self.popup = tk.Toplevel(self.parent)
            CustomDatePicker.popup_instance = self.popup
            self.popup.title("Select Date")
            self.popup.geometry("250x200")

            # Year dropdown
            current_year = datetime.datetime.now().year
            years = list(range(1999, current_year + 1))
            self.year_dropdown = ttk.Combobox(
                self.popup, textvariable=self.year_var, values=years,
                state="readonly"
            )
            self.year_dropdown.grid(row=0, column=1, padx=10, pady=5)
            self.year_dropdown.set(self.year_var.get())

            # Month dropdown
            month_values = self.month_short_names
            self.month_dropdown = ttk.Combobox(
                self.popup, textvariable=self.month_var, values=month_values,
                state="readonly"
            )
            self.month_dropdown.grid(row=1, column=1, padx=10, pady=5)
            self.month_dropdown.set(self.month_var.get())
            self.month_dropdown.bind("<<ComboboxSelected>>", self.update_days)

            # Day dropdown
            self.day_dropdown = ttk.Combobox(
                self.popup, textvariable=self.day_var, state="readonly"
            )
            self.day_dropdown.grid(row=2, column=1, padx=10, pady=5)
            self.update_days()

            # Labels
            tk.Label(self.popup, text="Year:")\
                .grid(row=0, column=0, padx=5, pady=5)
            tk.Label(self.popup, text="Month:")\
                .grid(row=1, column=0, padx=5, pady=5)
            tk.Label(self.popup, text="Day:").grid(
                row=2, column=0, padx=5, pady=5
            )

            # Submit button
            submit_button = tk.Button(
                self.popup, text="Confirm", command=self.set_date
            )
            submit_button.grid(row=3, column=0, columnspan=2, pady=10)
        except Exception as e:
            AppMessage.show("error", "Failed to open date picker", e)

    def update_days(self, event=None):
        """Updates the day dropdown based on the selected month."""
        try:
            if not hasattr(self, 'day_dropdown'):
                return
            month_days = self.month_days
            month = self.month_var.get()
            if month in month_days:
                days = [str(day) for day in range(1, month_days[month] + 1)]
                self.day_dropdown["values"] = days
                if str(self.day_var.get()) not in days:
                    self.day_var.set(days[0])
                    self.day_dropdown.set(days[0])
        except Exception as e:
            AppMessage.show("error", "Failed to update days", e)

    def set_date(self, date_str=None):
        """
        Sets the date picker to a given date string (YYYY-MM-DD)
        or defaults to current date.
        """
        try:
            if date_str:
                try:
                    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    # Fallback to current date if invalid
                    date_obj = datetime.datetime.now()
            else:
                date_obj = datetime.datetime.now()

            self.year_var.set(date_obj.year)
            self.month_var.set(self.month_short_names[date_obj.month - 1])
            self.day_var.set(date_obj.day)
            formatted_date = date_obj.strftime("%Y-%m-%d")
            self.date_var.set(formatted_date)

            if hasattr(self, 'popup') and self.popup:
                self.popup.destroy()
        except Exception as e:
            AppMessage.show("error", "Failed to set date", e)
