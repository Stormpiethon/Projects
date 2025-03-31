# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Alexander Brittain
# Sorting algorithm project for data structures and algorithms
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import time

# Node classs for linked list
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# Linked list class
class LinkedList:
    def __init__(self):
        self.head = None

    # Add a new node to the end of the linked list
    def append(self, data):
        new_node = Node(data)
        
        if self.head is None:
            self.head = new_node
            return
        
        # Traverse to the end of the list
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
    
    # Display the linked list
    def display(self):
        elements = []
        current = self.head
        while current:
            elements.append(str(current.data))
            current = current.next
        return "->".join(elements)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# ***** QUICK SORT ******
# Find the tail of the linked list
def get_tail(head):
    current = head
    while current and current.next:
        current = current.next
    return current

# Split the linked list into two halves
def partition(start, end):
    if start == end or start == None:
        return start
    
    # Initialize pivot_prev and current node
    pivot_prev = start
    curr = start
    pivot = end.data
    
    # Iterate until the node points to the end of the list
    while start != end:
        if start.data <= pivot:
            pivot_prev = curr
            temp = curr.data
            curr.data = start.data
            start.data = temp
            curr = curr.next
        start = start.next
    
    # Swap the data
    temp = curr.data
    curr.data = pivot
    end.data = temp
    
    return pivot_prev

# Perform quick sort on the linked list recursively
def quick_sort_recur(start, end):
    if start == None or start == end or start == end.next:
        return
    
    # Partition the list and obtain the pivot node
    pivot_prev = partition(start, end)
    quick_sort_recur(start, pivot_prev)
    
    # Compare the pivot node with the start
    if pivot_prev != None and pivot_prev == start:
        quick_sort_recur(pivot_prev.next, end)
    elif pivot_prev != None and pivot_prev.next != None:
        quick_sort_recur(pivot_prev.next, end)

# Primary function to sort the linked list using quick sort
def quick_sort(linked_list1):
    head = linked_list1.head
    tail = get_tail(head)
    quick_sort_recur(head, tail)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# ***** MERGE SORT ******
def merge_sort(head):
    # Base case - if head is None or only one element
    if head is None or head.next is None:
        return head
    
    # Split the list into two halves
    left_half, right_half = split_list(head)
    
    # Recursively sort both halves
    left = merge_sort(left_half)
    right = merge_sort(right_half)
    
    # Merge the sorted halves
    return merge(left, right)

# Split the linked list into two halves
def split_list(head):
    if head is None or head.next is None:
        return head, None
    
    # Two pointers to traverse the list and find the center
    slow = head
    fast = head.next
    
    # Move the pointers to find the center of the list
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    # Split the list into two halves
    mid = slow.next
    slow.next = None
    return head, mid

# Merge two sorted linked lists
def merge(left, right):
    merged = Node(0)
    current = merged
    
    # Compare elements from both lists and merge them in sorted order
    while left and right:
        if left.data <= right.data:
            current.next = left
            left = left.next
        else:
            current.next = right
            right = right.next
        current = current.next
    
    # Append any remaining elements from the left or right list
    if left:
        current.next = left
    if right:
        current.next = right
    
    return merged.next
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# ***** BUBBLE SORT ******
def bubble_sort(linked_list):
    if linked_list.head is None:
        return
    
    # Initialize pointers for the start and end of the list
    end = None
    while True:
        swapped = False
        current = linked_list.head
        
        # Traverse the list and swap adjacent elements if they are in the wrong order
        while current.next != end:
            if current.data > current.next.data:
                current.data, current.next.data = current.next.data, current.data
                swapped = True
            current = current.next
        
        # If no swaps were made in this pass, the list is sorted
        end = current
        if not swapped:
            break
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# Function to time the sorting algorithms
def time_sort(sort_func, linked_list):
    start_time = time.perf_counter()
    if sort_func.__name__ == 'quick_sort':
        sort_func(linked_list)  # Quick sort modifies the list in place
    elif sort_func.__name__ == 'bubble_sort':
        sort_func(linked_list)  # Bubble sort modifies the list in place
    else:
        linked_list.head = sort_func(linked_list.head)  # Merge sort returns new head
    end_time = time.perf_counter()
    return end_time - start_time

# Function to save the results to a file
def save_results(algorithm_name, time_taken, size):
    with open('sorting_results.txt', 'a') as file:
        file.write(f"{algorithm_name[0]},{time_taken:.6f},{size}\n")

