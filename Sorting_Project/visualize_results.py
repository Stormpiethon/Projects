# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Alexander Brittain
# Visualize the results of sorting algorithms
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import matplotlib.pyplot as plt
import pandas as pd

# Read and process the data
def process_sorting_data(filename):
    algorithms = []
    times = []
    sizes = []
    
    # Read the data from the file
    with open(filename, 'r') as file:
        for line in file:
            algo, time, size = line.strip().split(',')
            algorithms.append(algo)
            times.append(float(time))
            sizes.append(size)
    
    # Create a DataFrame for the data and store the lists in it
    return pd.DataFrame({
        'Algorithm': algorithms,
        'Time': times,
        'Size': sizes
    })

# Create visualization
def create_performance_graph(data):
    plt.figure(figsize=(12, 6))
    
    # Plot for each algorithm
    for algo in ['Q', 'M', 'B']:
        algo_data = data[data['Algorithm'] == algo]
        
        # Calculate mean time for each size
        mean_times = algo_data.groupby('Size')['Time'].mean()
        
        # Plot with appropriate labels
        label = 'Quick Sort' if algo == 'Q' else 'Merge Sort' if algo == 'M' else 'Bubble Sort'
        plt.plot(range(len(mean_times)), mean_times.values, marker='o', label=label)
    
    # Customize the plot
    plt.title('Sorting Algorithm Performance Comparison', fontsize=14)
    plt.xlabel('Input Size', fontsize=12)
    plt.ylabel('Time (seconds)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    # Set x-axis labels
    plt.xticks(range(3), ['10 elements', '100 elements', '1000 elements'])
    
    # Display the plot
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Read and visualize the data
    data = process_sorting_data('sorting_results.txt')
    create_performance_graph(data)
