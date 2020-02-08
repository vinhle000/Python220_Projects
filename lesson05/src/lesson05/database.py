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

    # Had to include encoding, was loading extra symbols due to csv file format
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

    #product_data = load_csv_file(directory_name + "\\" + product_file)
    client = pymongo.MongoClient(
        "mongodb+srv://uwvinh:uwtest2020@cluster0-ksxsk.mongodb.net/test?retryWrites=true&w=majority")

    # Lists for tracking record and error counts
    record_count_list = list()
    error_count_list = list()

    file_list = [product_file, customer_file, rental_file]

    for file in file_list:
        csv_records = load_csv_file(os.path.join(directory_name, file))
        logger.debug(csv_records)

        # list of each record as a dictionary
        record_dict_list = list()

        # First line of the csv file is the "Schema" model for data structure
        record_data_format = csv_records[0]

        # Creates a dict for every record in csv and appends to a list
        for record in csv_records[1:]:
            curr_product_dict = dict()
            for i in range(len(record)):
                curr_product_dict[record_data_format[i]] = record[i]
            record_dict_list.append(curr_product_dict)

        logger.debug(record_dict_list)

        with client:
            db = client.data

            # file name is used database name
            file_name = file.split(".")[0]
            logger.debug(file_name)
            record_db = db[file_name]

            record_count = 0
            error_count = 0

            # Adds dictionary items to the database
            for record_dict in record_dict_list:
                #logger.debug(record_dict)
                try:
                    record_db.insert_one(record_dict)
                    record_count += 1
                except Exception as e:
                    logger.error(e.__traceback__)
                    error_count += 1

            record_count_list.append(record_count)
            error_count_list.append(error_count)

            # OTHER METHOD
            # Could use to insert many all dict records to mongodb,
            # But wanted to check for errors every time a record is inserted
            # result = product_d.insert_many(product_dict_list)

    return tuple(record_count_list), tuple(error_count_list)


def show_available_products():
    """Returns a Python dictionary of products listed as available """
    client = pymongo.MongoClient(
        "mongodb+srv://uwvinh:uwtest2020@cluster0-ksxsk.mongodb.net/test?retryWrites=true&w=majority")

    #Dict format {product_id : {description: val, product_type:val, quantity:val}


    with client:
        db = client["data"]
        collection = db["product"]

        results = collection.find()

        product_dict = dict()
        for result in results:
            product_id_dict = dict()

            product_id_dict['description'] = result['description']
            product_id_dict['quantity_available'] = result['quantity_available']

            product_id = result['\ufeffproduct_id']
            product_dict[product_id] = product_id_dict

            #print(result)

    return product_dict

    #TODO get user ID info from rentals
def show_rentals(product_id):
    """ Returns a Python dictionary with the user information from users that have rented products matching product_id"""

    client = pymongo.MongoClient(
        "mongodb+srv://uwvinh:uwtest2020@cluster0-ksxsk.mongodb.net/test?retryWrites=true&w=majority")

    with client:
        db = client["data"]
        rental_collection = db["rental"]
        customer_collection = db["customers"]

        current_rentals = rental_collection.find({'\ufeffproduct_id': product_id})

        for rental in current_rentals:
            print(rental)

        # for rental in rental_collection.find():
        #     print(rental)

        # for customer in customer_collection.find():
        #         #     print(customer)



def main():
    #csv_files_directory = os.path.dirname(os.getcwd()) + "\data"
    csv_files_directory = os.path.abspath("data")
    logger.debug(csv_files_directory)

    #print(import_data(csv_files_directory, "product.csv", "customers.csv", "rental.csv"))

    #print(show_available_products())
    print(show_rentals('prd002'))

if __name__ == "__main__":
    main()
