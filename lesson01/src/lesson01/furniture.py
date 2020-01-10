""""## What you need to do
1. Create a new Python project
1. The project will use a list of tuples of product transactions as input.
1. The project will display a list of tuples of products and stock quantities as output.
1. The input tuple will contain a product name, a transaction type code of A,
   or S (add, sell), and a quantity.
1. There should be several transactions for each product, so quantities can be
   added and sold.
1. The output list of tuples will show the final stock quantities for every product as a
   result of processing all the transactions.
1. There will be exactly one record in output for each input product, showing
   the product name and quantity.
"""



def calculate_transactions(transactions):

    transaction_dict = {}

    for transaction in transactions:
        item = transaction[0]
        transaction_type = transaction[1]
        amount = transaction[2]

        # if transaction_type == 'A':
        #     if item in transaction_dict.keys():
        #         curr_amount = transaction_dict[item]
        #     else:
        #         curr_amount = 0
        #     transaction_dict[item] = curr_amount + amount
        #
        # if transaction_type == 'S':
        #     if item in transaction_dict.keys():
        #         curr_amount = transaction_dict[item]
        #     else:
        #         curr_amount = 0
        #     transaction_dict[item] = curr_amount - amount


        if transaction_type == 'A':

            if item not in transaction_dict.keys():
                curr_amount = 0
            else:
                curr_amount = transaction_dict[item]
            transaction_dict[item] = curr_amount + amount

        if transaction_type == 'S':
            if item not in transaction_dict.keys():
                curr_amount = 0
            else:
                curr_amount = transaction_dict[item]
            transaction_dict[item] = curr_amount - amount

    # Test Dictionary
    print(transaction_dict.items())

    return transaction_dict.items()


if __name__ == "__main__":
    product_transactions = [('Chair', 'S', 10),
                            ('Bed', 'A', 12),
                            ('Chair', 'S', 6)]

    calculate_transactions(product_transactions)