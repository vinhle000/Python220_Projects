'''
Returns total price paid for individual rentals 
'''
# pylint: disable=C0321
import argparse
import json
import datetime
import math
import pysnooper
from loguru import logger
import sys

log_format = "{time} {file}:{line:3d} {level} {message}"
log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'

#logger.remove() #Removes Default Handler
#logger.add(sys.stderr, format=log_format, level="WARNING")

logger.add(log_file, format=log_format, level="INFO")


#@pysnooper.snoop()
def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)

    return parser.parse_args()


def load_rentals_file(filename):
    logger.debug("In load_rentals_file")
    with open(filename) as file:
        logger.debug("Opened file")
        try:
            data = json.load(file) # extra comma in line 5884 of json file, removed comma for so data can be loaded
            logger.debug("json file is loaded, and variable not assigned")
        except json.decoder.JSONDecodeError:

            logger.error("Expecting property name enclosed in double quotes")
            logger.warning("json file was not loaded")
            #exit(0)
    try:
        return data
    except UnboundLocalError:
        logger.error("local variable 'data' referenced before assignment")

#@pysnooper.snoop()
def calculate_additional_fields(data):
    """ Returns total price paid for individual rentals

    :param data: Loaded json data
    :return: Calculated data dictionary
    """

    try:
        for value in data.values():
            try:
                rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
                rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')


                value['total_days'] = abs((rental_end - rental_start).days) # This procuded a negative value, difference needs to be changed to an absolute value


                value['total_price'] = value['total_days'] * value['price_per_day']
                # logger.debug("total_days = {}".format(value['total_days']))
                # logger.debug("price_per_day = {}".format(value['price_per_day']))
                # logger.debug("total_price = {}".format(value['total_price']))
                # logger.debug("units_rented = {}".format(value['units_rented']))
                value['sqrt_total_price'] = math.sqrt(value['total_price']) #Throws ValueError, due to total_price bing a negative number
                value['unit_cost'] = value['total_price'] / value['units_rented'] #there is data in the json that includes 'units_rented' = 0
            except ValueError:
                logger.warning('"sqrt_total_price" was not able to be attained, total_days was a negative value')
                #(0)
            except ZeroDivisionError:
                logger.error('division by zero, units_rented')

    except AttributeError:
        logger.error("'data' variable object has no attribute 'values'")


    return data

def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    with pysnooper.snoop():
        args = parse_cmd_arguments() # add exception for no parameters / warning
        data = load_rentals_file(args.input)
        data = calculate_additional_fields(data)
        save_to_json(args.output, data)
