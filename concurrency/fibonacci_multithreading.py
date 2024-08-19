import threading
import queue
import time
import sysconfig
import sys
import os

os.environ["Py_GIL_DISABLED"] = "1"
os.environ["PYTHON_GIL"] = "0"

# Check if the current interpreter is configured with --disable-gil
is_gil_disabled = sysconfig.get_config_var("Py_GIL_DISABLED")
print(f"GIL disabled in build: {is_gil_disabled}")

# Check if the GIL is actually disabled in the running process
is_gil_enabled = sys._is_gil_enabled()
print(f"GIL enabled at runtime: {is_gil_enabled}")

def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

def worker(q, results):
    while not q.empty():
        n = q.get()  
        results[n] = fibonacci(n)
        q.task_done()

if __name__ == '__main__':

    n = 10000  # Number of Fibonacci numbers to generate
    num_threads = 4  # Number of threads to use

    q = queue.Queue()
    results = [None] * n

    # Enqueue tasks
    for i in range(n):
        q.put(i)

    start = time.time()
    # Create and start threads
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(q, results))
        t.start()
        threads.append(t)

    # Wait for all tasks to be completed
    q.join()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    #print("Fibonacci sequence:", results)
    end = time.time()
    print("Time being used in second -", end - start)
