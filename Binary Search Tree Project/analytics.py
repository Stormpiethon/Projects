# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Alexander Brittain
# Analytics of the binary search tree project
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Libraries
import csv
import matplotlib.pyplot as plt
import numpy as np

# Function to read the CSV file and organize the results
def read_performance_data(file_path):
    # Dictionary to hold the data, structured by test size and operation
    performance_data = {
        '100': {'insert': [], 'delete': [], 'traverse': [], 'maximum': []},
        '1000': {'insert': [], 'delete': [], 'traverse': [], 'maximum': []},
        '10000': {'insert': [], 'delete': [], 'traverse': [], 'maximum': []},
        '100000': {'insert': [], 'delete': [], 'traverse': [], 'maximum': []}
    }

    # Read the CSV file
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        # Skip the header line
        next(csv_reader)  

        for row in csv_reader:
            size, operation, perf_time = row[0], row[1], float(row[2])

            # Normalize the operation name to lowercase and strip any extra spaces
            operation = operation.strip().lower()

            # Handle variations in operation names (e.g., 'max' and 'maximum')
            if operation == 'max':
                operation = 'maximum'

            # Ensure the size and operation are valid
            if size in performance_data and operation in performance_data[size]:
                performance_data[size][operation].append(perf_time)

    # Calculate average performance for each operation at each test size
    averages = {}
    for size, operations in performance_data.items():
        averages[size] = {op: np.mean(times) for op, times in operations.items()}

    return averages

# Function to plot the bar graph
def plot_performance_data(averages):
    # Test sizes and operations
    test_sizes = ['100', '1000', '10000', '100000']
    operations = ['insert', 'delete', 'traverse', 'maximum']

    # Prepare data for plotting
    data = {operation: [averages[size][operation] for size in test_sizes] for operation in operations}

    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # The x positions for the groups
    x = np.arange(len(test_sizes))

    # Bar width
    width = 0.2

    # Plot each operation's data as a bar
    bars = {}
    for i, operation in enumerate(operations):
        bars[operation] = ax.bar(x + i * width, data[operation], width, label=operation.capitalize())

    # Set labels and title
    ax.set_xlabel('Test Size')
    ax.set_ylabel('Average Time (seconds)')
    ax.set_title('Performance Data for Different Operations')
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(test_sizes)
    ax.legend()

    # Adding vertical labels above the bars
    for i, operation in enumerate(operations):
        for j, bar in enumerate(bars[operation]):
            yval = bar.get_height()  # Get the height of each bar
            ax.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.8f}', ha='center', va='bottom', rotation=90, fontsize=9)

    # Show the plot
    plt.tight_layout()
    plt.show()

# Example usage
# file_path = 'BSTperformance_results.csv'
file_path = 'AVLperformance_results.csv' 
averages = read_performance_data(file_path)
plot_performance_data(averages)
