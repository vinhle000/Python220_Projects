"""
grade lesson 5
"""

import os
import pytest

from lesson05 import database as l

@pytest.fixture
def _show_available_products():
    return {'prd001': {'description': '60-inch TV stand', 'quantity_available': '3'},
            'prd002': {'description': 'L-shaped sofa', 'quantity_available': '0'},
            'prd003': {'description': 'Acacia kitchen table', 'quantity_available': '7'},
            'prd004': {'description': 'Queen bed', 'quantity_available': '10'},
            'prd005': {'description': 'Reading lamp', 'quantity_available': '20'},
            'prd006': {'description': 'Portable heater', 'quantity_available': '14'},
            'prd007': {'description': 'Ballerina painting', 'quantity_available': '0'},
            'prd008': {'description': 'Smart microwave', 'quantity_available': '30'},
            'prd009': {'description': 'Popcorn machine', 'quantity_available': '0'},
            'prd010': {'description': '60-inch TV', 'quantity_available': '3'}}



@pytest.fixture
def _show_rentals():
    return {'user008': {'name': 'Shirlene Harris', 'address': '4329 Honeysuckle Lane',
                        'zip_code': '98055', 'phone_number': '206-279-5340',
                        'email': 'harrisfamily@gmail.com'},
            'user005': {'name': 'Dan Sounders', 'address': '861 Honeysuckle Lane',
                        'zip_code': '98244', 'phone_number': '206-279-1723',
                        'email': 'soundersoccer@mls.com'}}


def test_import_data():
    """ import """
    data_dir = os.path.dirname(os.path.abspath(__file__))
    added, errors = l.import_data(data_dir, "product.csv", "customers.csv", "rental.csv")

    for add in added:
        assert isinstance(add, int)

    for error in errors:
        assert isinstance(error, int)

    assert added == (10, 10, 9)
    assert errors == (0, 0, 0)


def test_show_available_products(_show_available_products):
    """ available products """
    students_response = l.show_available_products()
    assert students_response == _show_available_products


def test_show_rentals(_show_rentals):
    """ rentals """
    students_response = l.show_rentals("prd002")
    assert students_response == _show_rentals

if __name__ == "__main__":
    pytest.main([__file__])