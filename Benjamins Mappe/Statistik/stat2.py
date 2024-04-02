from scipy.stats import norm

alpha = 0.05
X = norm(9,2/3)


print(X.ppf(0.05))
