import tkinter as tk
import requests
from add_bed_popup import AddBedPopup
from add_sofa_popup import AddSofaPopup
from remove_item_popup import RemoveItemPopup
from update_bed_popup import UpdateBedPopup
from update_sofa_popup import UpdateSofaPopup


class MainAppController(tk.Frame):
    """ Main Application for GUI """

    def __init__(self, parent):
        """ Initialize Main Application """
        tk.Frame.__init__(self, parent)
        self._popup_win = None

        self._references = {"sofas": {}, "beds": {}}

        tk.Label(self, text="Furniture shop inventory").grid(row=1, column=5)

        self._item_type_to_display = tk.IntVar()
        tk.Label(self, text="Show me:").grid(row=3, column=3)
        tk.Radiobutton(
            self,
            variable=self._item_type_to_display,
            value=1,
            text="Beds",
            command=self._update_items_list,
        ).grid(row=3, column=5)
        tk.Radiobutton(
            self,
            variable=self._item_type_to_display,
            value=0,
            text="Sofas",
            command=self._update_items_list,
        ).grid(row=3, column=4)

        self._items_listbox = tk.Listbox(self, width=110)
        self._items_listbox.bind("<Double-Button-1>", self._show_item_details)
        self._items_listbox.grid(row=4, column=3, columnspan=10)

        tk.Button(self, text="Quit", command=self._quit_callback).grid(row=10, column=2)
        tk.Button(self, text="Add Bed", command=self._add_bed).grid(row=10, column=3)
        tk.Button(self, text="Add Sofa", command=self._add_sofa).grid(row=10, column=4)
        tk.Button(self, text="Remove Item", command=self._remove_item).grid(
            row=10, column=5
        )
        tk.Button(self, text="Update Bed", command=self._update_bed).grid(
            row=10, column=6
        )
        tk.Button(self, text="Update Sofa", command=self._update_sofa).grid(
            row=10, column=7
        )

        self._update_items_list()

    def _quit_callback(self):
        """ Quit """
        self.quit()

    def _close_popup(self):
        self._popup_win.destroy()
        self._update_items_list()

    def _remove_item(self):
        """ Opens the remove item popup """
        self._popup_win = tk.Toplevel()
        self._popup = RemoveItemPopup(self._popup_win, self._close_popup)

    def _add_bed(self):
        """ Opens the add bed popup """
        self._popup_win = tk.Toplevel()
        self._popup = AddBedPopup(self._popup_win, self._close_popup)

    def _add_sofa(self):
        """ Opens the add sofa popup """
        self._popup_win = tk.Toplevel()
        self._popup = AddSofaPopup(self._popup_win, self._close_popup)

    def _update_bed(self):
        """ Opens the update bed popup """
        self._popup_win = tk.Toplevel()
        self._popup = UpdateBedPopup(self._popup_win, self._close_popup)

    def _update_sofa(self):
        """ Opens the update sofa popup """
        self._popup_win = tk.Toplevel()
        self._popup = UpdateSofaPopup(self._popup_win, self._close_popup)

    def _show_item_details(self, evt):
        """ Displays details about an item selected from the listbox, on the right side """
        w = evt.widget
        index = int(w.curselection()[0])
        select = "sofas"

        if self._item_type_to_display.get() == 1:
            select = "beds"

        print(self._references[select])

        response = requests.get(
            url="http://localhost:5000/furnituremanager/items/"
            + str(self._references[select][index])
        )

        if response.status_code == 200:
            txt = ""

            for key, value in response.json().items():
                key = key.replace("_", " ")
                key = key.replace("num", "number of ")
                txt += key + ": " + str(value) + "\n"

            tk.Label(self, text=txt).grid(row=4, column=15)

    def _update_items_list(self):
        """ Update the List of item Descriptions """

        if self._item_type_to_display.get() == 0:
            response = requests.get(
                "http://localhost:5000/furnituremanager/items/all/descriptions/sofa"
            )
            sofas = response.json()

            if response.status_code == 200:
                self._items_listbox.delete(0, tk.END)

                for i in range(len(sofas)):
                    self._references["sofas"][i] = sofas[i]["id"]
                    self._items_listbox.insert(tk.END, sofas[i]["desc"])
        else:
            response = requests.get(
                "http://localhost:5000/furnituremanager/items/all/descriptions/bed"
            )
            beds = response.json()

            if response.status_code == 200:
                self._items_listbox.delete(0, tk.END)

                for i in range(len(beds)):
                    self._references["beds"][i] = beds[i]["id"]
                    self._items_listbox.insert(tk.END, beds[i]["desc"])

        response = requests.get("http://localhost:5000/furnituremanager/items/stats")
        stats = response.json()

        if response.status_code == 200:
            txt = ""

            for stat_name, stat in stats.items():
                stat_name = stat_name.replace("_", " ")
                stat_name = stat_name.replace("num", "number of ")
                txt += stat_name + ": " + str(stat) + "\n"

            tk.Label(self, text=txt).grid(row=4, column=1)


if __name__ == "__main__":
    root = tk.Tk()
    MainAppController(root).pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    root.mainloop()

