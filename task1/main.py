import time

def caching_fibonacci():
    cache = {}

    def fibonacci(n):
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        elif n in cache:
            return cache[n]
        else:
            cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
            return cache[n]
    return fibonacci


if __name__ == "__main__":
    fib = caching_fibonacci()

    # First call - builds cache
    start_time = time.time()
    print("fib(10) =", fib(10))
    end_time = time.time()
    print(f"Execution time (first call): {end_time - start_time:.10f} seconds")

    # Second call - uses cache
    start_time = time.time()
    print("fib(10) =", fib(10))
    end_time = time.time()
    print(f"Execution time (second call): {end_time - start_time:.10f} seconds")

    # A bigger number - partially cached, partially new
    start_time = time.time()
    print("fib(15) =", fib(15))
    end_time = time.time()
    print(f"Execution time (fib(15)): {end_time - start_time:.10f} seconds")
    
