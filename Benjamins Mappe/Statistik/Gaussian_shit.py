import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Set the mean and variance
mean = 2
variance = 16

# Generate 30 data points from a Gaussian distribution
n = 1000
data = np.random.normal(mean, np.sqrt(variance), n)

# Define the range of x values for the PDF plot
x = np.linspace(mean - 4*np.sqrt(variance), mean + 4*np.sqrt(variance), 100)

# Calculate the Gaussian probability density function (PDF)
pdf = norm.pdf(x, mean, np.sqrt(variance))

# Plot absolute histogram
plt.figure(figsize=(10, 5))
plt.subplot(2, 2, 1)
plt.hist(data, bins=10, color='skyblue', edgecolor='black', alpha=0.7)
plt.title('Absolute Histogram')
plt.xlabel('Value')
plt.ylabel('Frequency')

# Plot relative histogram
plt.subplot(2, 2, 2)
plt.hist(data, bins=10, density=True, color='salmon', edgecolor='black', alpha=0.7)
plt.title('Relative Histogram')
plt.xlabel('Value')
plt.ylabel('Density')

# Plot normalized histogram
plt.subplot(2, 2, 3)
plt.hist(data, bins=10, density=True, color='lightgreen', edgecolor='black', alpha=0.7)
plt.plot(x, pdf, 'r--', linewidth=2)
plt.title('Normalized Histogram with PDF')
plt.xlabel('Value')
plt.ylabel('Density')

# Plot Gaussian PDF
plt.subplot(2, 2, 4)
plt.plot(x, pdf, 'r--', linewidth=2)
plt.title('Gaussian Probability Density Function (PDF)')
plt.xlabel('Value')
plt.ylabel('Density')

plt.tight_layout()
plt.show()