# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Alexander Brittain
# Project demonstrating a binary search tree
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Libraries
import csv, time, random

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Node class
class Node:
    # Constructor
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    # Method to display a node and the value it holds as a string
    def __repr__(self):
        return f"Node({self.value})"

# Binary Search Tree class
class BinarySearchTree:
    # Constructor
    def __init__(self):
        self.root = None

    # Method to insert a value into the tree
    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            # Call the recursive insert method to find the correct position
            self._insert_rec(self.root, value)

    # Recursive method to insert a value into the tree
    def _insert_rec(self, current, value):
        # If the value is less than the current node's value, go left
        if value < current.value:
            if current.left is None:
                current.left = Node(value)
            else:
                self._insert_rec(current.left, value)

        # If the value is greater than the current node's value, go right
        elif value > current.value:
            if current.right is None:
                current.right = Node(value)
            else:
                self._insert_rec(current.right, value)

        else:
            print("Value already exists in the tree.")

    # Method to delete a nodee from the tree while keeping the tree balanced
    def delete(self, value):
        self.root = self._delete_rec(self.root, value)

    # Recursive method to delete a node from the tree
    def _delete_rec(self, current, value):
        # If the tree is empty - Base Case
        if current is None:
            return current

        # Lesser values go left
        if value < current.value:
            current.left = self._delete_rec(current.left, value)
        # Greater values go right
        elif value > current.value:
            current.right = self._delete_rec(current.right, value)
        else:
            # Case 1: No child or one child
            if current.left is None:
                # Replace the node with its right child
                return current.right
            elif current.right is None:
                # Replace the node with its left child
                return current.left

            # Case 2: Two children
            current.value = self._find_min(current.right).value
            # Delete the inorder successor
            current.right = self._delete_rec(current.right, current.value)

        return current

    # Method to find the minimum value node in the tree
    def _find_min(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    # Method to find the maximum value node in the tree - the rightmost node
    def maximum(self):
        if self.root is None:
            return None
        else:
            return self._maximum_rec(self.root)

    # Recursive method to find the maximum value node in the tree
    def _maximum_rec(self, node):
        current = node
        while current.right is not None:
            current = current.right
        return current.value

    # Method to traverse the tree in a specific order - default to inorder traversal
    def traverse(self, order="inorder"):
        if order == "inorder":
            return self._inorder(self.root)
        elif order == "preorder":
            return self._preorder(self.root)
        elif order == "postorder":
            return self._postorder(self.root)
        else:
            raise ValueError("Invalid traversal order. Choose 'inorder', 'preorder', or 'postorder'.")

    # Recursive method for inorder traversal
    def _inorder(self, node):
        result = []
        if node:
            result += self._inorder(node.left)
            result.append(node.value)
            result += self._inorder(node.right)
        return result

    # Recursive method for preorder traversal
    def _preorder(self, node):
        result = []
        if node:
            result.append(node.value)
            result += self._preorder(node.left)
            result += self._preorder(node.right)
        return result

    # Recursive method for postorder traversal
    def _postorder(self, node):
        result = []
        if node:
            result += self._postorder(node.left)
            result += self._postorder(node.right)
            result.append(node.value)
        return result

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Function to read the csv files and return a list of integers, ignoring the header
def read_csv(filename):
    # Initialize an empty list to store the integers
    integers = []
    # Open the CSV file
    with open(filename, newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            integers.append(int(row[0]))  # Assuming the integers are in the first column
    return integers

# Function to shuffle a given list of integers
def shuffle_array(array):
    random.shuffle(array)
    return array

# Function to measure time performance of another function
def measure_time(func, *args, **kwargs):
    # Record the start time
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    # Record the end time
    end_time = time.perf_counter()
    # Calculate the execution time
    execution_time = end_time - start_time
    return execution_time

# Function to write performance results to a CSV file
def save_performance_to_csv(results, filename="BSTperformance_results.csv"):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Write headers if the file is empty
        file.seek(0, 2)  # Move to the end of the file
        if file.tell() == 0:
            writer.writerow(["Size", "Operation", "Time"])
        
        # Write the results
        for result in results:
            writer.writerow(result)

# Function to perform tests on the BST for each operation
def test_bst_operations(bst, shuffled_integers, size):
    results = []
    
    # Insertion test
    perf_time_insert = measure_time(bst.insert, shuffled_integers)
    results.append([size, "Insert", f"{perf_time_insert:.8f}"])

    # Maximum test (find maximum)
    perf_time_max = measure_time(bst.maximum)
    results.append([size, "Max", f"{perf_time_max:.8f}"])

    # Traversal test (inorder traversal)
    perf_time_traverse = measure_time(bst.traverse)
    results.append([size, "Traverse", f"{perf_time_traverse:.8f}"])

    # Deletion test (delete each element one by one)
    perf_time_delete = measure_time(delete_all_nodes, bst)
    results.append([size, "Delete", f"{perf_time_delete:.8f}"])

    return results

# Helper function to delete all nodes
def delete_all_nodes(bst):
    while bst.root is not None:
        bst.delete(bst.root.value)

# Main function to run the tests for different sizes
def run_tests():
    test_files = {
        100: "Binary Search Tree Project\\test100.csv",
        1000: "Binary Search Tree Project\\test1000.csv",
        10000: "Binary Search Tree Project\\test10000.csv",
        100000: "Binary Search Tree Project\\test100000.csv"
    }

    # Initialize an empty list to store all results
    all_results = []

    # Loop through each test file and size
    for size, test_file in test_files.items():
        integers = read_csv(test_file)
        shuffled_integers = shuffle_array(integers)

        # Create a BST and run the operations
        bst = BinarySearchTree()
        results = test_bst_operations(bst, shuffled_integers, size)

        # Add the results to the all_results list
        all_results.extend(results)

    # Save all the results to a CSV file
    save_performance_to_csv(all_results)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

if __name__ == "__main__":
    run_tests()