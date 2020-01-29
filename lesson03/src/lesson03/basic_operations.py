"""Performs Basic SQLite Database Operations"""

import logging
import os
from peewee import *


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


if os.path.isfile('customer.db'):
    os.remove('customer.db')
db = SqliteDatabase('customer.db')


class Customer(Model):
    """Model for a Customer in SQLite database"""
    customer_id = CharField()
    name = CharField()
    lastname = CharField()
    home_address = CharField()
    phone_number = CharField()
    email_address = CharField()
    status = CharField()
    credit_limit = CharField()

    class Meta:
        database = db


def create_tables(database):
    """Creates table, indexes and associated metadata for the given Customer model"""
    database.create_tables([Customer])


def add_customer(customer_id, name, lastname, home_address, phone_number,
                 email_address, status, credit_limit):
    """Add a new customer to the sqlite3 database. """
    new_customer = Customer.create(customer_id=customer_id, name=name,
                                   lastname=lastname, home_address=home_address,
                                   phone_number=phone_number, email_address=email_address,
                                   status=status, credit_limit=credit_limit)
    new_customer.save()


def search_customer(customer_id):
    """Returns a dictionary object with name, lastname, email address and phone number
        of a customer or an empty dictionary object if no customer was found. """
    customer_dict = dict()

    for customer in Customer.select().where(Customer.customer_id == customer_id):
        customer_dict["name"] = customer.name
        customer_dict["lastname"] = customer.lastname
        customer_dict["email_address"] = customer.email_address
        customer_dict["phone_number"] = customer.phone_number
        return customer_dict

    logger.info("Customer_ID was not found in database")
    return customer_dict


def delete_customer(customer_id):
    """Delete a customer from the sqlite3 database.
    """

    for customer in Customer.select().where(Customer.customer_id == customer_id):
        customer.delete_instance()
        logger.info(f"Customer:{customer_id} has been deleted")
        return True

    logger.info(f"Customer:{customer_id} does not exist in Database")
    return False

    # Another Method of deleting
    # query = Customer.delete().where(Customer.customer_id == customer_id)
    # query.execute()


def update_customer_credit(customer_id, credit_limit):
    """Search an existing customer by customer_id and update their credit limit
        or raise a ValueError exception if the customer does not exist.
    """

    customer_exists = False

    for customer in Customer.select().where(Customer.customer_id == customer_id):
        customer.credit_limit = credit_limit
        logger.info(f"Changed customer: {customer_id} credit to {customer.credit_limit}")
        customer.save()
        customer_exists = True

    if not customer_exists:
        raise ValueError("NoCustomer")


def list_active_customers():
    """Returns an integer with the number of customers whose status is currently active.
    """
    active_customer_count = 0
    for customer in Customer.select().where(Customer.status == "active"):
        active_customer_count += 1

    return active_customer_count


# Local Tesetin
# if __name__ == "__main__":
#     db.connect()
#     create_tables(db)
#
#     list_of_customers = [
#         ("598", "Name", "Lastname", "Address", "phone", "email", "active", 999),
#         ("597", "Name", "Lastname", "Address", "phone", "email", "inactive", 10),
#         ("596", "Name", "Lastname", "Address", "phone", "email", "inactive", 99),
#         ("595", "Name", "Lastname", "Address", "phone", "email", "active", 999),
#         ("594", "Name", "Lastname", "Address", "phone", "email", "active", 10),
#         ("593", "Name", "Lastname", "Address", "phone", "email", "active", 99)
#     ]
#
#     for customer in list_of_customers:
#         add_customer(customer[0],
#                      customer[1],
#                      customer[2],
#                      customer[3],
#                      customer[4],
#                      customer[5],
#                      customer[6],
#                      customer[7]
#                      )
#
#     customer_dict = search_customer("598")
#     logger.info(customer_dict)
#     update_customer_credit("598", 9000)
#     print(delete_customer("593"))
#
#     for customer in Customer:
#         logger.info(customer.customer_id)
#     logger.info(list_active_customers())
#     db.close()
