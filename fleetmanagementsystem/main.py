import tkinter as tk
from fleetmanagementsystem.gui.fleetapp import FleetApp
# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = FleetApp(root)
    root.mainloop()