# Function to run sorting tests and output the performance data
def run_sorting_tests():
    test_sizes = {
        "10 elements": test_data_10,
        "100 elements": test_data_100,
        "1000 elements": test_data_1000
    }
    
    print("\nSorting Algorithm Performance Tests")
    print("=" * 60)
    
    for size_name, data in test_sizes.items():
        print(f"\nTesting {size_name}")
        print("-" * 30)
        
        # Create linked lists for each sorting algorithm
        list_for_quick = LinkedList()
        list_for_merge = LinkedList()
        list_for_bubble = LinkedList()
        
        # Populate the linked lists with the test data
        for num in data:
            list_for_quick.append(num)
            list_for_merge.append(num)
            list_for_bubble.append(num)

        # Display the unsorted lists
        if size_name == "10 elements":
            print("\nUnsorted List:")
            print(list_for_quick.display())
            print("\nUnsorted List:")
            print(list_for_merge.display())
            print("\nUnsorted List:")
            print(list_for_bubble.display())
        
        # Time the sorting algorithms
        quick_time = time_sort(quick_sort, list_for_quick)
        merge_time = time_sort(merge_sort, list_for_merge)
        bubble_time = time_sort(bubble_sort, list_for_bubble)

        # Save results to file
        save_results("Quick", quick_time, size_name)
        save_results("Merge", merge_time, size_name)
        save_results("Bubble", bubble_time, size_name)
        
        # Display results for 10 elements
        if size_name == "10 elements":
            print("\nQuick Sort Result:")
            print(list_for_quick.display())
            print("\nMerge Sort Result:")
            print(list_for_merge.display())
            print("\nBubble Sort Result:")
            print(list_for_bubble.display())
            
        # Display the performance information of each algorithm
        print(f"\nQuick Sort Time: {quick_time:.6f} seconds")
        print(f"Merge Sort Time: {merge_time:.6f} seconds")
        print(f"Bubble Sort Time: {bubble_time:.6f} seconds")


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

if __name__ == "__main__":
    
    test_data_10 = [12, 54, 9, 67, 34, 88, 23, 19, 41, 76]

    test_data_100 = [
        35, 83, 91, 10, 17, 60, 89, 100, 29, 8, 41, 46, 
        90, 80, 53, 7, 61, 72, 38, 74, 84, 50, 57, 65, 
        49, 99, 70, 22, 69, 77, 97, 4, 79, 54, 55, 6, 14, 
        31, 20, 59, 23, 45, 68, 78, 48, 44, 43, 47, 86, 
        73, 93, 88, 81, 1, 82, 51, 42, 66, 33, 92, 75, 21, 
        37, 58, 5, 2, 71, 98, 26, 36, 16, 85, 18, 24, 34, 
        11, 13, 28, 76, 94, 32, 67, 62, 3, 63, 9, 30, 39, 
        96, 19, 40, 52, 56, 87, 25, 12, 15, 27, 64, 95
    ]


    test_data_1000 = [
        846, 572, 114, 535, 413, 67, 929, 212, 840, 831, 
        57, 21, 118, 357, 897, 569, 734, 602, 813, 993, 
        228, 547, 424, 828, 372, 478, 211, 244, 908, 512, 
        954, 56, 831, 656, 343, 333, 973, 688, 669, 788, 
        340, 335, 35, 772, 636, 309, 506, 70, 96, 832, 
        431, 271, 779, 456, 629, 314, 290, 485, 855, 559, 
        134, 326, 971, 232, 259, 730, 363, 27, 806, 704, 
        456, 220, 221, 732, 873, 207, 904, 116, 624, 890, 
        545, 762, 471, 198, 446, 44, 389, 801, 592, 131, 
        274, 463, 328, 688, 973, 747, 928, 696, 944, 923, 
        282, 755, 208, 682, 443, 334, 59, 265, 212, 720, 
        40, 353, 317, 348, 34, 783, 858, 157, 588, 999, 
        973, 768, 899, 187, 819, 598, 657, 774, 566, 313, 
        672, 905, 780, 710, 211, 650, 242, 492, 121, 301, 
        654, 334, 869, 352, 544, 465, 17, 924, 329, 42, 
        202, 130, 660, 737, 436, 500, 290, 284, 347, 424, 
        18, 402, 494, 895, 554, 647, 593, 36, 497, 741, 
        983, 858, 358, 998, 936, 496, 725, 314, 937, 523, 
        607, 597, 296, 461, 19, 738, 506, 678, 163, 989, 
        42, 496, 507, 604, 833, 875, 996, 885, 193, 457, 
        80, 439, 349, 351, 277, 520, 757, 317, 246, 170, 
        974, 735, 319, 871, 204, 231, 318, 908, 297, 249, 
        449, 80, 762, 78, 596, 215, 843, 659, 59, 594, 
        268, 19, 137, 332, 878, 452, 823, 755, 986, 541, 
        217, 743, 924, 332, 701, 243, 446, 682, 199, 283, 
        482, 444, 767, 485, 209, 245, 524, 513, 552, 177, 
        825, 438, 292, 874, 317, 931, 43, 576, 449, 288, 
        915, 702, 432, 340, 100, 486, 747, 238, 425, 646, 
        79, 475, 756, 257, 132, 784, 283, 937, 687, 278, 
        220, 117, 927, 763, 336, 175, 622, 199, 111, 510, 
        637, 84, 643, 576, 526, 45, 347, 359, 159, 601, 
        486, 741, 246, 497, 435, 14, 938, 611, 771, 598, 
        762, 474, 874, 631, 428, 314, 467, 387, 804, 141
    ]

    # Run the sorting tests
    run_sorting_tests()

