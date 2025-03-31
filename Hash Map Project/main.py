# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Alexander Brittain
# Program to demonstrate a hash map for a conference registration
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import json, time, csv

# Hash Table data structure
class HashTable:
    # Initialize the hash table with a given number of buckets
    def __init__(self, num_buckets):
        self.num_buckets = num_buckets
        # Each bucket is a list for separate chaining
        self.table = [[] for _ in range(num_buckets)]

    # Simple hash function: compute the hash of the key and map it to a bucket
    def hash_function(self, key):
        return hash(key) % self.num_buckets

    # Method to insert a key-value pair into the hash table
    def insert(self, key, value):
        bucket_index = self.hash_function(key)
        # Check for existing keys and update if found
        for i, (existing_key, _) in enumerate(self.table[bucket_index]):
            if existing_key == key:
                self.table[bucket_index][i] = (key, value)
                return
        # Otherwise, append the new key-value pair
        self.table[bucket_index].append((key, value))

    # Method to retrieve a value based on a key
    def retrieve(self, key):
        bucket_index = self.hash_function(key)
        for existing_key, value in self.table[bucket_index]:
            if existing_key == key:
                return value
        
        # Return None if the key is not found
        return None  

    # Method to display the hash table to the console
    def print_table(self):
        all_items = []
        # Flatten the buckets
        for bucket in self.table:
            all_items.extend(bucket)  
        # Sort by key (e.g., alphabetical order)
        for key, value in sorted(all_items, key=lambda x: x[0]):
            print(f"{key}: {value}")

    # Function to print the hash tables individually so they can be viewed in the terminal
    def display_table_10(hash_table):
        print("Displaying 10-bucket hash table:")
        print_table(hash_table)

    def display_table_100(hash_table):
        print("Displaying 100-bucket hash table:")
        print_table(hash_table)

    def display_table_1000(hash_table):
        print("Displaying 1000-bucket hash table:")
        print_table(hash_table)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Function to load dataset
def load_dataset(file_name):
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        return []


# Measure runtime of a function with flexible arguments
def measure_runtime(func, *args, **kwargs):
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    return result, end_time - start_time


# Measure runtime of sorting entries
def measure_sort_runtime(hash_table):
    # Measure the time taken to sort the entries in the hash table
    def sort_entries():
        # Empty list to store sorted entries
        all_items = []
        # Iterate through the hash table buckets
        for bucket in hash_table.table:
            # Append each entry in the bucket to the list
            all_items.extend(bucket)
        # Sort the list of entries based on the key
        sorted_items = sorted(all_items, key=lambda x: x[0])
        return sorted_items

    # Store the time taken to sort the entries for return
    _, sort_time = measure_runtime(sort_entries)
    print(f"Sorting complete. Time taken: {sort_time:.6f} seconds")
    return sort_time


# Function to save performance data to a CSV file
def save_performance_data(file_name, performance_data):
    # Check if the file exists
    file_exists = False
    try:
        file_exists = open(file_name).close() is None
    except FileNotFoundError:
        pass

    # Format the data to avoid scientific notation
    formatted_data = [(f"{insert_time:.6f}", f"{sort_time:.6f}", data_set_size)
                      for insert_time, sort_time, data_set_size in performance_data]

    # Save the performance data to a CSV file
    with open(file_name, 'a', newline='') as file:
        writer = csv.writer(file)
        # Write headers if the file doesn't exist
        if not file_exists:
            writer.writerow(['Insert Time (s)', 'Sort Time (s)', 'Data Set Size'])
        writer.writerows(formatted_data)
    print(f"Performance data saved to {file_name}")
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Main execution
if __name__ == "__main__":
    # Load datasets
    dataset_10 = load_dataset("Python\Hash Map Project\\10_entries_realistic.json")
    dataset_100 = load_dataset("Python\Hash Map Project\\100_entries_realistic.json")
    dataset_1000 = load_dataset("Python\Hash Map Project\\1000_entries_realistic.json")

    # Create and populate hash tables
    hash_table_10 = HashTable(10)
    hash_table_100 = HashTable(100)
    hash_table_1000 = HashTable(1000)

    # Measure insertion times and display
    _, insert_time_10 = measure_runtime(
        lambda: [hash_table_10.insert(
            f"{entry['name']} ({entry['state']})", entry) for entry in dataset_10]
    )
    print(f"Insert time for 10 buckets: {insert_time_10:.6f} seconds")

    _, insert_time_100 = measure_runtime(
        lambda: [hash_table_100.insert(
            f"{entry['name']} ({entry['state']})", entry) for entry in dataset_100]
    )
    print(f"Insert time for 100 buckets: {insert_time_100:.6f} seconds")

    _, insert_time_1000 = measure_runtime(
        lambda: [hash_table_1000.insert(
            f"{entry['name']} ({entry['state']})", entry) for entry in dataset_1000]
    )
    print(f"Insert time for 1000 buckets: {insert_time_1000:.6f} seconds")

    # Measure sorting time
    sort_time_10 = measure_sort_runtime(hash_table_10)
    sort_time_100 = measure_sort_runtime(hash_table_100)
    sort_time_1000 = measure_sort_runtime(hash_table_1000)

    # Uncomment these lines to display tables separately
    # hash_table_10.print_table()
    hash_table_100.print_table()
    # hash_table_1000.print_table()

    # Collect performance data
    performance_data = [
        (insert_time_10, sort_time_10, len(dataset_10)),
        (insert_time_100, sort_time_100, len(dataset_100)),
        (insert_time_1000, sort_time_1000, len(dataset_1000))
    ]

    # Save performance data to file
    save_performance_data("performance_data.txt", performance_data)
