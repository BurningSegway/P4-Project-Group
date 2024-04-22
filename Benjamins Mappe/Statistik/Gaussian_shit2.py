import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Set the mean and variance
mean = 2
variance = 16

# Generate 30 data points from a Gaussian distribution
n = 1000
data = np.random.normal(mean, np.sqrt(variance), n)

# Sort the data
sorted_data = np.sort(data)

# Calculate the empirical cumulative density function (CDF)
empirical_cdf = np.linspace(0, 1, n)

# Calculate the Gaussian cumulative distribution function (CDF)
gaussian_cdf = norm.cdf(sorted_data, mean, np.sqrt(variance))

# Find the value corresponding to the 0.2-quantile in the empirical CDF
quantile_02_empirical = sorted_data[np.argmax(empirical_cdf >= 0.2)]

# Find the value corresponding to the 0.2-quantile in the Gaussian CDF
quantile_02_gaussian = norm.ppf(0.2, mean, np.sqrt(variance))

# Plot the empirical and Gaussian CDFs
plt.figure(figsize=(10, 5))
plt.plot(sorted_data, empirical_cdf, label='Empirical CDF', color='blue')
plt.plot(sorted_data, gaussian_cdf, label='Gaussian CDF', color='red')
plt.axvline(quantile_02_empirical, color='blue', linestyle='--', label='0.2-Quantile (Empirical)')
plt.axvline(quantile_02_gaussian, color='red', linestyle='--', label='0.2-Quantile (Gaussian)')
plt.title('Empirical vs Gaussian CDF')
plt.xlabel('Value')
plt.ylabel('Cumulative Probability')
plt.legend()
plt.grid(True)
plt.show()