'''

Returns total price paid for individual rentals

'''
import argparse
import json
import datetime
import math
import sys
import pysnooper
from loguru import logger

log_format = "{time} {file}:{line:3d} {level} {message}"
log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
logger.remove() #Removes Default Handler
logger.add(sys.stderr, format=log_format, level="DEBUG")
logger.add(log_file, format=log_format, level="INFO") # Does not include log Debug statements


# @pysnooper.snoop()
def parse_cmd_arguments():
    """System argument parser
    -input and output json file arguments are required"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)

    return parser.parse_args()


# @pysnooper.snoop()
def load_rentals_file(filename):
    """Loads Json into a dictionary and that is returned
    :param filename: JSON file to be loaded
    :return: data - a dictionary from the loaded JSON file
    """

    with open(filename) as file:
        try:
            data = json.load(file) # Double quotes expected at line 5884 in Json
                                   # fixed by removed extra comma char
            logger.debug("json file is loaded, and variable not assigned")
        except json.decoder.JSONDecodeError:
            logger.error("Expecting property name enclosed in double quotes in JSON")
            logger.warning("json file was not loaded")
    try:
        return data
    except UnboundLocalError:
        logger.error("local variable 'data' referenced before assignment")


# @pysnooper.snoop()
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

                # The difference is a negative number,
                # need to make it an absolute number
                value['total_days'] = (rental_end - rental_start).days

                value['total_price'] = value['total_days'] * value['price_per_day']

                # logger.debug("total_days = {}".format(value['total_days']))
                # logger.debug("price_per_day = {}".format(value['price_per_day']))
                # logger.debug("total_price = {}".format(value['total_price']))
                # logger.debug("units_rented = {}".format(value['units_rented']))

                # total_price is a negative number, due to the difference acquired in total_days
                value['sqrt_total_price'] = math.sqrt(value['total_price'])

                # there is data in the json that includes 'units_rented' = 0
                value['unit_cost'] = value['total_price'] / value['units_rented']

            except ValueError:
                logger.debug(value)

                # total_price was a negative value,
                # or there was no value provided for the rental_end property in the JSON
                logger.warning('"sqrt_total_price" was not able to be attained')


            except ZeroDivisionError:
                logger.debug(value)
                logger.error('division by zero, occurred from trying to calculate unit_cost')

    except AttributeError:  # Occurs due to no proper Json file was loaded,
                            # In this case, due to the syntax error in the Json file at line 5884
        logger.error("'data' variable object has no attribute 'values'")

    return data


def save_to_json(filename, data):
    """Saves data dictionary to JSON file

    :param filename: Name of file for data to be saved as a JSON file
    :param data: dictionary
    """
    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    with pysnooper.snoop():
        try:
            args = parse_cmd_arguments()
        except:
            logger.error("the following arguments are required: -i/--input, -o/--output")

        data = load_rentals_file(args.input)
        data = calculate_additional_fields(data)
        save_to_json(args.output, data)
