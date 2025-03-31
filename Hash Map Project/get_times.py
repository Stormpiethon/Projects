# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Alexander Brittain
# Program to take performance data from a CSV file and plot it
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Import pandas and matplotlib to plot performance data
import pandas as pd
import matplotlib.pyplot as plt

# Load performance data from the .txt file (with a CSV-like format)
df = pd.read_csv('performance_data.txt', header=None, names=['Insert Time', 'Sort Time', 'Data Set Size'])

# Convert the columns to numeric values (in case they are read as strings)
df['Insert Time'] = pd.to_numeric(df['Insert Time'], errors='coerce')
df['Sort Time'] = pd.to_numeric(df['Sort Time'], errors='coerce')
df['Data Set Size'] = pd.to_numeric(df['Data Set Size'], errors='coerce')

# Group the data by 'Data Set Size' and calculate the mean for Insert Time and Sort Time
means = df.groupby('Data Set Size').agg({'Insert Time': 'mean', 'Sort Time': 'mean'}).reset_index()

# Set up the plot
plt.figure(figsize=(10, 6))

# Create an x-axis for the three data set sizes (10, 100, 1000) evenly spaced
x = [0, 1, 2]

# Map dataset sizes to the x-axis positions
data_set_sizes = [10, 100, 1000]
position_mapping = dict(zip(data_set_sizes, x))

# Plot Insert Time (shifted slightly to the left)
insert_bars = plt.bar([position_mapping[10], position_mapping[100], position_mapping[1000]], 
                      means['Insert Time'], width=0.3, label='Insert Time', color='b')

# Plot Sort Time (shifted slightly to the right)
sort_bars = plt.bar(
    [pos + 0.3 for pos in [position_mapping[10], position_mapping[100], position_mapping[1000]]], 
    means['Sort Time'], width=0.3, label='Sort Time', color='g')

# Labeling the axes
plt.xlabel('Data Set Size')
plt.ylabel('Time (seconds)')

# Title and legend
plt.title('Performance of Hash Table Operations by Data Set Size')
plt.legend()

# Set the x-ticks to show the actual data set sizes (10, 100, 1000)
plt.xticks([0, 1, 2], data_set_sizes)

# Display the value above each bar for Insert Time
for bar in insert_bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.6f}', ha='center', va='bottom', fontsize=8)

# Display the value above each bar for Sort Time
for bar in sort_bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.6f}', ha='center', va='bottom', fontsize=8)

# Display the plot
plt.tight_layout()
plt.show()

