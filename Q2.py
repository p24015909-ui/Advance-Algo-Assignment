from datetime import datetime
import time
import sys


class Transaction:
    """Transaction entity class representing a customer transaction in an online shopping system"""

    def __init__(self, transaction_id, customer_name, product_name, amount, transaction_date):
        """
        Constructor for Transaction class
        Divide step: Creating individual transaction objects
        """
        self.transaction_id = transaction_id
        self.customer_name = customer_name
        self.product_name = product_name
        self.amount = amount
        self.transaction_date = transaction_date

    # Getters and Setters
    def get_transaction_id(self):
        return self.transaction_id

    def set_transaction_id(self, transaction_id):
        self.transaction_id = transaction_id

    def get_customer_name(self):
        return self.customer_name

    def set_customer_name(self, customer_name):
        self.customer_name = customer_name

    def get_product_name(self):
        return self.product_name

    def set_product_name(self, product_name):
        self.product_name = product_name

    def get_amount(self):
        return self.amount

    def set_amount(self, amount):
        self.amount = amount

    def get_transaction_date(self):
        return self.transaction_date

    def set_transaction_date(self, transaction_date):
        self.transaction_date = transaction_date

    def __str__(self):
        """String representation of Transaction"""
        return f"ID: {self.transaction_id:6d} | Customer: {self.customer_name:15s} | Product: {self.product_name:20s} | Amount: ${self.amount:8.2f} | Date: {self.transaction_date}"

    def __repr__(self):
        return self.__str__()


