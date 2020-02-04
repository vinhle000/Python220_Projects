
from lesson04 import lesson04_assignment as l

import pytest
import os

test_records = [("dining chair", "1", "1", "1.0", "1" ),
                 ("dining table", "2", "2", "2.0", "2"),
                 ("bed", "3", "3", "3.0", "3"),
                 ("dining set", "4", "4", "4.0", "4"),
                 ("stool", "5", "5", "5.0", "5"),
                 ("couch", "6", "6", "6.0", "6"),
                 ("occasional table", "7", "7", "7.0", "7"),
                 ("recliner", "8", "8", "8.0", "8"),
                 ("dining chair", "9", "1", "1.0", "1"),
                 ("dining table", "10", "2", "2.0", "2"),
                 ("bed", "11", "3", "3.0", "3"),
                 ("dining set", "12", "4", "4.0", "4"),
                 ("stool", "13", "5", "5.0", "5"),
                 ("couch", "14", "6", "6.0", "6"),
                 ("occasional table", "15", "7", "7.0", "7"),
                 ("recliner", "16", "8", "8.0", "8"),
                 ("dining chair", "17", "1", "1.0", "1"),
                 ("dining table", "18", "2", "2.0", "2"),
                 ("bed", "19", "3", "3.0", "3"),
                 ("dining set", "20", "4", "4.0", "4"),
                 ("stool", "21", "5", "5.0", "5"),
                 ("couch", "22", "6", "6.0", "6"),
                 ("occasional table", "23", "7", "7.0", "7"),
                 ("recliner", "24", "8", "8.0", "8")
                 ]


def test_csv_file_created():
    l.import_to_csv(l.generate_records(1000))
    assert os.path.exists("my_file.csv")

    #Test 1000 records generated
    record_list = l.load_csv("my_file.csv")
    assert len(record_list) == 1000


def test_load_csv_format():
    l.import_to_csv(test_records)
    record_list = l.load_csv("my_file.csv")
    assert record_list[0] == ['dining chair', '1', '1', '1.0', '1']
    assert record_list[23] == ['recliner', '24', '8', '8.0', '8']


def test_top_products_by_total_monthly_payments():
    top_products = l.top_products_by_total_monthly_payments(test_records)
    result = ['recliner', 'recliner', 'recliner', 'occasional table', 'occasional table',
                   'occasional table', 'couch', 'couch', 'couch', 'stool']
    assert top_products == result


def test_top_customers_by_quantity_of_products_rented():
    top_customers = l.top_customers_by_quantity_of_products_rented(test_records)
    result = ['8', '16', '24', '7', '15']
    assert top_customers == result

# Only covers 3 customers for a product
def test_top_customers_for_every_product():
    top_customers = l.top_customers_for_every_product(test_records)
    result = {'dining chair': ['1', '9', '17'],
              'dining table': ['2', '10', '18'],
              'bed': ['3', '11', '19'],
              'dining set': ['4', '12', '20'],
              'stool': ['5', '13', '21'],
              'couch': ['6', '14', '22'],
              'occasional table': ['7', '15', '23'],
              'recliner': ['8', '16', '24']}
    assert top_customers == result


def test_lowest_paying_customers():
    lowest_paying = l.lowest_paying_customers(test_records)
    result = ['1', '9', '17', '2', '10', '18', '3', '11', '19', '4', '12',
              '20', '5', '13', '21', '6', '14', '22', '7', '15']
    assert lowest_paying == result