from tkinter import messagebox
import logging


class AppMessage:
    """Custom message handling class for the Fleet Management System."""

    @staticmethod
    def show(message_type, message, error=""):
        """
        Displays a message and logs it in the terminal.

        Args:
            message_type (str): Type of the message ('info' or 'error').
            message (str): The message content to display and log.
        """
        if message_type == "info":
            logging.info(message)
            messagebox.showinfo("Information", message)
        elif message_type == "error":
            logging.error(f"{message},{error}")
            messagebox.showerror("Error", f"{message},{error}")
        elif message_type == "warning":
            logging.warning(f"{message}, {error}")
            messagebox.showwarning("Warning", f"{message},{error}")
        else:
            raise ValueError(
                "Invalid message type. Use 'info', 'error', or 'warning'."
            )
