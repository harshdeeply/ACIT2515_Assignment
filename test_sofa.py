import unittest

import inspect
import os
from sofa import Sofa
from furniture_manager import FurnitureManager


class TestSofa(unittest.TestCase):
    """ Unit tests for Sofa class """

    def setUp(self):
        """ Generated the object """
        self.test_sofa = Sofa("001", "2019", "BrandX", 99.99, 139.99, 3, 5)

    def tearDown(self):
        """ Destroys the object """
        self.test_sofa = None
        self.log_point()

    def log_point(self):
        currentTest = self.id().split(".")[-1]
        callingFunction = inspect.stack()[1][3]
        print("in %s - %s()" % (currentTest, callingFunction))

    def test_sofa_valid_parameters(self):
        """ 010A - Valid constructor """

        self.assertIsNotNone(self.test_sofa, "Sofa must be defined")

    def test_sofa_invalid_parameters(self):
        """ 010B - Invalid constructor """

        # invalid data type for number of seats
        self.assertRaises(
            ValueError, Sofa, "001", "2019", "BrandX", 99.99, 139.99, "3", 5
        )

        # invalid data type for number of cushions
        self.assertRaises(
            ValueError, Sofa, "001", "2019", "BrandX", 99.99, 139.99, 3, "5"
        )

        # invalid value for number of seats
        self.assertRaises(
            ValueError, Sofa, "001", "2019", "BrandX", 99.99, 139.99, 0, "5"
        )

        # invalid value for number of cushions
        self.assertRaises(
            ValueError, Sofa, "001", "2019", "BrandX", 99.99, 139.99, "3", 0
        )
        self.assertRaises(
            ValueError, Sofa, "001", "2019", "BrandX", 99.99, 139.99, "", 5
        )
        self.assertRaises(
            ValueError, Sofa, "001", "2019", "BrandX", 99.99, 139.99, 3, ""
        )
        self.assertRaises(
            ValueError, Sofa, "001", "2019", "BrandX", 99.99, 139.99, None, 5
        )
        self.assertRaises(
            ValueError, Sofa, "001", "2019", "BrandX", 99.99, 139.99, 3, None
        )

    def test_get_number_of_seats_valid(self):
        """ 020A - Valid number of seats """

        self.assertEqual(self.test_sofa.number_of_seats, 3, "Number of seats must be 3")

    def test_get_number_of_cushions_valid(self):
        """ 030A - Valid number of cushions """

        self.assertEqual(
            self.test_sofa.number_of_cushions, 5, "Number of cushions must be 5"
        )

    def test_get_item_type_valid(self):
        """ 040A - Valid furniture type """

        self.assertEqual(
            self.test_sofa.get_item_type(), "sofa", "Item type must be 'sofa'"
        )

    def test_get_item_description(self):
        """ 050 A - Valid item description """

        self.assertEqual(
            self.test_sofa.get_item_description(),
            "sofa with serial number 001 manufactured by BrandX with 3 number of seats and 5 number of "
            "cushions is available for $139.99",
            "Output must match 'sofa 001 manufactured by BrandX with 3 number of seats and 5 "
            "number of cushions is available for $139.99'",
        )

    def test_to_dict_valid(self):
        """ 060 A - Valid to_dict test"""

        self.assertEqual(
            self.test_sofa.to_dict(),
            {
                "id": None,
                "type": "sofa",
                "item_serial_num": "001",
                "item_brand": "BrandX",
                "year_manufactured": "2019",
                "cost": 99.99,
                "price": 139.99,
                "is_sold": False,
                "number_of_seats": 3,
                "number_of_cushions": 5,
            },
        )


if __name__ == "__main__":
    unittest.main()

