from multiprocessing import Pool, Process, Queue, Lock
import functools
import time
import csv
import threading
import logging
import os
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
    with Pool(size) as p:
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
class AsyncResult:
    """Static class to store Results of Async tasks"""
    lock = asyncio.Lock()
    list_data = []


@time_me
async def calc_for_parallel_async(one_range):
    results = [fibo(i) for i in range(one_range)]
    await AsyncResult.lock.acquire()
    try:
        AsyncResult.list_data.append(results)
    finally:
        AsyncResult.lock.release()


async def create_parallel_async_tasks(loop, runs):
    """Helper function to create tasks, need the await for all tasks to complete"""
    tasks = []
    for run in runs:
        tasks.append(loop.create_task(calc_for_parallel_async(run)))
    await asyncio.wait(tasks)


@time_me
def do_parallel_async(runs):
    AsyncResult.list_data = []  # Resets/Clear list
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_parallel_async_tasks(loop, runs))

    #logger.debug(AsyncResult.list_data)
    return AsyncResult.list_data



# USE OF PROCESSES
# Currently not working

# data_q = Queue()
#
# @time_me
# def calc_for_parallel_process(one_range):
#     result = [fibo(i) for i in range(one_range)]
#     logger.debug(result)
#     data_q.put(result)
#
# @time_me
# def do_parallel_process(runs):
#     data_q.empty()
#     results = []
#     proc_list = []
#     for run in runs:
#         proc = Process(target=calc_for_parallel_process, args=(run,))
#         proc_list.append(proc)
#         proc.start()
#         print("______")
#
#     print("+++++")
#
#     results = [data_q.get() for i in proc_list]
#     logger.debug(results)
#     print("*******")
#    return results

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


class ParallelData:
    counter = 0
    lock = threading.Lock()



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
    ParallelData.counter = 0
    thread_list = []
    for result_set in results:
        for file in result_set:
            thread = FileThread(header, file, footer)
            thread_list.append(thread)
            thread.start()

    for thread in thread_list:
        thread.join()

@time_me
def main():
    ranges = ((10, 12, 5, 7, 4, 3, 2), (35, 30, 25, 40), (40, 38, 42))
    parallel = []
    serial = []
    for number_set in ranges:
        parallel.append(do_parallel(number_set))
        serial.append(do_serial(number_set))

    header = "h" * 100000000
    footer = "f" * 100000000

    parallel = parallel[0]
    serial = serial[0]
    save_serial(serial, header, footer)
    save_parallel(parallel, header, footer)


if __name__ == "__main__":
    main()
