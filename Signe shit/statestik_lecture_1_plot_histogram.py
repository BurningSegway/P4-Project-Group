#plotting absulute, relative and normalized histogram based on data from file
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Read in the data
data = pd.read_csv("C:/Users/signe/OneDrive - Aalborg Universitet/Skrivebord/Statestik/Starlink_latency.csv")
print(data.keys())

#plottin absolute histogram
plt.hist(data[' latency'], bins=50, color='c')
plt.title('Absolute histogram of latency')
plt.xlabel('latency')
plt.ylabel('Frequency')
plt.show()

# Calculate the weights
weights = np.ones_like(data[' latency']) / 50

# Plotting relative histogram n(i)/n - n is the number of bins
plt.hist(data[' latency'], bins=50, color='c', weights=weights) #density=giver normaliseret histogram 
plt.title('Relative histogram of latency')
plt.xlabel('latency')
plt.ylabel('Relative frequency')
plt.show()

#plotting normalized histogram
plt.hist(data[' latency'], bins=50, color='c', density=True,) #cumulative=True gives it cummulated(sammenlagt)
plt.title('Normalized histogram of latency')
plt.xlabel('latency')
plt.ylabel('Normalized frequency')
plt.show()

#plotting boxplot
plt.boxplot(data[' latency'])
plt.title('Boxplot of latency')
plt.ylabel('latency')
plt.show()




# Create a 2x2 grid of plots
fig, axs = plt.subplots(2, 2, figsize=(10, 10))

# Plotting absolute histogram
axs[0, 0].hist(data[' latency'], bins=50, color='c')
axs[0, 0].set_title('Absolute histogram of latency')
axs[0, 0].set_xlabel('latency')
axs[0, 0].set_ylabel('Frequency')

# Calculate the weights
weights = np.ones_like(data[' latency']) / 50

# Plotting relative histogram n(i)/n - n is the number of bins
axs[0, 1].hist(data[' latency'], bins=50, color='c', weights=weights)
axs[0, 1].set_title('Relative histogram of latency')
axs[0, 1].set_xlabel('latency')
axs[0, 1].set_ylabel('Relative frequency')

# Plotting normalized histogram
axs[1, 0].hist(data[' latency'], bins=50, color='c', density=True)
axs[1, 0].set_title('Normalized histogram of latency')
axs[1, 0].set_xlabel('latency')
axs[1, 0].set_ylabel('Normalized frequency')

# Plotting boxplot
axs[1, 1].boxplot(data[' latency'])
axs[1, 1].set_title('Boxplot of latency')
axs[1, 1].set_ylabel('latency')

# Display the plots
plt.tight_layout()
plt.show()