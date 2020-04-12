import json


class FurnitureStats:
    """ FurnitureStats class """

    def __init__(
        self,
        num_total_items,
        num_items_sold,
        num_sold_sofas,
        num_unsold_sofas,
        num_sold_beds,
        num_unsold_beds,
        total_profit,
    ):
        """ Constructor """
        self._num_items_sold = num_items_sold
        self._num_total_items = num_total_items
        self._num_sold_sofas = num_sold_sofas
        self._num_sold_beds = num_sold_beds
        self._num_unsold_beds = num_unsold_beds
        self._num_unsold_sofas = num_unsold_sofas
        self._total_profit = total_profit

    def get_num_sold_sofas(self):
        """
        Returns the total number of sold sofas
        :return: number of sofas
        """
        return self._num_sold_sofas

    def get_num_sold_beds(self):
        """
        Returns the total number of sold beds
        :return: number of beds
        """
        return self._num_sold_beds

    def get_num_unsold_sofas(self):
        """
        Returns the total number of unsold sofas
        :return: number of sofas
        """
        return self._num_unsold_sofas

    def get_num_unsold_beds(self):
        """
        Returns the total number of unsold beds
        :return: number of beds
        """
        return self._num_unsold_beds

    def get_num_total_items(self):
        """
        Returns the total number of items
        :return: total number of items
        """
        return self._num_total_items

    def get_num_items_sold(self):
        """
        Returns the total number of items sold
        :return: total number of sofas
        """
        return self._num_items_sold

    def get_total_profit(self):
        """
        Returns the total profit made from sold items
        :return: profit
        """
        return self._total_profit

    def to_dict(self):
        """
        Returns dictionary representation of furniture stats
        :return: dictionay
        """
        return_dict = {}
        return_dict["num_items_sold"] = self.get_num_items_sold()
        return_dict["num_total_items"] = self.get_num_total_items()
        return_dict["num_sold_beds"] = self.get_num_sold_beds()
        return_dict["num_unsold_beds"] = self.get_num_unsold_beds()
        return_dict["num_sold_sofas"] = self.get_num_sold_sofas()
        return_dict["num_unsold_sofas"] = self.get_num_unsold_sofas()
        return_dict["total_profit"] = self.get_total_profit()

        return return_dict
