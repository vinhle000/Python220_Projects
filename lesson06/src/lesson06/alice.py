"""
performance analysis
"""
import csv
from lesson06.alice_ut import Speedy, timer
import timeit

"""
Importing Speedy from the alice utilities, This class is used as a decorator for the 
fibo() function. This decorator allows the function to be called and save its return values
into a Key, Value pair. Where the Argument is the key, and the fibo() function return is the
value of the dictionary. 
This provides faster lookups when the fibi() function is called when
it is used for the list comprehension. It will provide the fibo() sequence faster from a dictionary
lookup if the value has already been previously passed in, instead of running the function completely again.
This allows the function to be aware of its previous return values.
"""

"""
Process time when running with @Speedy decorator
0.0023490000000000455
"""

@Speedy
def fibo(n):
    if n <= 1:
        return 1
    return fibo(n - 1) + fibo(n - 2)


def save_it(alist, name):
    with open(name, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(alist)


def calc(write=False, ranges=(25, 35, 20, 42)):
    a = [fibo(i) for i in range(ranges[0])]
    if write:
        save_it(a, "a.csv")
    b = [fibo(i) for i in range(ranges[1])]
    if write:
        save_it(b, "b.csv")
    c = [fibo(i) for i in range(ranges[2])]
    if write:
        save_it(c, "c.csv")
    d = [fibo(i) for i in range(ranges[3])]
    if write:
        save_it(d, "d.csv")


if __name__ == "__main__":
    #calc(True, (24, 34, 21, 42))
    print(timeit.timeit('calc(True, (24, 34, 21, 42))', globals=globals(), number=1))