class TransactionSystem:
    """Main system implementing Divide and Conquer algorithms"""

    def __init__(self):
        """Initialize the transaction system with empty transaction list"""
        self.transactions = []
        self.recursive_call_count = 0
        self.sort_comparisons = 0

    def load_sample_data(self):
        """
        Create a dataset of transactions (10-30 records)
        The dataset will initially be unsorted
        """
        # Sample data - 15 transactions with unsorted IDs
        sample_data = [
            (105, "Alice Johnson", "Laptop", 1200.50, "2026-01-15"),
            (102, "Bob Smith", "Smartphone", 799.99, "2026-01-12"),
            (108, "Carol White", "Headphones", 199.95, "2026-01-18"),
            (101, "David Brown", "Tablet", 499.00, "2026-01-10"),
            (110, "Eve Davis", "Monitor", 349.50, "2026-01-20"),
            (104, "Frank Wilson", "Keyboard", 89.99, "2026-01-14"),
            (107, "Grace Lee", "Mouse", 49.99, "2026-01-17"),
            (103, "Henry Taylor", "Printer", 289.00, "2026-01-13"),
            (109, "Ivy Martinez", "Webcam", 79.95, "2026-01-19"),
            (106, "Jack Anderson", "Speakers", 159.00, "2026-01-16"),
            (113, "Karen Thomas", "External HDD", 129.99, "2026-01-23"),
            (111, "Liam Garcia", "USB Cable", 19.99, "2026-01-21"),
            (115, "Mia Robinson", "Desk Lamp", 45.50, "2026-01-25"),
            (112, "Noah Clark", "Notebook", 35.00, "2026-01-22"),
            (114, "Olivia Wright", "Calculator", 25.99, "2026-01-24"),
        ]

        self.transactions = []
        for data in sample_data:
            transaction = Transaction(
                data[0], data[1], data[2], data[3], data[4]
            )
            self.transactions.append(transaction)

        print(f"✓ Loaded {len(self.transactions)} transaction records")

    def display_all_transactions(self, title="All Transactions"):
        """
        Display all transactions in the current order
        """
        print(f"\n{'=' * 100}")
        print(f"{title}")
        print(f"{'=' * 100}")
        print(f"Total records: {len(self.transactions)}\n")

        if not self.transactions:
            print("No transactions to display.")
            return

        for i, transaction in enumerate(self.transactions, 1):
            print(f"{i:3d}. {transaction}")
        print(f"{'=' * 100}")

    # ============ MERGE SORT IMPLEMENTATION (Divide and Conquer) ============

    def merge_sort(self, arr, key_func=None, depth=0):
        """
        Merge Sort implementation using Divide and Conquer strategy

        DIVIDE step: Split array into two halves
        CONQUER step: Recursively sort each half
        COMBINE step: Merge the two sorted halves

        Args:
            arr: List to sort
            key_func: Function to extract comparison key (e.g., lambda x: x.transaction_id)
            depth: Current recursion depth (for visualization)

        Returns:
            Sorted list
        """
        # Recursive call counter (for advanced feature)
        self.recursive_call_count += 1

        # BASE CASE: If array has 0 or 1 element, it's already sorted
        if len(arr) <= 1:
            return arr

        # DIVIDE step: Split the array into two halves
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        # Visualize the divide step (optional)
        # print(f"{'  ' * depth}DIVIDE: Splitting {len(arr)} elements into [{len(left_half)}] and [{len(right_half)}]")

        # CONQUER step: Recursively sort both halves
        left_sorted = self.merge_sort(left_half, key_func, depth + 1)
        right_sorted = self.merge_sort(right_half, key_func, depth + 1)

        # COMBINE step: Merge the two sorted halves
        merged = self.merge(left_sorted, right_sorted, key_func, depth)

        return merged

    def merge(self, left, right, key_func, depth=0):
        """
        Merge two sorted lists into one sorted list

        This is the COMBINE step of the Divide and Conquer strategy

        Args:
            left: First sorted list
            right: Second sorted list
            key_func: Function to extract comparison key
            depth: Current recursion depth (for visualization)

        Returns:
            Merged sorted list
        """
        result = []
        i = j = 0

        # Compare elements from left and right and merge in sorted order
        while i < len(left) and j < len(right):
            # Get comparison keys
            left_key = key_func(left[i]) if key_func else left[i]
            right_key = key_func(right[j]) if key_func else right[j]

            self.sort_comparisons += 1

            if left_key <= right_key:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        # Add remaining elements from left (if any)
        while i < len(left):
            result.append(left[i])
            i += 1

        # Add remaining elements from right (if any)
        while j < len(right):
            result.append(right[j])
            j += 1

        # Visualize the merge step (optional)
        # print(f"{'  ' * depth}MERGE: Combined [{len(result)}] elements")

        return result

    def sort_transactions_by_id(self):
        """
        Sort transactions using Merge Sort based on transactionID

        This demonstrates the full Divide and Conquer algorithm:
        1. DIVIDE: Split the list into halves
        2. CONQUER: Recursively sort each half
        3. COMBINE: Merge sorted halves
        """
        print("\n" + "=" * 100)
        print("MERGE SORT - DIVIDE AND CONQUER ALGORITHM")
        print("=" * 100)

        # Reset counters
        self.recursive_call_count = 0
        self.sort_comparisons = 0

        print("\nBEFORE SORTING (Unsorted):")
        self.display_all_transactions("TRANSACTIONS - BEFORE SORTING")

        # Define key function to extract transaction ID for sorting
        def get_transaction_id(transaction):
            return transaction.transaction_id

        # Perform Merge Sort
        print("\n" + "-" * 100)
        print("EXECUTING MERGE SORT (Divide and Conquer)...")
        print("DIVIDE → Split array into halves")
        print("CONQUER → Recursively sort each half")
        print("COMBINE → Merge sorted halves")
        print("-" * 100)

        # Sort using Merge Sort
        start_time = time.time()
        sorted_transactions = self.merge_sort(self.transactions.copy(), get_transaction_id)
        end_time = time.time()

        # Update transactions with sorted list
        self.transactions = sorted_transactions

        print(f"\n✓ Merge Sort completed!")
        print(f"  - Recursive calls: {self.recursive_call_count}")
        print(f"  - Comparisons made: {self.sort_comparisons}")
        print(f"  - Execution time: {(end_time - start_time) * 1000:.4f} ms")

        print("\nAFTER SORTING (Sorted by Transaction ID):")
        self.display_all_transactions("TRANSACTIONS - AFTER SORTING (Merge Sort)")

        return end_time - start_time

    # ============ BINARY SEARCH IMPLEMENTATION (Divide and Conquer) ============

    def binary_search(self, target_id, arr=None, left=0, right=None, depth=0):
        """
        Binary Search implementation using Divide and Conquer strategy

        DIVIDE step: Find middle element and compare
        CONQUER step: Recursively search in left or right half

        Args:
            target_id: The transaction ID to search for
            arr: The sorted array to search in
            left: Left boundary index
            right: Right boundary index
            depth: Current recursion depth (for visualization)

        Returns:
            Tuple (index, recursive_call_count) or (-1, count) if not found
        """
        # Base case: initialize if not provided
        if arr is None:
            arr = self.transactions
            right = len(arr) - 1

        # Recursive call counter
        self.recursive_call_count += 1

        # BASE CASE: If left > right, element not found
        if left > right:
            return -1

        # DIVIDE step: Find the middle element
        mid = (left + right) // 2
        mid_id = arr[mid].transaction_id

        # Print search progress (optional)
        # print(f"{'  ' * depth}Searching in range [{left}..{right}], mid={mid}, ID={mid_id}")

        # Check if target is at the middle
        if mid_id == target_id:
            return mid
        # CONQUER step: Search in the appropriate half
        elif target_id < mid_id:
            # Search in the left half
            return self.binary_search(target_id, arr, left, mid - 1, depth + 1)
        else:
            # Search in the right half
            return self.binary_search(target_id, arr, mid + 1, right, depth + 1)

    def search_transaction_binary(self, transaction_id):
        """
        Search for a transaction using Binary Search (Divide and Conquer)

        This demonstrates the Divide and Conquer strategy:
        1. DIVIDE: Compare with middle element
        2. CONQUER: Recursively search in left or right half
        """
        print("\n" + "=" * 100)
        print("BINARY SEARCH - DIVIDE AND CONQUER ALGORITHM")
        print("=" * 100)

        # Reset recursive call counter
        self.recursive_call_count = 0

        # Ensure transactions are sorted before binary search
        if not self._is_sorted_by_id():
            print("\n⚠️ Warning: Transactions are not sorted by ID.")
            print("Sorting before performing binary search...")
            self.sort_transactions_by_id()

        print(f"\n🔍 Searching for transaction ID: {transaction_id}")
        print("-" * 100)
        print("DIVIDE → Compare with middle element")
        print("CONQUER → Recursively search in left or right half")
        print("-" * 100)

        start_time = time.time()
        index = self.binary_search(transaction_id)
        end_time = time.time()

        print(f"\nBinary Search completed!")
        print(f"  - Recursive calls: {self.recursive_call_count}")
        print(f"  - Execution time: {(end_time - start_time) * 1000:.4f} ms")

        if index != -1:
            print(f"\n✓ Transaction FOUND at position {index + 1}:")
            print(f"  {self.transactions[index]}")
            return True
        else:
            print(f"\n✗ Transaction with ID {transaction_id} NOT FOUND")
            return False

    def _is_sorted_by_id(self):
        """
        Check if transactions are sorted by ID
        """
        for i in range(len(self.transactions) - 1):
            if self.transactions[i].transaction_id > self.transactions[i + 1].transaction_id:
                return False
        return True

    # ============ LINEAR SEARCH (For Comparison) ============

    def linear_search(self, transaction_id):
        """
        Linear Search implementation for comparison with Binary Search
        """
        print("\n" + "=" * 100)
        print("LINEAR SEARCH")
        print("=" * 100)

        print(f"\n🔍 Searching for transaction ID: {transaction_id}")
        print("-" * 100)

        start_time = time.time()
        comparisons = 0

        for i, transaction in enumerate(self.transactions):
            comparisons += 1
            if transaction.transaction_id == transaction_id:
                end_time = time.time()
                print(f"\n✓ Transaction FOUND at position {i + 1} after {comparisons} comparisons:")
                print(f"  {transaction}")
                print(f"  - Execution time: {(end_time - start_time) * 1000:.4f} ms")
                return True

        end_time = time.time()
        print(f"\n✗ Transaction with ID {transaction_id} NOT FOUND")
        print(f"  - Comparisons made: {comparisons}")
        print(f"  - Execution time: {(end_time - start_time) * 1000:.4f} ms")
        return False

    # ============ PERFORMANCE COMPARISON ============

    def compare_performance(self):
        """
        Compare performance of Merge Sort vs Binary Search
        """
        print("\n" + "=" * 100)
        print("PERFORMANCE COMPARISON: Merge Sort vs Binary Search")
        print("=" * 100)

        print("\n📊 Time Complexity Analysis:")
        print("-" * 100)
        print(f"{'Algorithm':<20} {'Time Complexity':<25} {'Space Complexity':<20}")
        print("-" * 100)
        print(f"{'Merge Sort':<20} {'O(n log n)':<25} {'O(n)':<20}")
        print(f"{'Binary Search':<20} {'O(log n)':<25} {'O(1) recursive':<20}")
        print(f"{'Linear Search':<20} {'O(n)':<25} {'O(1)':<20}")
        print("-" * 100)

        print("\n📈 Performance Testing:")
        print("-" * 100)

        # Test Merge Sort performance
        print("\n1. Merge Sort (Divide and Conquer):")
        print("   - Sorts the entire dataset")
        print(f"   - Dataset size: {len(self.transactions)} elements")

        # Reset and sort
        self.sort_transactions_by_id()

        # Test Binary Search performance
        print("\n2. Binary Search (Divide and Conquer):")
        print("   - Searches in sorted dataset")

        # Search for existing transaction
        existing_id = self.transactions[0].transaction_id
        print(f"   - Searching for existing ID: {existing_id}")
        start_time = time.time()
        self.binary_search(existing_id)
        end_time = time.time()
        print(f"   - Time: {(end_time - start_time) * 1000:.4f} ms")

        # Search for non-existing transaction
        non_existing_id = 999
        print(f"   - Searching for non-existing ID: {non_existing_id}")
        start_time = time.time()
        self.binary_search(non_existing_id)
        end_time = time.time()
        print(f"   - Time: {(end_time - start_time) * 1000:.4f} ms")

        # Test Linear Search performance
        print("\n3. Linear Search (Comparison):")
        print("   - Searches in unsorted dataset")

        # Shuffle transactions for linear search
        shuffled = self.transactions.copy()
        random.shuffle(shuffled)

        print(f"   - Searching for existing ID: {existing_id}")
        start_time = time.time()
        for t in shuffled:
            if t.transaction_id == existing_id:
                break
        end_time = time.time()
        print(f"   - Time: {(end_time - start_time) * 1000:.4f} ms")

        print("\n📊 Analysis:")
        print("-" * 100)
        print("• Merge Sort: Efficient for large datasets, O(n log n) complexity")
        print("• Binary Search: Extremely fast for searching, requires sorted data")
        print("• Linear Search: Simple but slow for large datasets")
        print("• Divide and Conquer algorithms show significant performance benefits")
        print("  for large datasets compared to naive approaches")
        print("=" * 100)

    # ============ ADVANCED FEATURES ============

    def insert_transaction_dynamic(self):
        """
        Advanced Feature: Allow user to insert transaction dynamically
        """
        print("\n" + "=" * 100)
        print("INSERT NEW TRANSACTION")
        print("=" * 100)

        try:
            # Get transaction details from user
            transaction_id = int(input("Enter Transaction ID: "))

            # Check if ID already exists
            for t in self.transactions:
                if t.transaction_id == transaction_id:
                    print("❌ Transaction ID already exists!")
                    return

            customer_name = input("Enter Customer Name: ")
            product_name = input("Enter Product Name: ")
            amount = float(input("Enter Amount ($): "))
            date_str = input("Enter Transaction Date (YYYY-MM-DD): ")

            # Create new transaction
            new_transaction = Transaction(transaction_id, customer_name, product_name, amount, date_str)

            # Add to list
            self.transactions.append(new_transaction)

            print(f"\n✓ Transaction added successfully!")
            print(f"  {new_transaction}")

        except ValueError as e:
            print(f"❌ Invalid input: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")

    def sort_by_amount(self):
        """
        Advanced Feature: Sort transactions based on amount using Merge Sort
        """
        print("\n" + "=" * 100)
        print("MERGE SORT - SORT BY AMOUNT")
        print("=" * 100)

        # Reset counters
        self.recursive_call_count = 0
        self.sort_comparisons = 0

        print("\nBEFORE SORTING (Unsorted):")
        self.display_all_transactions("TRANSACTIONS - BEFORE SORTING BY AMOUNT")

        # Define key function to extract amount for sorting
        def get_transaction_amount(transaction):
            return transaction.amount

        # Perform Merge Sort
        start_time = time.time()
        sorted_transactions = self.merge_sort(self.transactions.copy(), get_transaction_amount)
        end_time = time.time()

        # Update transactions with sorted list
        self.transactions = sorted_transactions

        print(f"\n✓ Merge Sort completed!")
        print(f"  - Recursive calls: {self.recursive_call_count}")
        print(f"  - Comparisons made: {self.sort_comparisons}")
        print(f"  - Execution time: {(end_time - start_time) * 1000:.4f} ms")

        print("\nAFTER SORTING (Sorted by Amount):")
        self.display_all_transactions("TRANSACTIONS - SORTED BY AMOUNT")

        return end_time - start_time

    def display_recursive_calls_count(self):
        """
        Advanced Feature: Display count of recursive calls
        """
        print("\n" + "=" * 100)
        print("RECURSIVE CALLS ANALYSIS")
        print("=" * 100)

        print("\n📊 Merge Sort Recursive Calls:")
        print("-" * 100)

        # Run merge sort on a copy to count recursive calls
        temp_list = self.transactions.copy()
        self.recursive_call_count = 0
        self.merge_sort(temp_list, lambda x: x.transaction_id)

        print(f"  Total recursive calls for {len(self.transactions)} elements: {self.recursive_call_count}")
        print(f"  Theoretical calls (2n-1 for n elements): {2 * len(self.transactions) - 1}")
        print(f"  Ratio: {self.recursive_call_count / (2 * len(self.transactions) - 1):.2f}")

        print("\n📊 Binary Search Recursive Calls:")
        print("-" * 100)

        # Run binary search to count recursive calls
        self.recursive_call_count = 0
        if self.transactions:
            self.binary_search(self.transactions[0].transaction_id)
            print(f"  Recursive calls to find element: {self.recursive_call_count}")
            print(f"  Theoretical maximum calls: {int(len(self.transactions).bit_length())}")

    def display_time_complexity_table(self):
        """
        Advanced Feature: Display time complexity analysis in tabular format
        """
        print("\n" + "=" * 100)
        print("TIME COMPLEXITY ANALYSIS")
        print("=" * 100)

        print("\n📊 ALGORITHM COMPLEXITY TABLE:")
        print("-" * 100)
        print(f"{'Algorithm':<25} {'Best Case':<20} {'Average Case':<20} {'Worst Case':<20} {'Space':<15}")
        print("-" * 100)

        algorithms = [
            ("Merge Sort", "O(n log n)", "O(n log n)", "O(n log n)", "O(n)"),
            ("Binary Search", "O(1)", "O(log n)", "O(log n)", "O(1)*"),
            ("Linear Search", "O(1)", "O(n)", "O(n)", "O(1)"),
            ("Quick Sort", "O(n log n)", "O(n log n)", "O(n²)", "O(log n)"),
        ]

        for algo, best, avg, worst, space in algorithms:
            print(f"{algo:<25} {best:<20} {avg:<20} {worst:<20} {space:<15}")

        print("-" * 100)
        print("* Binary Search requires O(log n) space for recursive implementation")
        print("\n📈 COMPARISON FOR N = {} ELEMENTS:".format(len(self.transactions)))
        print("-" * 100)

        n = len(self.transactions)
        import math

        print(f"{'Algorithm':<25} {'Operations':<20} {'Time Estimate':<20}")
        print("-" * 100)

        # Merge Sort
        merge_ops = n * math.log2(n)
        print(f"{'Merge Sort':<25} {int(merge_ops):<20} {'O(n log n)':<20}")

        # Binary Search
        binary_ops = math.log2(n)
        print(f"{'Binary Search':<25} {int(binary_ops):<20} {'O(log n)':<20}")

        # Linear Search
        print(f"{'Linear Search':<25} {n:<20} {'O(n)':<20}")

        print("=" * 100)
        print("✓ Divide and Conquer algorithms significantly reduce complexity:")
        print(f"  • Merge Sort: {int(merge_ops)} operations vs {n * n} for naive sort")
        print(f"  • Binary Search: {int(binary_ops)} operations vs {n} for linear search")


