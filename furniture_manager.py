from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from abstract_furniture import AbstractFurniture
from bed import Bed
from furniture_stats import FurnitureStats
from sofa import Sofa


class FurnitureManager:
    """ Furniture manager class """

    def __init__(self, db_filename):
        """ Creates an instance of a furniture manager """

        if db_filename is None or db_filename == "":
            raise ValueError("DB name cannot be undefined")

        if not isinstance(db_filename, str):
            raise ValueError("DB name can only be a string.")

        engine = create_engine("sqlite:///" + db_filename)
        self._db_session = sessionmaker(bind=engine, expire_on_commit=False)

    def add(self, item):
        """
        Adds a new item to the directory
        :param item: item
        """

        if item is None or not isinstance(item, AbstractFurniture):
            raise ValueError("Invalid furniture.")

        # Verify no duplicated Serial Number
        if self._item_exists(item.item_serial_number):
            raise ValueError("Serial number already exists.")

        session = self._db_session()

        session.add(item)
        session.commit()

        session.close()
        return item.id

    def _item_exists(self, item_serial_number):
        """ Returns True if the serial number exists and False if it does not exist """
        if item_serial_number is None or not isinstance(item_serial_number, str):
            raise ValueError("Invalid Serial Number.")
        session = self._db_session()

        item = (
            session.query(AbstractFurniture)
            .filter(AbstractFurniture.item_serial_number == item_serial_number)
            .first()
        )

        session.close()

        if item is not None:
            return True

        return False

    def get(self, id):
        """
        Returns an item with the given ID
        :param item_id: ID
        :return: Item (AbstractFurniture)
        """

        if id is None or id == "":
            raise ValueError("ID cannot be undefined.")

        if not isinstance(id, int):
            raise ValueError("ID is not an integer.")

        session = self._db_session()
        item = (
            session.query(Sofa)
            .filter(AbstractFurniture.id == id)
            .filter(AbstractFurniture.type == Sofa.FURNITURE_TYPE)
            .first()
        )

        if item is None:
            item = (
                session.query(Bed)
                .filter(AbstractFurniture.id == id)
                .filter(AbstractFurniture.type == Bed.FURNITURE_TYPE)
                .first()
            )

        session.close()
        return item

    def get_all(self):
        """
        Returns the whole directory
        :return: List of AbstractFurniture items
        """
        session = self._db_session()

        furniture = session.query(Sofa).filter(Sofa.type == Sofa.FURNITURE_TYPE).all()
        furniture = (
            furniture + session.query(Bed).filter(Bed.type == Bed.FURNITURE_TYPE).all()
        )

        session.close()
        return furniture

    def get_all_by_type(self, type):
        """
        Returns a list of items with the given furniture type
        :param type: furniture type
        :return: List of AbstractFurniture items
        """

        if type is None or type == "":
            raise ValueError("Furniture type cannot be undefined.")
        if not isinstance(type, str):
            raise ValueError("Furniture type can only be a string.")

        session = self._db_session()

        if type == Sofa.FURNITURE_TYPE:
            items = session.query(Sofa).filter(Sofa.type == Sofa.FURNITURE_TYPE).all()

        elif type == Bed.FURNITURE_TYPE:
            items = session.query(Bed).filter(Bed.type == Bed.FURNITURE_TYPE).all()

        else:
            items = []
            raise ValueError("Invalid furniture type.")

        session.close()
        return items

    # --------------------------------------------------------------------------------------------------------

    def update(self, item):
        """
        Replaces an item with the same id as the id of the given item
        :param item: item to replace the existing item with
        """
        if item is None:
            return

        session = self._db_session()
        legacy_item = None

        if item.type == Sofa.FURNITURE_TYPE:
            legacy_item = session.query(Sofa).filter(Sofa.id == item.id)

        elif item.type == Bed.FURNITURE_TYPE:
            legacy_item = session.query(Bed).filter(Bed.id == item.id)

        if legacy_item:
            # item_dict["item_serial_number"] = item.pop("item_serial_num")
            item_dict = item.to_dict()
            item_dict["item_serial_number"] = item_dict.pop("item_serial_num")
            legacy_item.update(item_dict)

        session.commit()
        session.close()

    # --------------------------------------------------------------------------------------------------------

    def delete(self, id):
        """
        Removes an item with the given ID
        :param item_id: ID
        """
        if id is None or not isinstance(id, int):
            raise ValueError("Invalid ID.")

        session = self._db_session()
        item = (
            session.query(AbstractFurniture).filter(AbstractFurniture.id == id).first()
        )

        if item is None:
            session.close()
            raise ValueError("Item Serial Number does not exist.")

        session.delete(item)
        session.commit()

        session.close()

    def get_furniture_stats(self):
        """
        Returns information (stats) about the directory
        :return: FurnitureStats Object
        """
        n_total_items = (
            n_sold_items
        ) = n_sold_sofas = n_sold_beds = n_unsold_sofas = n_unsold_beds = 0
        profit = 0.0

        session = self._db_session()
        all_items = session.query(AbstractFurniture).all()

        for i in all_items:
            if i.type == Bed.FURNITURE_TYPE:
                if i.is_sold:
                    n_sold_beds += 1
                else:
                    n_unsold_beds += 1

            if i.type == Sofa.FURNITURE_TYPE:
                if i.is_sold:
                    n_sold_sofas += 1
                else:
                    n_unsold_sofas += 1

            if i.is_sold:
                profit += i.calculate_profit()
                n_sold_items += 1

            n_total_items += 1

        session.close()

        return FurnitureStats(
            n_total_items,
            n_sold_items,
            n_sold_sofas,
            n_unsold_sofas,
            n_sold_beds,
            n_unsold_beds,
            profit,
        )

    def get_items_by_brand_name(self, item_brand):
        """
        Returns a list of items that have been manufactured by the given brand
        :param brand_name: Brand name to select items by
        :return: List of AbstractFurniture items
        """
        if item_brand is None or item_brand == "":
            raise ValueError("Item Brand cannot be undefined.")
        if not isinstance(item_brand, str):
            raise ValueError("Brand name must be a string.")

        session = self._db_session()
        item = (
            session.query(AbstractFurniture)
            .filter(AbstractFurniture.item_brand == item_brand)
            .first()
        )

        session.close()
        if item != "":
            return item

        else:
            return "No item(s) found with the specified brand name."

    @staticmethod
    def _validate_type(item, name, datatype):
        """
        Static method to validate an input's data type as well as check if it's none
        :param item: Item to check
        :param name: Name to print in an error statement if needed
        :param datatype: Datatype to check for
        """
        if item is None:
            raise ValueError(name + " is of type None")

        if not isinstance(item, datatype):
            raise ValueError(name + " is not of the required type")

    @staticmethod
    def _validate_nonzero(num, name):
        """
        Static method to check if a number is less than zero and raise and error if it is
        :param num: Number to check (float, int)
        :param name: Name to print in an error statement if needed
        """
        if float(num) < 0.0:
            raise ValueError(name + " is less than zero")
