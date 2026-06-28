import time  # <-- ADD THIS!
TOMBSTONE = object()

# Part 1: Medicine Class
class Medicine:
    def __init__(self, id, name, med_type, price, quantity):
        self.id = id
        self.name = name
        self.med_type = med_type
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"ID:{self.id},| Name:{self.name},| Med_Type:{self.med_type},| Price:{self.price}, | quantity:{self.quantity}"


# Part 2: Hash Table
class HashTable:
    def __init__(self, size=11):
        self.size = size
        self.buckets = [None] * size
        self.count = 0

    def _hash(self, key):
        return key % self.size

    def insert(self, medicine):
        key = medicine.id
        index = self._hash(key)
        first_tombstone = -1

        for _ in range(self.size):
            bucket = self.buckets[index]

            if bucket is None:
                if first_tombstone != -1:
                    self.buckets[first_tombstone] = medicine
                else:
                    self.buckets[index] = medicine
                self.count = self.count + 1
                return True

            if bucket is TOMBSTONE:
                if first_tombstone == -1:
                    first_tombstone = index
                index = (index + 1) % self.size
                continue

            if bucket.id == key:
                self.buckets[index] = medicine
                return True

            index = (index + 1) % self.size

        if first_tombstone != -1:
            self.buckets[first_tombstone] = medicine
            self.count = self.count + 1
            return True

        print("Error: Hash table is completely full")
        return False

    def search(self, key):
        index = self._hash(key)
        for _ in range(self.size):
            bucket = self.buckets[index]
            if bucket is None:
                return None
            if bucket is TOMBSTONE:
                index = (index + 1) % self.size
                continue
            if bucket.id == key:
                return bucket
            index = (index + 1) % self.size
        return None

    def delete(self, key):
        index = self._hash(key)
        for _ in range(self.size):
            bucket = self.buckets[index]
            if bucket is None:
                return False
            if bucket is not TOMBSTONE and bucket.id == key:
                self.buckets[index] = TOMBSTONE
                self.count = self.count - 1
                return True
            index = (index + 1) % self.size  # <-- FIXED: changed & to %
        return False

    def display(self):
        print("\n" + "=" * 70)
        print("Pharmacy Inventory (Hash Table)".center(70))
        print("=" * 70)
        print(f"{'Bucket':<8} {'ID':<6} {'Name':<15} {'Type':<15} {'Price':<10} {'Stock':<6}")  # <-- FIXED formatting
        print("-" * 70)

        found = False
        for i, bucket in enumerate(self.buckets):
            if bucket is not None and bucket is not TOMBSTONE:
                print(f"{i:<8} {bucket.id:<6} {bucket.name:<15} {bucket.med_type:<15} ${bucket.price:<9.2f} {bucket.quantity:<6}")
                found = True
        if not found:
            print("(Inventory is empty)".center(70))
        print("=" * 70 + "\n")


# Part 3: Array Operations
def insert_into_array(arr, medicine):  # <-- FIXED: renamed from insert_inti_array
    arr.append(medicine)

def search_array(arr, key):
    for medicine in arr:
        if medicine.id == key:
            return medicine
    return None  # <-- FIXED: moved outside the loop

def display_array(arr):
    print("\n" + "=" * 70)
    print("Plain Array Inventory (Reference)".center(70))
    print("=" * 70)
    print(f"{'ID':<6} {'Name':<15} {'Type':<15} {'Price':<10} {'Stock':<6}")  # <-- FIXED formatting
    print("-" * 70)

    if not arr:
        print("(Array is empty)".center(70))
    else:
        for medicine in arr:
            print(f"{medicine.id:<6} {medicine.name:<15} {medicine.med_type:<15} ${medicine.price:<9.2f} {medicine.quantity:<6}")
    print("=" * 70 + "\n")


