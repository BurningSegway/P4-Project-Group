import numpy as np
import scipy as sp
import math


alpha = 0.05
Z_alpha = sp.stats.norm.ppf(1-alpha)
print(Z_alpha)

T_1=((-10)*(25**0.5))/35
print("T_1= ", T_1)

phi_1=sp.stats.norm.cdf(T_1)
print("P_1 = ", phi_1)


T_2=((-10)*(64**0.5))/35
print("T_1= ", T_2)

phi_2=sp.stats.norm.cdf(T_2)
print("P_1 = ", phi_2)


if T_1 < -Z_alpha :
    print("T_1 rejected")
else:
    print("T_1 accepted")

if T_2 < -Z_alpha :
    print("T_2 rejected")
else:
    print("T_2 accepted")
