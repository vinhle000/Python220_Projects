"""Furniture Product Transactions"""

product_transactions = [('Chair', 'A', 10),
                        ('Bed', 'A', 12),
                        ('Couch', 'A', 10),
                        ('Table', 'A', 12),
                        ('Lamp', 'A', 10),
                        ('Chair', 'S', 10),
                        ('Bed', 'S', 12),
                        ('Couch', 'S', 10),
                        ('Table', 'S', 12),
                        ('Lamp', 'S', 10),
                        ('Chair', 'A', 10),
                        ('Bed', 'A', 12),
                        ('Couch', 'A', 10),
                        ('Table', 'A', 12),
                        ('Lamp', 'A', 10),
                        ('Chair', 'A', 10),
                        ('Bed', 'A', 12),
                        ('Couch', 'A', 10),
                        ('Table', 'A', 12),
                        ('Lamp', 'A', 10)]


def calculate_transactions(transactions):
    """Calculates the product transactions of each item in the list
        and returns a dictionary of the item and quanity

    :param transactions: A list of tuples that include a item name,
            transaction type A(Add) or S(Sell), and quantity within in each tuple
    :return: Dictionary of item name and quantity representing the record of the final stock
    """
    transaction_dict = dict()

    for transaction in transactions:
        item_name = transaction[0]
        transaction_type = transaction[1]
        new_amount = transaction[2]

        if transaction_type == "A":
            if item_name in transaction_dict.keys():
                current_amount = transaction_dict[item_name]
            else:
                current_amount = 0
            transaction_dict[item_name] = current_amount + new_amount

        if transaction_type == "S":
            if item_name in transaction_dict.keys():
                current_amount = transaction_dict[item_name]
            else:
                # Initial transaction is sell, which will cause quantities to go below zero
                raise ValueError("Transaction has caused quantity to go below zero")

            # Check if amount subtracting transaction goes negative
            if new_amount <= current_amount:
                transaction_dict[item_name] = current_amount - new_amount
            else:
                raise ValueError("Transaction has caused quantity to go below zero")

    return [(key,value) for key, value in transaction_dict.items()]


# if __name__ == "__main__":
#     print(calculate_transactions(product_transactions))
