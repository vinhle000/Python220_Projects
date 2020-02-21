from multiprocessing import Pool, Process, Queue
import functools
import time
import csv
import threading
import logging
import asyncio

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def time_me(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Ran {func.__name__!r} in {run_time:.4f} secs")
        return value

    return wrapper_timer


def fibo(n):
    if n <= 1:
        return 1
    return fibo(n - 1) + fibo(n - 2)


@time_me
def calc_for_serial(one_range):
    results = []
    for num in one_range:
        results.append([fibo(i) for i in range(num)])
    return results


@time_me
def calc_for_parallel(one_range):
    results = [fibo(i) for i in range(one_range)]
    return results


@time_me
def do_parallel(runs):
    size = len(runs)
    # results = []
    with Pool(2) as p:
        [results] = [p.map(calc_for_parallel, runs)]  # Maps a process to a calculate the run from a the number_set passed in
        logger.debug(results)
    return results

# USE OF THREADS
class ThreadResult:
    """Class to create the mutex lock, and hold the results of the threads running in parallel"""
    lock = threading.Lock()
    list_data = []
    # Could use a Queue as instead


@time_me
def calc_for_parallel_threads(one_range):
    results = [fibo(i) for i in range(one_range)]
    ThreadResult.lock.acquire()
    ThreadResult.list_data.append(results)
    ThreadResult.lock.release()

@time_me
def do_parallel_threads(runs):
    ThreadResult.list_data = []  # Reset/Clear list data back to empty list
    threads = []
    for run in runs:
        thread = threading.Thread(target=calc_for_parallel_threads, args=(run,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()  # waits for threads to finish before it continues

    logger.debug(ThreadResult.list_data)
    return ThreadResult.list_data

# USE OF ASYNC
# results_list = []
#
# async def calc_for_parallel_async(one_range):
#     results = [fibo(i) for i in range(one_range)]
#     results_list.append(results)
#
# def do_parallel_async(runs):
#     results_list = []  # Resets/Clear list
#     runner = asyncio.get_event_loop()
#
#     for run in runs:
#         runner.create_task(calc_for_parallel_async(run))
#
#     runner.run_forever()
#     runner.close()
#     logger.debug(results_list)
#     return results_list

# USE OF PROCESSES
data_q = Queue()

@time_me
def calc_for_parallel_process(one_range):
    result = [fibo(i) for i in range(one_range)]
    logger.debug(result)
    data_q.put(result)

@time_me
def do_parallel_process(runs):
    data_q.empty()
    results = []
    proc_list = []
    for run in runs:
        proc = Process(target=calc_for_parallel_process, args=(run,))
        proc_list.append(proc)
        proc.start()
        print("______")

    print("+++++")

    results = [data_q.get() for i in proc_list]
    logger.debug(results)
    print("*******")
    return results

@time_me
def do_serial(runs):
    results = []
    results.append(calc_for_serial(runs))
    [results] = results
    return results


@time_me
def save_serial(results, header, footer):
    counter = 0
    logger.debug(results)
    for result_set in results:
        for file in result_set:
            counter += 1
            with open('res' + str(counter) + '.txt', 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([header, file, footer])


# Maybe try thread spawning other threads

class ParallelData:
    counter = 0
    lock = threading.Lock()

# class ResultSetThread(threading.Thread):
#     def run(self):
#         file_thread = FileThread()
#         file_thread.start()

class FileThread(threading.Thread):

    def __init__(self, header, file, footer):
        threading.Thread.__init__(self)
        self.header = header
        self.file = file
        self.footer = footer

    def run(self):
        ParallelData.lock.acquire()
        ParallelData.counter += 1
        ParallelData.lock.release()
        with open('res' + str(ParallelData.counter) + '.txt', 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([self.header, self.file, self.footer])


@time_me
def save_parallel(results, header, footer):
    counter = 0
    logger.debug(results)
    for result_set in results:
        for file in result_set:
           thread = FileThread(header, file, footer)
           thread.start()





@time_me
def main():
    ranges = ((10, 12, 5, 7, 4, 3, 2), (35, 30, 25, 40), (40, 38, 42))
    parallel = []
    serial = []
    for number_set in ranges:
        parallel.append(do_parallel_threads(number_set))
        serial.append(do_serial(number_set))

    header = "h" * 100000000
    footer = "f" * 100000000

    parallel = parallel[0]
    serial = serial[0]
    save_serial(serial, header, footer)
    save_parallel(parallel, header, footer)


if __name__ == "__main__":
    main()


"""
First Original run
Ran 'calc_for_parallel' in 0.0000 secs
Ran 'calc_for_parallel' in 0.0001 secs
Ran 'calc_for_parallel' in 0.0000 secs
Ran 'calc_for_parallel' in 0.0000 secs
Ran 'calc_for_parallel' in 0.0000 secs
Ran 'calc_for_parallel' in 0.0000 secs
Ran 'calc_for_parallel' in 0.0000 secs
Ran 'do_parallel' in 0.1786 secs
Ran 'calc_for_serial' in 0.0001 secs
Ran 'do_serial' in 0.0001 secs

Ran 'calc_for_parallel' in 0.0387 secs
Ran 'calc_for_parallel' in 0.4595 secs
Ran 'calc_for_parallel' in 4.8584 secs
Ran 'calc_for_parallel' in 52.5120 secs
Ran 'do_parallel' in 52.7064 secs
Ran 'calc_for_serial' in 56.8237 secs
Ran 'do_serial' in 56.8237 secs

Ran 'calc_for_parallel' in 20.4934 secs
Ran 'calc_for_parallel' in 52.9245 secs
Ran 'calc_for_parallel' in 138.7730 secs
Ran 'do_parallel' in 138.9404 secs
Ran 'calc_for_serial' in 204.2321 secs
Ran 'do_serial' in 204.2322 secs

Ran 'save_serial' in 228.3163 secs
Ran 'save_parallel' in 0.0000 secs
Ran 'main' in 681.2865 secs
"""


"""
Running with pool of 2
Ran 'calc_for_parallel' in 0.0000 secs
Ran 'calc_for_parallel' in 0.0001 secs
Ran 'calc_for_parallel' in 0.0000 secs
Ran 'calc_for_parallel' in 0.0000 secs
Ran 'calc_for_parallel' in 0.0000 secs
Ran 'calc_for_parallel' in 0.0000 secs
Ran 'calc_for_parallel' in 0.0000 secs
Ran 'do_parallel' in 0.1360 secs
Ran 'calc_for_serial' in 0.0001 secs
Ran 'do_serial' in 0.0001 secs

Ran 'calc_for_parallel' in 0.5260 secs
Ran 'calc_for_parallel' in 0.0376 secs
Ran 'calc_for_parallel' in 5.1407 secs
Ran 'calc_for_parallel' in 50.9536 secs
Ran 'do_parallel' in 51.6709 secs
Ran 'calc_for_serial' in 56.3757 secs
Ran 'do_serial' in 56.3757 secs

Ran 'calc_for_parallel' in 20.8798 secs
Ran 'calc_for_parallel' in 55.9482 secs
Ran 'calc_for_parallel' in 137.7519 secs
Ran 'do_parallel' in 158.8258 secs
Ran 'calc_for_serial' in 206.7084 secs
Ran 'do_serial' in 206.7085 secs

Ran 'save_serial' in 237.8291 secs
Ran 'save_parallel' in 0.0000 secs
Ran 'main' in 711.6385 secs
"""

""" 
Running with pool of 20
Ran 'calc_for_parallel' in 0.0001 secs
Ran 'calc_for_parallel' in 0.0001 secs
Ran 'calc_for_parallel' in 0.0000 secs
Ran 'calc_for_parallel' in 0.0000 secs
Ran 'calc_for_parallel' in 0.0000 secs
Ran 'calc_for_parallel' in 0.0000 secs
Ran 'calc_for_parallel' in 0.0000 secs
Ran 'do_parallel' in 0.2868 secs
Ran 'calc_for_serial' in 0.0001 secs
Ran 'do_serial' in 0.0001 secs

Ran 'calc_for_parallel' in 0.0887 secs
Ran 'calc_for_parallel' in 0.4811 secs
Ran 'calc_for_parallel' in 4.8112 secs
Ran 'calc_for_parallel' in 53.0557 secs
Ran 'do_parallel' in 53.3916 secs
Ran 'calc_for_serial' in 58.0960 secs
Ran 'do_serial' in 58.0960 secs

Ran 'calc_for_parallel' in 21.2788 secs
Ran 'calc_for_parallel' in 55.2495 secs
Ran 'calc_for_parallel' in 140.1409 secs
Ran 'do_parallel' in 140.4670 secs
Ran 'calc_for_serial' in 207.8432 secs
Ran 'do_serial' in 207.8432 secs

Ran 'save_serial' in 229.3836 secs
Ran 'save_parallel' in 0.0000 secs
Ran 'main' in 689.5582 secs
"""

""" Running with Threads
Ran 'calc_for_parallel_threads' in 0.0000 secs
Ran 'calc_for_parallel_threads' in 0.0001 secs
Ran 'calc_for_parallel_threads' in 0.0000 secs
Ran 'calc_for_parallel_threads' in 0.0000 secs
Ran 'calc_for_parallel_threads' in 0.0000 secs
Ran 'calc_for_parallel_threads' in 0.0000 secs
Ran 'calc_for_parallel_threads' in 0.0000 secs
Ran 'do_parallel_threads' in 0.0025 secs
Ran 'calc_for_serial' in 0.0001 secs
Ran 'do_serial' in 0.0001 secs

Ran 'calc_for_parallel_threads' in 0.1401 secs
Ran 'calc_for_parallel_threads' in 1.2206 secs
Ran 'calc_for_parallel_threads' in 10.3192 secs
Ran 'calc_for_parallel_threads' in 57.7420 secs
Ran 'do_parallel_threads' in 57.8500 secs
Ran 'calc_for_serial' in 57.9982 secs
Ran 'do_serial' in 57.9983 secs

Ran 'calc_for_parallel_threads' in 226.2336 secs
Ran 'do_parallel_threads' in 226.2568 secs
Ran 'calc_for_serial' in 214.6230 secs
Ran 'do_serial' in 214.6230 secs
Ran 'save_serial' in 229.1793 secs
Ran 'save_parallel' in 0.0000 secs

Ran 'main' in 786.0006 secs
"""



"""
1)Explain the time difference between the serial and parallel functions
    Parallel function initially has overhead from creating the pool for processes, and therefore
    takes longer to run than the the Serial function.
    But over time when the functions are running again, Parallel completes it calculations for the second set of 
    tuples faster than Serial.
    And for the third set of tuples, which contain less numbers, but are higher in value, the parallel function is 
    completing the function even faster than the Serial function. The time gap between the completion times of the two
    functions became greater.


2)Explain why serial is faster in the first number_set and slower in the rest
     Parallel function initially has overhead from creating the pool and each separate processes to run
     in parallel, so taking longer to run and complete than the the Serial function.
     Pool starts a new instance of the python interpreter  in its in own core.
     
     
3)What is the impact of changing Pool(size) to different values? Why? Does it even make a difference? Why?
    Changing the pool size to a greater value, did not have a significant impact on time of completion(This could vary)
    Changing the pool size to a lower value however, did have a longer run to complete
    
    Pool.map applies that function to each element to the iterable
    
"""