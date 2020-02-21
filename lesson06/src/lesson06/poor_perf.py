"""
performance analysis
"""
import csv
import time
import timeit


def fibo(n):
    if n <= 1:
        return 1
    return fibo(n - 1) + fibo(n - 2)


def save_it(alist, name):
    with open(name, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(alist)



def calc(write=False, ranges=(25, 35, 20, 42)):
    # you can only change code between this line....
    # and within fibo and save_it

    # First run without edits
    # Approx 240.25756067700001
    if write:
        init = time.clock()
        a = [fibo(i) for i in range(ranges[0])]
        save_it(a, "a.csv")
        b = [fibo(i) for i in range(ranges[1])]
        save_it(b, "b.csv")
        c = [fibo(i) for i in range(ranges[2])]
        save_it(c, "c.csv")
        d = [fibo(i) for i in range(ranges[3])]
        save_it(d, "d.csv")

        duration = time.clock() - init
        print("First process time: {}".format(duration))

        # Created the list, with comprehension, within the save_it() function
        # rather than creating a list as a variable first, then passing it
        # as an argument
        # Approx 4.9435781069999996
        save_it([fibo(i) for i in range(ranges[0])], "a.csv")
        save_it([fibo(i) for i in range(ranges[1])], "b.csv")
        save_it([fibo(i) for i in range(ranges[2])], "c.csv")
        save_it([fibo(i) for i in range(ranges[2])], "d.csv")

        new_duration = time.clock() - (init + duration)
        print("Second process time: {}".format(new_duration))


        # Passed in A list of that contains map object, it maps fibo function to every item in range list
        # Approx 0.003171678000000004
        save_it([map(fibo, (x for x in range(ranges[0])))], "a.csv")
        save_it([map(fibo, (x for x in range(ranges[1])))], "b.csv")
        save_it([map(fibo, (x for x in range(ranges[2])))], "c.csv")
        save_it([map(fibo, (x for x in range(ranges[3])))], "d.csv")

        #duration = time.clock() - (init + duration)
        print("Third process time: {}".format(time.clock() - (init + duration + new_duration)))

    # and this line


if __name__ == "__main__":

    print(timeit.timeit('calc(True, (24, 34, 21, 42))', globals=globals(), number=1))


# Multiple if statements slowing it down