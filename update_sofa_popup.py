import tkinter as tk
from tkinter import messagebox
import requests
import re
import json
from sofa import Sofa


class UpdateSofaPopup(tk.Frame):
    """ Popup Frame to Add a Sofa """

    def __init__(self, parent, close_callback):
        """ Constructor """

        tk.Frame.__init__(self, parent)
        self._close_cb = close_callback
        self.grid(rowspan=2, columnspan=2)

        # Entry boxes
        tk.Label(self, text="Serial Num:").grid(row=1, column=1)
        self._serial_num = tk.Entry(self)
        self._serial_num.grid(row=1, column=2)

        tk.Label(self, text="Item Brand:").grid(row=2, column=1)
        self._item_brand = tk.Entry(self)
        self._item_brand.grid(row=2, column=2)

        tk.Label(self, text="Year Manufactured:").grid(row=3, column=1)
        self._year_manufactured = tk.Entry(self)
        self._year_manufactured.grid(row=3, column=2)

        tk.Label(self, text="Cost:").grid(row=4, column=1)
        self._cost = tk.Entry(self)
        self._cost.grid(row=4, column=2)

        tk.Label(self, text="Price:").grid(row=5, column=1)
        self._price = tk.Entry(self)
        self._price.grid(row=5, column=2)

        tk.Label(self, text="Number of Seats:").grid(row=6, column=1)
        self._num_seats = tk.Entry(self)
        self._num_seats.grid(row=6, column=2)

        tk.Label(self, text="Number of Cushions:").grid(row=7, column=1)
        self._num_cushions = tk.Entry(self)
        self._num_cushions.grid(row=7, column=2)

        tk.Label(self, text="Old Item ID:").grid(row=8, column=1)
        self._id = tk.Entry(self)
        self._id.grid(row=8, column=2)

        # Submit and close
        tk.Button(self, text="Submit", command=self._submit_cb).grid(row=9, column=1)
        tk.Button(self, text="Close", command=self._close_cb).grid(row=9, column=2)

    def _submit_cb(self):
        """ Submit the Update Sofa """

        if re.match(r"^[0-9][0-9]?$|^100$", self._id.get()) is None:
            messagebox.showerror("Error", "ID must be an integer.")
            return

        # Validate the non-string data values
        if re.match(r"^\d{4}$", self._year_manufactured.get()) is None:
            messagebox.showerror("Error", "Year manufactured must have format yyyy")
            return

        if re.match(r"^\d+.\d{2}$", self._cost.get()) is None:
            messagebox.showerror("Error", "Bed cost must be a valid cost e.g. $dd.dd")
            return

        if re.match(r"^\d+.\d{2}$", self._price.get()) is None:
            messagebox.showerror("Error", "Bed price must be a valid price e.g. $dd.dd")
            return

        if re.match(r"^\d$", self._num_cushions.get()) is None:
            messagebox.showerror(
                "Error", "Number of cushions must a single digit integer."
            )
            return

        if re.match(r"^\d$", self._num_seats.get()) is None:
            messagebox.showerror(
                "Error", "Number of seats must a single digit integer."
            )
            return

        # Create the dictionary for the JSON request body
        data = {}
        data["type"] = Sofa.FURNITURE_TYPE
        data["item_serial_num"] = self._serial_num.get()
        data["item_brand"] = self._item_brand.get()
        data["year_manufactured"] = self._year_manufactured.get()
        data["cost"] = float(self._cost.get())
        data["price"] = float(self._price.get())
        data["number_of_seats"] = self._num_seats.get()
        data["number_of_cushions"] = self._num_cushions.get()

        # Implement your code here
        response = requests.put(
            url="http://localhost:5000/furnituremanager/items/" + self._id.get(),
            data=json.dumps(data),
            headers={"content-type": "application/json"},
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
