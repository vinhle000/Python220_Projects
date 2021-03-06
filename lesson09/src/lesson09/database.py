"""MongoDB handling"""
import csv
import logging
import os
import pymongo


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class MongoDBConnection():
    """MongoDB Connection class for context management"""
    def __init__(self, host="mongodb+srv://uwvinh:uwtest2020@cluster0-ksxsk"
                            ".mongodb.net/test?retryWrites=true&w=majority"):
        self.host = host
        self.connection = None

    def __enter__(self):
        self.connection = pymongo.MongoClient(host=self.host)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def print_mdb_collection(collection_name):
    """Helper function to print docs in collection within Mongo Database"""
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

    # TODO: REMOVE if using custom context manager
    # client = pymongo.MongoClient(
    #     "mongodb+srv://uwvinh:uwtest2020@cluster0-ksxsk"
    #     ".mongodb.net/test?retryWrites=true&w=majority")



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

        client = MongoDBConnection()
        logger.info(f"Connected to: {client.connection}")

        with client:
            db = client.connection.data

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

    # TODO: REMOVE if using custom context manager
    # client = pymongo.MongoClient(
    #     "mongodb+srv://uwvinh:uwtest2020@cluster0-ksxsk"
    #     ".mongodb.net/test?retryWrites=true&w=majority")
    client = MongoDBConnection()

    with client:
        db = client.connection["data"]
        collection = db["product"]

        results = collection.find()

        product_dict = dict()
        for result in results:
            product_id_dict = dict()
            logger.debug(result)
            product_id_dict['description'] = result['description']
            product_id_dict['quantity_available'] = result['quantity_available']

            product_id = result['\ufeffproduct_id']
            product_dict[product_id] = product_id_dict

    return product_dict


def show_rentals(product_id):
    """ Returns a Python dictionary with the user
    information from users that have rented products matching product_id"""

    # TODO: REMOVE if using custom context manager
    # client = pymongo.MongoClient(
    #     "mongodb+srv://uwvinh:uwtest2020@cluster0-ksxsk"
    #     ".mongodb.net/test?retryWrites=true&w=majority")
    client = MongoDBConnection()

    with client:
        db = client.connection["data"]
        rental_collection = db["rental"]
        customer_collection = db["customers"]

        # Retrieve userIDs of customers that rented the product
        current_rentals = rental_collection.find({'\ufeffproduct_id': product_id})
        rental_customers = [rental['user_id'] for rental in current_rentals]
        logger.debug(rental_customers)

        # Retrieve info of customers that rented product with userID
        rental_customer_dict = dict()
        for customer in rental_customers:
            customer_info = dict()
            for curr_customer in customer_collection.find({'\ufeffuser_id': customer}):
                customer_info['name'] = curr_customer['name']
                customer_info['address'] = curr_customer['address']
                customer_info['zip_code'] = curr_customer['zip_code']
                customer_info['phone_number'] = curr_customer['phone_number']
                customer_info['email'] = curr_customer['email']
                rental_customer_dict[customer] = customer_info

        return rental_customer_dict

def delete_db():
    """Deletes current database collections"""

    # TODO: REMOVE if using custom context manager
    # client = pymongo.MongoClient(
    #     "mongodb+srv://uwvinh:uwtest2020@cluster0-ksxsk"
    #     ".mongodb.net/test?retryWrites=true&w=majority")

    client = MongoDBConnection()

    with client:
        db = client.connection["data"]
        customers_collection = db['customers']
        products_collection = db['product']
        rental_collection = db['rental']

        customers_collection.drop()
        products_collection.drop()
        rental_collection.drop()


def main():
    csv_files_directory = os.path.abspath("data")
    logger.debug(csv_files_directory)
    print(import_data(csv_files_directory, "product.csv", "customers.csv", "rental.csv"))
    print(show_available_products())
    print(show_rentals('prd002'))
    delete_db()


if __name__ == "__main__":
    main()
