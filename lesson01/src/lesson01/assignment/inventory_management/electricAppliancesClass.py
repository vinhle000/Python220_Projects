# Electric appliances class
from src.lesson01.assignment.inventory_management.inventoryClass import Inventory


class ElectricAppliances(Inventory):

    def __init__(self, product_code, description, market_price,
                 rental_price, brand, voltage):
        Inventory.__init__(self, product_code, description,
                           market_price, rental_price)
        # Creates common instance variables from the parent class

        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        output_dict = dict()
        output_dict['productCode'] = self.productCode
        output_dict['description'] = self.description
        output_dict['marketPrice'] = self.marketPrice
        output_dict['rentalPrice'] = self.rentalPrice
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
