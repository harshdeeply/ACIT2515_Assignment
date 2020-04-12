import unittest
import os
import inspect
from bed import Bed
from sqlalchemy import create_engine
from base import Base
from furniture_manager import FurnitureManager
from furniture_stats import FurnitureStats
from sofa import Sofa


class TestFurnitureManager(unittest.TestCase):
    def setUp(self):
        """
        setUp method for testing methods of the FurnitureManager class
        """
        engine = create_engine("sqlite:///test_furniture.sqlite")

        # Creates all the tables
        Base.metadata.create_all(engine)
        Base.metadata.bind = engine

        self.manager = FurnitureManager("test_furniture.sqlite")
        self.beds = {
            "Bed1": ["001", "2019", "Ikea", 24.99, 44.99, "190x100cm", "25cm"],
            "Bed2": [
                "002",
                "2015",
                "HelloFurniture",
                124.99,
                144.99,
                "190x100cm",
                "25cm",
            ],
        }

        self.sofas = {"Sofa1": ["003", "2012", "HelloFurniture", 99.99, 119.99, 4, 6]}
        self.Bed1 = Bed(
            self.beds["Bed1"][0],
            self.beds["Bed1"][1],
            self.beds["Bed1"][2],
            self.beds["Bed1"][3],
            self.beds["Bed1"][4],
            self.beds["Bed1"][5],
            self.beds["Bed1"][6],
        )
        self.Bed2 = Bed(
            self.beds["Bed2"][0],
            self.beds["Bed2"][1],
            self.beds["Bed2"][2],
            self.beds["Bed2"][3],
            self.beds["Bed2"][4],
            self.beds["Bed2"][5],
            self.beds["Bed2"][6],
        )
        self.Sofa1 = Sofa(
            self.sofas["Sofa1"][0],
            self.sofas["Sofa1"][1],
            self.sofas["Sofa1"][2],
            self.sofas["Sofa1"][3],
            self.sofas["Sofa1"][4],
            self.sofas["Sofa1"][5],
            self.sofas["Sofa1"][6],
        )

    def tearDown(self):
        """ Destroys test data """
        os.remove("test_furniture.sqlite")
        self.log_point()

    def log_point(self):
        currentTest = self.id().split(".")[-1]
        callingFunction = inspect.stack()[1][3]
        print("in %s - %s()" % (currentTest, callingFunction))

    def test_add_item_success(self):
        """
        020A - Tests whether add() adds a new item correctly
        """
        self.manager.add(self.Bed1)
        self.assertTrue(self.manager.get(self.Bed1.id))

        self.manager.add(self.Sofa1)
        self.assertTrue(self.manager.get(self.Sofa1.id))

    def test_add_failure(self):
        """
        020B - Tests whether add() raises a ValueError for bad/none values
        """
        # None for item
        self.assertRaisesRegex(ValueError, "Invalid furniture.", self.manager.add, None)
        self.assertRaisesRegex(
            ValueError, "Invalid furniture.", self.manager.add, "String object"
        )

        # Try to add an item with the same serial number twice
        self.manager.add(self.Bed1)
        self.assertRaisesRegex(
            ValueError, "Serial number already exists.", self.manager.add, self.Bed1
        )

    def test_get_success(self):
        """
        030A - Tests whether get() gets the correct item
        """
        self.manager.add(self.Bed1)
        self.assertIsNotNone(self.manager.get(self.Bed1.id))
        self.manager.add(self.Sofa1)
        self.assertIsNotNone(self.manager.get(self.Sofa1.id))
        self.assertIsNone(self.manager.get(750))

    def test_get_failure(self):
        """
        030B - Tests whether get() raises a ValueError for bad/none values
        """
        # None as id
        self.assertRaisesRegex(
            ValueError, "ID cannot be undefined.", self.manager.get, None
        )
        # Empty string as ID
        self.assertRaisesRegex(
            ValueError, "ID cannot be undefined", self.manager.get, "",
        )

        # String as ID
        self.assertRaisesRegex(
            ValueError, "ID is not an integer.", self.manager.get, "Random String."
        )

    def test_get_all_success(self):
        """
        040A - Tests whether get_all() returns the correct number of items
        """
        self.manager.add(self.Bed1)
        self.manager.add(self.Bed2)
        self.manager.add(self.Sofa1)
        self.assertTrue(self.manager.get_all())

    def test_get_all_failure(self):
        """
        040A - Tests whether get_all() fails
        """
        # Testing get_all() to return None without adding any item
        self.assertFalse(self.manager.get_all())

    def test_get_all_by_type_success(self):
        """
        050A - Tests whether get_all_by_type() returns the correct number of items
        """
        self.manager.add(self.Bed1)
        self.manager.add(self.Bed2)
        self.manager.add(self.Sofa1)

        self.assertTrue(self.manager.get_all_by_type(Sofa.FURNITURE_TYPE))
        self.assertTrue(self.manager.get_all_by_type(Bed.FURNITURE_TYPE))

    def test_get_all_by_type_failure(self):
        """
        050B - Tests whether get_all_by_type() raises the correct errors for None/Bad values
        """
        # None as type
        self.assertRaisesRegex(
            ValueError,
            "Furniture type cannot be undefined.",
            self.manager.get_all_by_type,
            None,
        )

        # Empty string as type
        self.assertRaisesRegex(
            ValueError,
            "Furniture type cannot be undefined.",
            self.manager.get_all_by_type,
            "",
        )

        # Bad Value
        self.assertRaisesRegex(
            ValueError,
            "Furniture type can only be a string.",
            self.manager.get_all_by_type,
            1,
        )

    def test_update_success(self):
        """
        060A - Tests whether update() correctly updates an item
        """
        self.manager.add(self.Bed1)
        self.Bed1.item_brand = "foo"  # change brand name for bed

        # perform update
        self.manager.update(self.Bed1)

        self.assertEqual("foo", self.manager.get(self.Bed1.id).item_brand)

    def test_delete_success(self):
        """
        070A - Tests whether deletes() deletes the correct item
        """
        self.manager.add(self.Bed1)
        self.assertTrue(self.manager.get(self.Bed1.id))
        self.manager.delete(self.Bed1.id)
        self.assertFalse(self.manager.get(self.Bed1.id))

        self.manager.add(self.Sofa1)
        self.assertTrue(self.manager.get(self.Sofa1.id))
        self.manager.delete(self.Sofa1.id)
        self.assertFalse(self.manager.get(self.Sofa1.id))

    def test_delete_failure(self):
        """
        070B - Tests invalid delete() calls
        """
        self.assertRaisesRegex(ValueError, "Invalid ID.", self.manager.delete, None)
        self.assertRaisesRegex(ValueError, "Invalid ID.", self.manager.delete, "String")

    def test_get_furniture_stats_success(self):
        """
        080A - Tests whether get_furniture_stats() returns the correct object type
        """
        stats1 = self.manager.get_furniture_stats()
        self.assertEqual(0, stats1.get_num_items_sold())
        self.assertEqual(0, stats1.get_num_total_items())
        self.assertEqual(0, stats1.get_num_sold_beds())
        self.assertEqual(0, stats1.get_num_unsold_beds())
        self.assertEqual(0, stats1.get_num_sold_sofas())
        self.assertEqual(0, stats1.get_num_unsold_sofas())
        self.assertEqual(0.0, stats1.get_total_profit())

    def test_get_items_by_brand_name_success(self):
        """
        090A - Tests whether get_items_by_brand_name() returns the correct items
        """
        self.manager.add(self.Sofa1)
        self.manager.add(self.Bed2)

        self.assertTrue(self.manager.get_items_by_brand_name(self.Sofa1.item_brand))

    def test_get_items_by_brand_name_failure(self):
        """
        090B - Tests whether get_items_by_brand_name() raises the right errors for bad/none values
        """
        # None as brand name
        self.assertRaisesRegex(
            ValueError,
            "Item Brand cannot be undefined.",
            self.manager.get_items_by_brand_name,
            None,
        )

        # Bad value as brand name
        self.assertRaisesRegex(
            ValueError,
            "Brand name must be a string.",
            self.manager.get_items_by_brand_name,
            100,
        )


if __name__ == "__main__":
    unittest.main()
