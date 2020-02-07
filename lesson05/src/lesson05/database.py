import pymongo
import dns # required for connecting with SRV
import getpass
import csv
import logging
import os
import json


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

#p = getpass.getpass(prompt="Enter Pass: ", stream=None)
# #client = pymongo.MongoClient("mongodb+srv://kay:myRealPassword@cluster0.mongodb.net/test?w=majority")
# client = pymongo.MongoClient("mongodb+srv://uwvinh:uwtest2020@cluster0-ksxsk.mongodb.net/test?retryWrites=true&w=majority")
# db = client.test


def print_mdb_collection(collection_name):
    """Helper function to print docs in collection withinn Mongo Database"""
    for doc in collection_name.find():
        print(doc)


def load_csv_file(csv_file):
    """Loads the csv file items into a list """
    record_list = list()
    with open(csv_file, "r", encoding="utf8", newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            record_list.append(row)
    return record_list


def import_data(directory_name, product_file, customer_file, rental_file):
    """

    :param directory_name: name of directory with csv files
    :param product_file: csv file with product data
    :param customer_file: csv file with customer data
    :param rental_file: csv file with rental data
    :return: 2 tuples, one representing record count of number of products, customers, rentals
                       the other for the count of any errors that occured
    """
    # MAYBE can add each file to be a list, and iterate through and use this same for loop implemenation

    #product_data = load_csv_file(directory_name + "\\" + product_file)

    file_list = [product_file, customer_file, rental_file]

    #TODO incorporate file list to perform loop for every file
    #for file in file_list:
    record_data = load_csv_file(os.path.join(directory_name, product_file))
    logger.debug(record_data)

    # list of each record as a dictionary
    product_dict_list = list()

    # First line of the csv file is the "Schema"
    record_data_format = record_data[0]

    for record in record_data[1:]:
        # Current product dictionary to be added to the list
        curr_product_dict = dict()
        for i in range(len(record)):
            curr_product_dict[record_data_format[i]] = record[i]
        product_dict_list.append(curr_product_dict)

    logger.debug(product_dict_list)

    client = pymongo.MongoClient(
        "mongodb+srv://uwvinh:uwtest2020@cluster0-ksxsk.mongodb.net/test?retryWrites=true&w=majority")

    with client:
        db = client.data
        product_d = db["customer"]
        # for product_dict in product_dict_list:
        #     #db.insert_one(product_dict)
        result = product_d.insert_many(product_dict_list)
    return tuple()


def main():
    #csv_files_directory = os.path.dirname(os.getcwd()) + "\data"
    csv_files_directory = os.path.abspath("data")
    logger.debug(csv_files_directory)

    import_data(csv_files_directory, "product.csv", "customers.csv", "rental.csv")


if __name__ == "__main__":
    main()
