from sqlalchemy import Column, Integer

from abstract_furniture import AbstractFurniture


class Sofa(AbstractFurniture):
    """ Represents a sofa in a Furniture shop """

    FURNITURE_TYPE = "sofa"

    number_of_cushions = Column(Integer)
    number_of_seats = Column(Integer)

    def __init__(
        self,
        item_serial_num,
        year_manufactured,
        item_brand,
        cost,
        price,
        number_of_seats,
        number_of_cushions,
    ):

        """ Initializes the sofa furniture type """

        super().__init__(
            item_serial_num,
            year_manufactured,
            item_brand,
            cost,
            price,
            Sofa.FURNITURE_TYPE,
        )
        if number_of_seats is None or number_of_seats == "":
            raise ValueError("Number of seats cannot be empty")
        if type(number_of_seats) != int or number_of_seats <= 0:
            raise ValueError("Number of seats must be a positive integer")
        if number_of_cushions is None or number_of_cushions == "":
            raise ValueError("Number of cushions cannot be empty")
        if type(number_of_cushions) != int or number_of_cushions <= 0:
            raise ValueError("Number of cushions must be a positive integer")

        self.number_of_seats = number_of_seats
        self.number_of_cushions = number_of_cushions

    def get_item_type(self):
        """ Returns the furniture type as sofa """
        return Sofa.FURNITURE_TYPE

    def to_dict(self):
        """ Returns the dictionary representation of a sofa """
        return_dict = {}
        return_dict["id"] = self.id
        return_dict["type"] = self.get_item_type()
        return_dict["item_serial_num"] = self.item_serial_number
        return_dict["item_brand"] = self.item_brand
        return_dict["year_manufactured"] = self.year_manufactured
        return_dict["cost"] = self.cost
        return_dict["price"] = self.price
        return_dict["is_sold"] = self.is_sold
        return_dict["number_of_seats"] = self.number_of_seats
        return_dict["number_of_cushions"] = self.number_of_cushions

        # return json.dumps(return_dict, indent=4)
        return return_dict

    def get_item_description(self):
        details = (
            "%s with serial number %s manufactured by %s with %d number of seats and %d number of cushions is available for $%.2f"
            % (
                Sofa.FURNITURE_TYPE,
                self.item_serial_number,
                self.item_brand,
                self.number_of_seats,
                self.number_of_cushions,
                self.price,
            )
        )

        return details
