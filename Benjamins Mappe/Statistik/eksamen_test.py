import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from scipy.stats import norm, binom, t
from Stats_funcs import mean_csv,plt_Hist_norm,plt_PFD_GAUS,binomial_pmf, plt_Hist_relative, plt_Hist, sum_function, Z_score, T_Test, estimate_coef


#execution_data = [62, 59, 48, 52, 55, 47, 47, 53]

    #Find gaussiske værdier
#mean, variance, std_dev = mean_csv(execution_data)
#print('mean = ', mean, 'variance = ', variance, 'std_dev = ', std_dev)




#x_i = [0.41, 0.46, 0.44, 0.47, 0.42, 0.39, 0.41, 0.44, 0.43, 0.44]
#y_i = [1850, 2620, 2340, 2690, 2160, 1760, 2500, 2750, 2730, 3120]
x_i = [0.1, 0.2, 0.5, 0.7, 0.9]
y_i = [0.43, 0.52, 0.13, 1.73, 2.01]

np_x_i = np.asarray(x_i, dtype=np.float32)
np_y_i = np.asarray(y_i, dtype=np.float32)

b_0, b_1 = estimate_coef(np_x_i, np_y_i)
print('b_o =',b_0, 'b_1 =', b_1)
x_speccific = 1
print('Result in x=', x_speccific, 'is y=', b_0+b_1*x_speccific)
y = []
for i in range(len(x_i)):
    y_temp = b_0 + b_1 * x_i[i]
    y.append(y_temp)

plt.scatter(x_i, y_i)
plt.plot(x_i, y)
plt.show()
opgave = False
if opgave == True:
    error_temp = 0
    error = []
    n=10
    for i in range(len(x_i)):
        error_temp = (y_i[i]-(b_0+b_1*x_i[i]))
        error.append(error_temp**2)

    variance = (1/(n-2))*sum(error)
    print(variance)