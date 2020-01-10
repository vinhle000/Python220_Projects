from lesson01 import furniture
import pytest



def test_calculate():
    tranactions = [('Chair', 'S', 10),
                   ('Bed', 'A', 12),
                   ('Chair', 'S', 6)]

    result = [('Chair', 4), ('Bed', 12)]

    assert(furniture.calculate_transactions(tranactions), result)