import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
import math



def mean_csv(data):
    #Find gaussiske værdier
    mean = np.mean(data)
    variance = np.var(data)
    std_dev = np.sqrt(variance)
    return mean, variance, std_dev

def plt_Hist(data):
    plt.hist(data, bins=100, color="red", alpha=0.6)
    return
def plt_Hist_norm(data):
    plt.hist(data, bins=100, color="red", density=True, alpha=0.6)
    return
def plt_Hist_relative(data):
    plt.hist(data, bins=100, color="black", weights=np.ones_like(data) / len(data))
    return

def plt_PFD_GAUS(data, mean, std_dev):
    x_values = np.linspace(min(data), max(data), 1000)
    pdf_values = norm.pdf(x_values, mean, std_dev)
    plt.plot(x_values, pdf_values, color="black", linewidth=2)
    return

def binomial_pmf(n, k, p):
    return math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k))



def sum_function(n, f):
    total_sum = 0
    for i in range(1, n + 1):
        total_sum += f(i)
    return total_sum


def Z_score(percentile):
    x = norm.ppf(percentile)
    return x


def T_Test(samle_mean, mean, n, std_dev):
    T = ((samle_mean-mean)*math.sqrt(n)) / std_dev
    return T



def estimate_coef(x, y): 
  # number of observations/points 
  n = np.size(x) 
  
  # mean of x and y vector 
  m_x = np.mean(x) 
  m_y = np.mean(y) 
  
  # calculating cross-deviation and deviation about x 
  SS_xy = np.sum(y*x) - n*m_y*m_x 
  SS_xx = np.sum(x*x) - n*m_x*m_x 
  
  # calculating regression coefficients 
  b_1 = SS_xy / SS_xx 
  b_0 = m_y - b_1*m_x 
  
  return (b_0, b_1)