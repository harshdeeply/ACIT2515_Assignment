from sqlalchemy import Column, String
import json
from abstract_furniture import AbstractFurniture


class Bed(AbstractFurniture):
    """ Represents a bed in a Furniture shop """

    FURNITURE_TYPE = "bed"

    # Size in format 'length(cm) x width(cm)' = '180cm x 80cm'
    size = Column(String(12))

    # Height in format 'height(cm)' = '100cm'
    height = Column(String(5))

    def __init__(
        self, item_serial_num, year_manufactured, item_brand, cost, price, size, height
    ):

        """ Initializes the bed furniture type """

        super().__init__(
            item_serial_num,
            year_manufactured,
            item_brand,
            cost,
            price,
            Bed.FURNITURE_TYPE,
        )
        if size is None or size == "":
            raise ValueError("Bed size cannot be empty")
        if type(size) != str:
            raise ValueError("Bed size must be a string")
        if height is None or height == "":
            raise ValueError("Bed height cannot be empty")
        if type(height) != str:
            raise ValueError("Bed height must be a string")

        self.size = size
        self.height = height

    def get_item_type(self):
        """ Returns the furniture type as bed """
        return Bed.FURNITURE_TYPE

    def to_dict(self):
        """ Return the dictionary representation of a bed """
        return_dict = {}
        return_dict["id"] = self.id
        return_dict["type"] = self.get_item_type()
        return_dict["item_serial_num"] = self.item_serial_number
        return_dict["item_brand"] = self.item_brand
        return_dict["year_manufactured"] = self.year_manufactured
        return_dict["cost"] = self.cost
        return_dict["price"] = self.price
        return_dict["is_sold"] = self.is_sold
        return_dict["size"] = self.size
        return_dict["height"] = self.height

        # return json.dumps(return_dict, indent=4)
        return return_dict

    def get_item_description(self):
        """ Returns the description of the furniture product """
        details = (
            "%s with serial number %s manufactured by %s with %s dimensions and %s height is available for "
            "$%.2f"
            % (
                Bed.FURNITURE_TYPE,
                self.item_serial_number,
                self.item_brand,
                self.size,
                self.height,
                self.price,
            )
        )
        return details