# Part 4: Performance Comparison
def performance_comparison(hash_table, plain_array, test_keys):
    print("\n" + "=" * 70)
    print("Performance Comparison: Hash Table vs Plain Array".center(70))
    print("=" * 70)

    iterations = 10000

    for key in test_keys:
        # Measure Hash Table
        start = time.perf_counter()
        for _ in range(iterations):
            hash_table.search(key)
        end = time.perf_counter()
        hash_time = (end - start) * 1e6

        # Measure Plain Array
        start = time.perf_counter()
        for _ in range(iterations):
            search_array(plain_array, key)
        end = time.perf_counter()
        array_time = (end - start) * 1e6

        exists = hash_table.search(key) is not None
        status = "EXISTS" if exists else "DOES NOT EXIST"

        print(f"\nSearching for ID {key} ({status}):")
        print(f"  Hash Table Time: {hash_time:.2f} µs (over {iterations} searches)")
        print(f"  Plain Array Time: {array_time:.2f} µs (over {iterations} searches)")

        if hash_time < array_time:
            print(f"  ✅ Hash Table is {array_time / hash_time:.2f}x faster")
        else:
            print(f"  ✅ Plain Array is {hash_time / array_time:.2f}x faster")

    print("\nCONCLUSION:")
    print("- Hash Table uses O(1) average time (direct indexing + probing).")
    print("- Plain Array uses O(n) linear search (scans every element).")
    print("- For existing keys, both find the record, but Hash Table jumps directly to the bucket.")
    print("- For NON-EXISTING keys, the array must scan ALL elements, making it drastically slower.")
    print("=" * 70 + "\n")


# Part 5: CLI Menu
def cli_menu(hash_table, plain_array):
    while True:
        print("\n" + "=" * 40)
        print("   PHARMACY INVENTORY SYSTEM")
        print("=" * 40)
        print("1. Display All Medicines (Hash Table)")
        print("2. Display All Medicines (Plain Array) - reference")
        print("3. Insert a New Medicine")
        print("4. Search for a Medicine by ID")
        print("5. Delete a Medicine by ID (Optional)")
        print("6. Run Performance Comparison (Hash vs Array)")
        print("7. Exit")
        print("=" * 40)

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            hash_table.display()
        elif choice == "2":
            display_array(plain_array)
        elif choice == "3":
            print("\n--- Insert New Medicine ---")
            try:
                med_id = int(input("Enter ID (integer): "))
                name = input("Enter Name: ").strip()
                med_type = input("Enter Type (Tablets/Syrup/Supplements): ").strip()
                price = float(input("Enter Price: "))
                quantity = int(input("Enter Quantity: "))

                new_med = Medicine(med_id, name, med_type, price, quantity)
                hash_table.insert(new_med)
                insert_into_array(plain_array, new_med)
                print(f"✅ Medicine '{name}' inserted successfully into both structures!")
            except ValueError:
                print("❌ Invalid input! Please enter correct data types.")
        elif choice == "4":
            print("\n--- Search Medicine ---")
            try:
                med_id = int(input("Enter ID to search: "))
                found = hash_table.search(med_id)
                if found:
                    print(f"✅ Found: {found}")
                else:
                    print(f"❌ Medicine with ID {med_id} not found.")
            except ValueError:
                print("❌ Invalid ID format.")
        elif choice == "5":
            print("\n--- Delete Medicine (Optional) ---")
            try:
                med_id = int(input("Enter ID to delete: "))
                deleted = hash_table.delete(med_id)
                if deleted:
                    for i, med in enumerate(plain_array):
                        if med.id == med_id:
                            plain_array.pop(i)
                            break
                    print(f"✅ Medicine with ID {med_id} deleted successfully!")
                else:
                    print(f"❌ Medicine with ID {med_id} not found.")
            except ValueError:
                print("❌ Invalid ID format.")
        elif choice == "6":
            if plain_array:
                existing_key = plain_array[0].id
            else:
                existing_key = 101
            non_existing_key = 9999
            performance_comparison(hash_table, plain_array, [existing_key, non_existing_key])
        elif choice == "7":
            print("\nExiting Pharmacy Inventory System. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter a number between 1 and 7.")


# Part 6: Main Program
def main():
    pharmacy_table = HashTable(size=11)
    plain_array = []

    sample_medicines = [
        Medicine(101, "Panadol", "Tablets", 5.99, 50),
        Medicine(102, "Amoxicillin", "Tablets", 12.50, 30),
        Medicine(103, "Cough Syrup", "Syrup", 8.75, 20),
        Medicine(104, "Vitamin C", "Supplements", 15.20, 100),
        Medicine(105, "Ibuprofen", "Tablets", 9.90, 40),
        Medicine(106, "Zinc Plus", "Supplements", 11.30, 60),  # <-- FIXED: 11.30 not 11
        Medicine(107, "Allergy Relief", "Syrup", 14.00, 25)
    ]

    print("Loading sample medicines into the system...")
    for med in sample_medicines:
        pharmacy_table.insert(med)
        insert_into_array(plain_array, med)  # <-- FIXED: comma, not dot!

    print(f"✅ Loaded {len(sample_medicines)} sample records into both structures.\n")
    pharmacy_table.display()
    cli_menu(pharmacy_table, plain_array)


# Part 6: Run the program
if __name__ == "__main__":  # <-- FIXED: added spaces and double ==
    main()