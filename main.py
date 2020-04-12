from bed import Bed
from furniture_manager import FurnitureManager
from sofa import Sofa

qwerty = FurnitureManager("furniture.sqlite")
beds = {
    "Bed1": ["001", "2019", "Ikea", 24.99, 44.99, "190x100cm", "25cm"],
    "Bed2": ["002", "2015", "HelloFurniture", 124.99, 144.99, "190x100cm", "25cm"],
}

sofas = {"Sofa1": ["003", "2012", "HelloFurniture", 99.99, 119.99, 4, 6]}
Bed1 = Bed(
    beds["Bed1"][0],
    beds["Bed1"][1],
    beds["Bed1"][2],
    beds["Bed1"][3],
    beds["Bed1"][4],
    beds["Bed1"][5],
    beds["Bed1"][6],
)
Bed2 = Bed(
    beds["Bed2"][0],
    beds["Bed2"][1],
    beds["Bed2"][2],
    beds["Bed2"][3],
    beds["Bed2"][4],
    beds["Bed2"][5],
    beds["Bed2"][6],
)
Sofa1 = Sofa(
    sofas["Sofa1"][0],
    sofas["Sofa1"][1],
    sofas["Sofa1"][2],
    sofas["Sofa1"][3],
    sofas["Sofa1"][4],
    sofas["Sofa1"][5],
    sofas["Sofa1"][6],
)
# qwerty.add(Bed1)
# qwerty.add(Bed2)
# qwerty.add(Sofa1)
# print(qwerty.get(1))
# print(qwerty.get(2))
# print(qwerty.get(3))

# print('\nGetting fucking everything!')
# print(qwerty.get_all())
# print('\n')
# # qwerty.delete(2)
# # print('\nGetting all again!')
# # print(qwerty.get_all())
# print('Getting items by brand name:\n', qwerty.get_items_by_brand_name('HelloFurniture'))
# print('\nFurniture Stats:\n', qwerty.get_furniture_stats())

print(qwerty.get_all())
