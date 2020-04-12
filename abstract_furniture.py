import re

from sqlalchemy import Column, String, Integer, Float

from base import Base


class AbstractFurniture(Base):
    """ Abstract furniture class """

    __tablename__ = "furniture"

    id = Column(Integer, primary_key=True)
    item_serial_number = Column(String(100))
    year_manufactured = Column(String(4))
    item_brand = Column(String(20))
    cost = Column(Float)
    price = Column(Float)
    type = Column(String(4))
    is_sold = Column(Integer)

    ID_LABEL = "ID"
    SERIAL_NUM_LABEL = "Serial number"
    YEAR_MANUFACTURED_LABEL = "Year manufactured"
    ITEM_BRAND_LABEL = "Item brand name"
    COST_LABEL = "Cost"
    PRICE_LABEL = "Price"

    RE_YEAR = r"^\d{4}$"

    def __init__(self, serial_num, year_manufactured, item_brand, cost, price, type):
        """
        Constructor
        :param serial_num: Serial number of the furniture item
        :param year_manufactured: Year manufactured
        :param item_brand: Brand name of the brand that produced the item
        :param cost: Cost
        :param price: Price
        """

        # locally setting a reference to the class to make code easier to type and shorter
        af = AbstractFurniture

        af._validate_type(serial_num, af.SERIAL_NUM_LABEL, str)
        af._validate_type(year_manufactured, af.YEAR_MANUFACTURED_LABEL, str)

        if re.match(AbstractFurniture.RE_YEAR, year_manufactured) is None:
            raise ValueError("Year should be in the format YYYY")

        af._validate_type(item_brand, af.ITEM_BRAND_LABEL, str)
        af._validate_type(cost, af.COST_LABEL, float)
        af._validate_nonzero(cost, af.COST_LABEL)

        af._validate_type(price, af.PRICE_LABEL, float)
        af._validate_nonzero(price, af.PRICE_LABEL)

        self.item_serial_number = serial_num
        self.year_manufactured = year_manufactured
        self.item_brand = item_brand
        self.cost = cost
        self.price = price
        self.type = type

        self.id = None
        self.is_sold = False

    def get_item_description(self):
        """
        Returns a description of the item
        :return: Description (str)
        """
        raise NotImplementedError(
            "This method needs to be implemented by classes that inherit AbstractFurniture"
        )

    def to_dict(self):
        """
        Returns a JSON representation of the item
        :return: JSON dict (dict)
        """
        raise NotImplementedError(
            "This method needs to be implemented by classes that inherit AbstractFurniture"
        )

    def mark_sold(self):
        """
        Marks the item as sold
        """
        self.is_sold = True

    def calculate_profit(self):
        """
        Returns the profit that the store would make by selling the item
        :return: Profit (float)
        """
        return self.price - self.cost

    @staticmethod
    def _validate_type(item, name, datatype):
        """
        Static method to validate an input's data type as well as check if it's none
        :param item: Item to check
        :param name: Name to print in an error statement if needed
        :param datatype: Datatype to check for
        """
        if datatype == str:
            if item == "":
                raise ValueError(name + " is empty")

        if item is None:
            raise ValueError(name + " is of type None")

        if not isinstance(item, datatype):
            raise ValueError(name + " is not of type " + str(datatype))

    @staticmethod
    def _validate_nonzero(num, name):
        """
        Static method to check if a number is less than zero and raise and error if it is
        :param num: Number to check (float, int)
        :param name: Name to print in an error statement if needed
        """
        if float(num) < 0.0:
            raise ValueError(name + " is less than zero")
