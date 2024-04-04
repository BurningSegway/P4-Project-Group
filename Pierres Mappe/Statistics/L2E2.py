import scipy
from scipy.stats import norm
import matplotlib as plt

alpha = 0.05
X = norm(9,2/3)

print(X.ppf(0.05))