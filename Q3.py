import threading
import time


# ============================================================
# 1. Factorial function (iterative)
# ============================================================
def factorial(n: int) -> int:
    """
    Compute factorial of n iteratively.
    Time complexity: O(n) – n-1 multiplications.
    """
    if n < 0:
        raise ValueError("Factorial undefined for negative numbers")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


# ============================================================
# 2. Thread worker function
# ============================================================
def factorial_worker(n: int, results: dict, key: int):
    """Target function for each thread; stores result in shared dict."""
    results[key] = factorial(n)


# ============================================================
# 3. Multithreaded experiment (10 rounds)
# ============================================================
def run_multithreaded(rounds: int = 10):
    print("\n" + "=" * 60)
    print("MULTITHREADED EXECUTION (10 rounds)")
    print("=" * 60)

    times = []
    for r in range(1, rounds + 1):
        results = {}
        numbers = [50, 100, 200]
        threads = []

        # Record start time before starting any thread
        start_time = time.perf_counter_ns()

        # Create and start one thread per number
        for num in numbers:
            t = threading.Thread(target=factorial_worker, args=(num, results, num))
            threads.append(t)
            t.start()

        # Wait for all threads to finish
        for t in threads:
            t.join()

        end_time = time.perf_counter_ns()
        elapsed = end_time - start_time
        times.append(elapsed)
        print(f"Round {r:2d} : {elapsed:>12,} ns")

    avg_time = sum(times) / len(times)
    print(f"\nAverage time (multithreaded) : {avg_time:>12,.2f} ns")
    return times, avg_time


# ============================================================
# 4. Sequential experiment (10 rounds)
# ============================================================
def run_sequential(rounds: int = 10):
    print("\n" + "=" * 60)
    print("SEQUENTIAL EXECUTION (10 rounds)")
    print("=" * 60)

    times = []
    for r in range(1, rounds + 1):
        start_time = time.perf_counter_ns()

        # Compute factorials one after another (no threads)
        fac50 = factorial(50)
        fac100 = factorial(100)
        fac200 = factorial(200)

        end_time = time.perf_counter_ns()
        elapsed = end_time - start_time
        times.append(elapsed)
        print(f"Round {r:2d} : {elapsed:>12,} ns")

    avg_time = sum(times) / len(times)
    print(f"\nAverage time (sequential)    : {avg_time:>12,.2f} ns")
    return times, avg_time


# ============================================================
# 5. Main program – runs both experiments and compares
# ============================================================
if __name__ == "__main__":

    # --- Run multithreaded test ---
    mt_times, mt_avg = run_multithreaded(10)

    # --- Run sequential test ---
    seq_times, seq_avg = run_sequential(10)

    # --- Comparison ---
    print("\n" + "=" * 60)
    print("FINAL COMPARISON")
    print("=" * 60)
    print(f"Multithreaded average time : {mt_avg:>15,.2f} ns")
    print(f"Sequential average time    : {seq_avg:>15,.2f} ns")
    print(f"Difference (MT - Seq)      : {mt_avg - seq_avg:>15,.2f} ns")

    if mt_avg < seq_avg:
        print("\n✓ Multithreading was faster in this experiment.")
    else:
        print("\n✗ Multithreading was NOT faster; it added overhead.")

    # --- Discussion summary (prints to console for your report) ---
    print("\n" + "=" * 60)
    print("ANALYSIS & DISCUSSION")
    print("=" * 60)
    print("""
1.  Python's Global Interpreter Lock (GIL) allows only one thread 
    to execute Python bytecode at a time. Therefore, for CPU-bound 
    tasks like factorial computation, multithreading does NOT achieve 
    true parallelism (simultaneous execution on multiple cores).

2.  In this experiment, the multithreaded version is actually slower 
    because:
    - The GIL serialises the three factorial computations.
    - Thread creation, context switching, and joining add extra 
      overhead that sequential execution does not have.

3.  Time complexity of factorial(n): O(n) because the loop runs 
    (n-1) times, performing one multiplication each iteration.

4.  When DOES multithreading help?
    - For I/O-bound tasks (e.g., downloading files, querying a 
      database, reading/writing to disk). While one thread waits 
      for I/O, it releases the GIL, so other threads can run, 
      effectively overlapping waiting times and reducing total 
      elapsed time.
""")