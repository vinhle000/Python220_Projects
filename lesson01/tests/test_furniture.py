import pytest
from lesson01 import furniture

def test_calculate_transaction():
    test_transactions = [('Chair', 'A', 10),
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
                         ('Chair', 'S', 10),
                         ('Bed', 'S', 12),
                         ('Couch', 'S', 10),
                         ('Table', 'S', 12),
                         ('Lamp', 'S', 10)]

    assert(furniture.calculate_transactions(test_transactions) == [('Chair', 0), ('Bed', 0), ('Couch', 0), ('Table', 0),('Lamp', 0)])


def test_initial_subtract_transaction():
    test_transaction = [('Chair', 'S', 10),
                         ('Chair', 'A', 12)]
    with pytest.raises(ValueError):
        furniture.calculate_transactions(test_transaction)


def test_negative_amount_exception():
    test_transactions = [('Chair', 'A', 10),
                         ('Chair', 'S', 12)]

    with pytest.raises(ValueError):
        furniture.calculate_transactions(test_transactions)

if __name__ == "__main__":
    pytest.main([__file__])