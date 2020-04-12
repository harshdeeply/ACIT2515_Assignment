import tkinter as tk
from tkinter import messagebox
import requests


class RemoveItemPopup(tk.Frame):
    """ Popup Frame to remove an item """

    def __init__(self, parent, close_callback):
        """ Constructor """

        tk.Frame.__init__(self, parent)
        self._close_cb = close_callback
        self.grid(rowspan=2, columnspan=2)

        tk.Label(self, text="Item ID:").grid(row=1, column=1)
        self._serial_num = tk.Entry(self)
        self._serial_num.grid(row=1, column=2)
        tk.Button(self, text="Submit", command=self._submit_cb).grid(row=7, column=1)
        tk.Button(self, text="Close", command=self._close_cb).grid(row=7, column=2)

    def _submit_cb(self):
        """ submit request to remove item """

        # Implement your code here
        response = requests.delete(
            url="http://localhost:5000/furnituremanager/items/"
            + self._serial_num.get(),
        )

        if response.status_code == 200:
            messagebox.showinfo(
                "Success", "Code " + str(response.status_code) + ": " + response.text
            )
            self._close_cb()
        else:
            messagebox.showwarning(
                "Error", "Error " + str(response.status_code) + ": " + response.text
            )
