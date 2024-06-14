import scipy.stats as stats

# Parameters
mu = 2
sigma = 2
x = 1

# Calculate the CDF
cdf_value = stats.norm.cdf(x, loc=mu, scale=sigma)
print(1-cdf_value)
