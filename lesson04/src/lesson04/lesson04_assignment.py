"""Lesson04 Assignment - Utilize iteration to process data files"""
import csv
import random
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

product_names = ("dining chair", "dining table", "bed",
                 "dining set", "stool", "couch", "occasional table", "recliner")


def get_random_product_name():
    """Returns a random product name from the tuple"""
    return random.choice(product_names)


def get_random_qauntity_rented():
    """quantity_rented is a random integer between 1 and 4"""
    return random.randrange(1, 5)


def get_random_unit_rental_price_monthly():
    """unit_rental_price_monthly is a random float between 1.50 and 25.00"""
    return random.uniform(1.50, 25.00)


def get_random_rental_period_months():
    """rental_period_months is an integer between 6 and 60"""
    return random.randrange(6, 61)


def create_record(customer_id):
    """Creates a record with customer ID """
    new_record_tuple = (get_random_product_name(), customer_id, get_random_qauntity_rented(),
                        get_random_unit_rental_price_monthly(), get_random_rental_period_months())

    return new_record_tuple


def generate_records(num_of_records):
    """Generates a list of records"""
    records_list = list(map(create_record, (x+1 for x in range(num_of_records))))
    return records_list


def import_to_csv(my_data):
    """Imports record items into a csv file"""
    my_file = open('my_file.csv', 'w', newline='')
    with my_file:
        writer = csv.writer(my_file)
        writer.writerows(my_data)
    logger.info("Writing CSV File complete")


def load_csv(csv_file):
    """Loads the csv file items into a list"""
    record_list = list()
    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            record_list.append(row)

    logger.info("CSV file Loaded into list")
    return record_list


def total_monthly_payments(record):
    """Total Monthly Payments received"""
    return int(record[2]) * float(record[3]) * int(record[4])


def top_products_by_total_monthly_payments(record_list):
    """Top 10 products by Total Monthly Payments received
        Total Monthly Payments received  = quantity_rented * unit_rental_price * rental_period
    """

    sorted_record_list = sorted(record_list, key=lambda x: total_monthly_payments(x), reverse=True)

    # This can be returned as a generator
    top_10_products = [record[0] for record in sorted_record_list[:10]]
    logging.debug("Top 10 Products: {}".format(top_10_products))
    logging.debug([(record[0], total_monthly_payments(record))
                   for record in sorted_record_list[:10]])
    return top_10_products


def top_customers_by_quantity_of_products_rented(record_list):
    """Provides a list of top 5 Customers based on the quantity of products rented
    """

    sorted_record_list = sorted(record_list, key=lambda x: int(x[2]), reverse=True)

    # This can be returned as a generator
    top_5_customers = [record[1] for record in sorted_record_list[:5]]
    logger.debug("Top 5 customers:{}".format(top_5_customers))
    return top_5_customers


def top_customers_for_every_product(record_list):
    """Provides top 10 customers for every product based on total monthly payments received """
    # maybe use dictionray?
    # Each key is a product, and value is the top 10 based on the total monthly payments

    top_customers_dict = dict()

    for product in product_names:

        # Filter out records by current product
        product_records_list = list(filter(lambda x: x[0] == product, record_list))

        # Sort list by monthly payments, descending order
        sorted_product_records = sorted(product_records_list,
                                        key=lambda x: total_monthly_payments(x),
                                        reverse=True)
        # Takes the beginning 10 records from the sorted list and stores
        # it in the dictionary according to the product
        top_customers_dict[product] = [record[1] for record in sorted_product_records[:10]]

    return top_customers_dict


def lowest_paying_customers(record_list):
    """Provides the 20 customers who made the lowest total monthly payments."""

    sorted_record_list = sorted(record_list, key=lambda x: total_monthly_payments(x))

    lowest_payers = [record[1] for record in sorted_record_list[:20]]

    logging.debug("20 Customers with lowest total monthly payments: {}".format(lowest_payers))
    return lowest_payers

# if __name__ == "__main__":
#     # print(generate_records())
#     import_to_csv(generate_records(1000))
#     top_products_by_total_monthly_payments(load_csv('my_file.csv'))
#     top_customers_by_quantity_of_products_rented(load_csv('my_file.csv'))
#     logger.debug(top_customers_for_every_product(load_csv('my_file.csv')))
#     lowest_paying_customers(load_csv('my_file.csv'))