def main():
    """
    Main menu-driven program
    """
    system = TransactionSystem()

    # Load sample data
    system.load_sample_data()

    print("\n" + "=" * 100)
    print("       TRANSACTION MANAGEMENT SYSTEM - DIVIDE AND CONQUER")
    print("       Merge Sort | Binary Search | Linear Search")
    print("=" * 100)

    while True:
        print("\n" + "=" * 100)
        print("MAIN MENU")
        print("=" * 100)
        print("MANDATORY FEATURES:")
        print("1. Display All Transactions")
        print("2. Sort Transactions using Merge Sort (Divide & Conquer)")
        print("3. Search Transaction using Binary Search (Divide & Conquer)")
        print("4. Search Transaction using Linear Search (for comparison)")
        print("\nADVANCED FEATURES (Optional):")
        print("5. Insert Transaction Dynamically")
        print("6. Sort by Amount using Merge Sort")
        print("7. Display Recursive Calls Count")
        print("8. Display Time Complexity Analysis")
        print("\n9. Performance Comparison")
        print("0. Exit")
        print("=" * 100)

        try:
            choice = input("\nEnter your choice (0-9): ").strip()

            if choice == '0':
                print("\n✓ Thank you for using the Transaction Management System!")
                break

            elif choice == '1':
                system.display_all_transactions("ALL TRANSACTIONS")

            elif choice == '2':
                system.sort_transactions_by_id()

            elif choice == '3':
                try:
                    search_id = int(input("Enter Transaction ID to search: "))
                    system.search_transaction_binary(search_id)
                except ValueError:
                    print("❌ Please enter a valid integer ID")

            elif choice == '4':
                try:
                    search_id = int(input("Enter Transaction ID to search: "))
                    system.linear_search(search_id)
                except ValueError:
                    print("❌ Please enter a valid integer ID")

            elif choice == '5':
                system.insert_transaction_dynamic()

            elif choice == '6':
                system.sort_by_amount()

            elif choice == '7':
                system.display_recursive_calls_count()

            elif choice == '8':
                system.display_time_complexity_table()

            elif choice == '9':
                system.compare_performance()

            else:
                print("❌ Invalid choice. Please enter a number between 0 and 9.")

        except KeyboardInterrupt:
            print("\n\n✓ Program terminated by user")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()