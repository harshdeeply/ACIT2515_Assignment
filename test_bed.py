import unittest

from bed import Bed

# from sofa import Sofa
from furniture_manager import FurnitureManager


class TestBed(unittest.TestCase):
    """ Unit tests for Bed class """

    def test_bed_valid_parameters(self):
        """ 010A - Valid constructor """

        test_bed = Bed("001", "2019", "BrandX", 99.99, 139.99, "180cm x 120cm", "100cm")
        self.assertIsNotNone(test_bed, "Bed must be defined")

    def test_bed_invalid_parameters(self):
        """ 010B - Invalid constructor """

        # invalid data type for size of bed
        self.assertRaises(
            ValueError, Bed, "001", "2019", "BrandX", 99.99, 139.99, 30, "100cm"
        )

        # invalid data type for height of bed
        self.assertRaises(
            ValueError,
            Bed,
            "001",
            "2019",
            "BrandX",
            99.99,
            139.99,
            "180cm x 120cm",
            100,
        )

        # invalid value for size of bed
        self.assertRaises(
            ValueError, Bed, "001", "2019", "BrandX", 99.99, 139.99, "", "50cm"
        )

        # invalid value for height of bed
        self.assertRaises(
            ValueError, Bed, "001", "2019", "BrandX", 99.99, 139.99, "180cm x 100cm", ""
        )

        # passing none to the value of size of bed
        self.assertRaises(
            ValueError, Bed, "001", "2019", "BrandX", 99.99, 139.99, None, "50cm"
        )

        # passing none to the value of height of bed
        self.assertRaises(
            ValueError,
            Bed,
            "001",
            "2019",
            "BrandX",
            99.99,
            139.99,
            "180cm x 120cm",
            None,
        )

    def test_get_size_valid(self):
        """ 020A - Valid size of bed """
        test_bed = Bed("001", "2019", "BrandX", 99.99, 139.99, "180cm x 120cm", "50cm")
        self.assertEqual(
            test_bed.size, "180cm x 120cm", "Size of bed must be '180cm x 120cm'"
        )

    def test_get_height_valid(self):
        """ 030A - Valid height of bed """
        test_bed = Bed("001", "2019", "BrandX", 99.99, 139.99, "180cm x 120cm", "50cm")
        self.assertEqual(test_bed.height, "50cm", "Height of bed must be 50cm")

    def test_get_item_type_valid(self):
        """ 040A - Valid furniture type """
        test_bed = Bed("001", "2019", "BrandX", 99.99, 139.99, "180cm x 120cm", "50cm")
        self.assertEqual(test_bed.get_item_type(), "bed", "Item type must be 'bed'")

    def test_get_item_description(self):
        """ 050A - Valid Item Description """
        test_bed = Bed("001", "2019", "BrandX", 99.99, 139.99, "180cm x 120cm", "50cm")
        self.assertEqual(
            test_bed.get_item_description(),
            "bed with serial number 001 manufactured by BrandX with 180cm x 120cm dimensions and 50cm height is available for $139.99",
            "Output must match 'bed with serial number 001 manufactured by BrandX with 180cm x 120cm dimensions and 50cm height is available for $139.99'",
        )

    def test_to_dict_valid(self):
        """ 060 A - Valid to_dict test"""
        test_bed = Bed("001", "2019", "BrandX", 99.99, 139.99, "180cm x 120cm", "50cm")
        self.assertEqual(
            test_bed.to_dict(),
            {
                "id": None,
                "type": "bed",
                "item_serial_num": "001",
                "item_brand": "BrandX",
                "year_manufactured": "2019",
                "cost": 99.99,
                "price": 139.99,
                "is_sold": False,
                "size": "180cm x 120cm",
                "height": "50cm",
            },
        )


if __name__ == "__main__":
    unittest.main()
