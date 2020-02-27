"""Inventory management, with use of closures and currying """
from functools import partial
import csv
import os


def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """Adds furniture item to csv file"""
    item_info = [customer_name, item_code, item_description, item_monthly_price]
    with open(invoice_file, "a+", newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(item_info)



def single_customer(customer_name, invoice_file):

    rented_items_list = []
    def add_customers_furniture(rented_items):
        with open(rented_items, 'r') as rented_items_file:
            reader = csv.reader(rented_items_file)
            for row in reader:
                rented_items_list.append(row)

        item_info = partial(add_furniture, invoice_file=invoice_file, customer_name=customer_name)
        for item in rented_items_list:
            item_info(item_code=item[0], item_description=item[1], item_monthly_price=item[2])

    return add_customers_furniture


def generate_csv_file(file_name, record_amount):
    """generates_csv_file with psuedo ranom values"""



def delete_file(file):
    """deletes file if it exists"""
    if os.path.isfile(file):
        os.remove(file)

if __name__ == "__main__":
    add_furniture("rented_items.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
    add_furniture("rented_items.csv", "Edward Data", "KT78", "Kitchen Table", 10)
    add_furniture("rented_items.csv", "Alex Gonzales", "BR02", "Queen Mattress", 17)
    create_invoice = single_customer("Susan Wong", "rented_items.csv")
    create_invoice("test_items.csv")
    #delete_file("rented_items.csv")