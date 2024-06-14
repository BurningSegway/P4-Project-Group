import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from scipy.stats import norm, binom, t
from Stats_funcs import mean_csv,plt_Hist_norm,plt_PFD_GAUS,binomial_pmf, plt_Hist_relative, plt_Hist, sum_function, Z_score, T_Test, estimate_coef
#Functionsoversigt
#mean_csv - plt_Hist - plt_Hist_norm - plt_Hist_relative - plt_PFD_GAUS - binomial_pmf - sum_function -

def opgave_1_1(subtask):
    #Læs dataen
    data = pd.read_csv("Starlink_latency.csv")
    #find keys
    print(data.keys())
    #Ekstraher kolonnen med den relevante data
    latency_data = data[" pop_latency[ms] "]

    #Find gaussiske værdier
    mean, variance, std_dev = mean_csv(latency_data)

    if subtask == "a":
        #plot histogram
        fig, axs = plt.subplots(2, 2, figsize=(20, 10), sharey=None)
        axs[0, 0].hist(latency_data, bins=100, color="red", alpha=0.6)
        axs[0, 0].set_title("absolut")
        axs[0, 1].hist(latency_data, bins=100, color="red", density=True, alpha=0.6)
        axs[0, 1].set_title("normalized")
        axs[1, 0].hist(latency_data, bins=100, color="black", weights=np.ones_like(latency_data) / len(latency_data))
        axs[1, 0].set_title("relative")

        plt.show()
    else:
        x_values = np.linspace(min(latency_data), max(latency_data), 1000)
        pdf_values = norm.pdf(x_values, mean, std_dev)
        plt.plot(x_values, pdf_values, color="black", linewidth=2)
        plt.hist(latency_data, bins=100, color="red", density=True, alpha=0.6)
        plt.xlabel("Latency (ms)")
        plt.ylabel("Density")
        plt.title("Histogram and PDF of Latency Data: bin 100")
        plt.show()
#opgave_1_1("d")


def opgave_1_2():
    #opret tomme variabler
    mean_list, variance_list, std_dev_list, mean_variance_Ulist, mean_variance_Llist, sizes = [], [], [], [], [], []

    #For loop der bestemmer hvor mange gange forsøget skal køre
    for i in range(1, 1000):
        #Terningens udfald
        dice_data = np.random.randint(low=1, high=7, size=i)

        #find mean, varians og std_dev for forsøget
        mean, variance, std_dev = mean_csv(dice_data)
        #gem dem i lister
        mean_list.append(mean)
        variance_list.append(variance)
        std_dev_list.append(std_dev)
        #gem hvor meget std_dev ville tillade værdien at gå op eller ned
        mean_variance_Ulist.append(mean+std_dev)# std_dev kan udregnes som math.sqrt(variance)
        mean_variance_Llist.append(mean-std_dev)

        #gem antallet af variable i hvert forsøg så vi kan plotte imod dem
        sizes.append(i)
    
    #converter til np.arrays da disse kan plottes direkte
    mean_array = np.array(mean_list)
    mean_variance_Uarray = np.array(mean_variance_Ulist)
    mean_variance_Larray = np.array(mean_variance_Llist)

    #plot mean, samt øvre og nedre grænse
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, mean_array, 'r-', label='Sample mean',  linewidth=1)
    #plt.plot(sizes, mean_variance_Uarray, color="grey", linestyle='--', label='Sample mean+variance')
    #plt.plot(sizes, mean_variance_Larray, color="grey", linestyle='--', label='Sample mean-variance')
    plt.fill_between(sizes, mean_variance_Uarray, mean_variance_Larray, color="grey", alpha=0.3, label='Mean ± Std Dev')
    plt.plot(sizes, dice_data, 'bo', alpha=0.4 , label='dice values')
    # Add labels and title
    plt.xlabel('Sample size')
    plt.ylabel('Mean value')
    plt.title('Sample Mean and Mean ± Standard Deviation for Different Sample Sizes')
    plt.legend()
    plt.grid(True)
    # Show the plot
    plt.show()

    #Plot det normaliserede histogram
    fig, axs = plt.subplots(2, 2, figsize=(20, 10), sharey=None)
    dice_data10 = np.random.randint(low=1, high=7, size=10)
    dice_data100 = np.random.randint(low=1, high=7, size=100)
    dice_data500 = np.random.randint(low=1, high=7, size=500)
    dice_data1000 = np.random.randint(low=1, high=7, size=1000)
    axs[0, 0].hist(dice_data10, bins=6, color="blue", density=True, alpha=0.6)
    axs[0, 0].set_title('Dice rolls (n=10)')

    axs[0, 1].hist(dice_data100, bins=6, color="blue", density=True, alpha=0.6)
    axs[0, 1].set_title('Dice rolls (n=100)')

    axs[1, 0].hist(dice_data500, bins=6, color="blue", density=True, alpha=0.6)
    axs[1, 0].set_title('Dice rolls (n=500)')

    axs[1, 1].hist(dice_data1000, bins=6, color="blue", density=True, alpha=0.6)
    axs[1, 1].set_title('Dice rolls (n=1000)')
    plt.show()
#opgave_1_2()



def opgave_1_3(method):
    # Parameters
    p = 0.5  # Probability of success (fair coin)
    n1 = 10  # Number of trials for H10
    n2 = 100 # Number of trials for H100

    
    if method == "math":
        p = 0.5  # Probability of success (fair coin)
        n1 = 10  # Number of trials for H10
        n2 = 100 # Number of trials for H100

        # Function to calculate binomial probability mass function

        # Calculate probabilities for H10 >= 7
        probabillity_heads_7 = sum(binomial_pmf(n1, k, p) for k in range(7, n1 + 1))

        # Calculate probabilities for H100 >= 70
        probabillity_heads_70 = sum(binomial_pmf(n2, k, p) for k in range(70, n2 + 1))
    elif method == "scipy":
        # Calculate probabilities
        probabillity_heads_7 = 1 - binom.cdf(6, n1, p)
        probabillity_heads_70 = 1 - binom.cdf(69, n2, p)

    elif method == "clt":
        # Calculate mean and standard deviation of binomial distribution
        mu1 = n1 * p
        sigma1 = (n1 * p * (1 - p)) ** 0.5

        mu2 = n2 * p
        sigma2 = (n2 * p * (1 - p)) ** 0.5

        # Use normal approximation for H10 >= 7
        z1 = (7 - mu1) / sigma1  # Continuity correction
        probabillity_heads_7 = 1 - norm.cdf(z1)

        # Use normal approximation for H100 >= 70
        z2 = (70 - mu2) / sigma2  # Continuity correction
        probabillity_heads_70 = 1 - norm.cdf(z2)


    print("Probability of observing H10 >= 7:", probabillity_heads_7)
    print("Probability of observing H100 >= 70:", probabillity_heads_70)

#The CLT states that the sum of a large number of independent and identically distributed random variables, 
#regardless of the original distribution, will be approximately normally distributed. For binomial distributions, 
#this approximation becomes more accurate as n increases.

#Here's how you can use the CLT to approximate the probabilities:

#Calculate the mean (𝜇) and standard deviation (𝜎) of the binomial distribution.
#Approximate the binomial distribution with a normal distribution using these parameters.
#Use the cumulative distribution function (CDF) of the normal distribution to calculate the probabilities.


#opgave_1_3("scipy")


def gaus_likely(x, varians, mean):
    efter = 1
    for i in range(len(x)):
        før = ( 1/math.sqrt(2*math.pi*varians) ) * math.exp(-1*((x[i]-mean)**2)/2*varians)
        efter = efter*før
    return efter



def opgave_1_5():
    # Read the data
    data = pd.read_csv("temperature.csv")
    
    # Extract the column with the relevant data
    temperature_data = data[" 26.7"]
    
    # Define the number of data points in each group
    group_sizes = [10, 100]
    
    # Calculate the variance, standard deviation, and mean for the entire dataset
    mean, variance, std_dev = mean_csv(temperature_data)
    print("Mean:", mean, "Variance:", variance)
    
    temperature_data10 = temperature_data[0:10]
    temperature_data100 = temperature_data[0:100]
    
    x = np.linspace(23, 33)
    y10 = []
    y100 = []
    y10_log = []
    y100_log = []
    for i in range (len(x)):
        y10.append(gaus_likely(temperature_data10, variance, x[i]))
        y100.append(gaus_likely(temperature_data100, variance, x[i]))
        y10_log.append(math.log(gaus_likely(temperature_data10, variance, x[i])))
        y100_log.append(math.log(gaus_likely(temperature_data100, variance, x[i])))

    

    fig, axs = plt.subplots(2, 1, figsize=(10, 6), sharey=None)
    axs[0].plot(x, y10)
    axs[0].set_title("n = 10")
    # Add labels, title, legend, and grid
    axs[0].set_xlabel("mean")
    axs[0].set_ylabel('Likelihood')
    
    axs[1].plot(x, y100)
    axs[1].set_title("n = 100")
    # Add labels, title, legend, and grid
    axs[1].set_xlabel('mean')
    axs[1].set_ylabel('Likelihood')

    plt.show()

    plt.plot(x, y10_log, label="n = 10")
    plt.title("n = 10")
    # Add labels, title, legend, and grid
    plt.xlabel("mean")
    plt.ylabel('Likelihood')
    
    plt.plot(x, y100_log, label="n = 100")
    plt.title("n = 100")
    # Add labels, title, legend, and grid
    plt.xlabel('mean')
    plt.ylabel('Likelihood')
    plt.legend()
    
    plt.show()


    X10 = sum(temperature_data10)
    X100 = sum(temperature_data100)
    print('sum af X for n=10', X10)
    print('sum af X for n=100', X100)
    #Bare kør denne ligning i maple. det virker
    ligning = ((2*X10-2*10*mean) / (2 * x))




#opgave_1_5()



def opgave_2_3(opgave):
    #Læs dataen
    data = pd.read_csv("execution_times.csv")
    #find keys
    #print(data.keys())
    #Ekstraher kolonnen med den relevante data
    execution_data = data["execution_time"]

    #Find gaussiske værdier
    mean, variance, std_dev = mean_csv(execution_data)
    #print(mean, variance, std_dev)

    execution_data10 = execution_data[0:10]
    execution_data1000 = execution_data[0:1000]
    if opgave == 'a':
        X10 = sum(execution_data10)
        X1000 = sum(execution_data1000)
        print('sum af X for n=10', X10)
        print('sum af X for n=1000', X1000)
    elif opgave == 'b':
        plt.hist(execution_data, bins=50)
        plt.axvline(x = 13.04978140, color = 'red',  label = 'mean n=1000')
        plt.show()
    elif opgave == 'd':
        mean_10 = 13.35643168
        mean_1000 = 13.04978140
        Z = 1.96

        perm = 0
        for i in range(0, 10):
            temp = (execution_data10[i] - mean_10)**2
            perm += temp
        n = 10
        s_variance10 = 1/(n-1) * perm
        #print(s_variance10)
        CL10 = (Z*(s_variance10/math.sqrt(n)))
        print('CL10 = (', mean_10-CL10 , ',', mean_10+CL10, ')')

        perm = 0
        for i in range(0,1000):
            temp = (execution_data1000[i] - mean_1000)**2
            perm += temp
        n = 1000
        s_variance1000 = 1/(n-1) * perm
        #print(s_variance1000)
        CL1000 = ((s_variance1000/math.sqrt(n)))
        print('CL10000 = (', mean_1000-CL1000 , ',', mean_1000+CL1000, ')')
    elif opgave == 'e':
        print('lavet i maple')


#opgave_2_3()


def opgave_2_5(opgave):
    x_i = [0.41, 0.46, 0.44, 0.47, 0.42, 0.39, 0.41, 0.44, 0.43, 0.44]
    y_i = [1850, 2620, 2340, 2690, 2160, 1760, 2500, 2750, 2730, 3120]

    np_x_i = np.asarray(x_i, dtype=np.float32)
    np_y_i = np.asarray(y_i, dtype=np.float32)

    b_0, b_1 = estimate_coef(np_x_i, np_y_i)
    if opgave == 'b':
        print('b_o =',b_0, 'b_1 =', b_1)

    if opgave == 'c':
        print(b_0+b_1*0.43)
    y = []
    for i in range(len(x_i)):
        y_temp = b_0 + b_1 * x_i[i]
        y.append(y_temp)

    plt.scatter(x_i, y_i)
    plt.plot(x_i, y)
    plt.show()

    if opgave == 'd':
        error_temp = 0
        error = []
        n=10
        for i in range(len(x_i)):
            error_temp = (y_i[i]-(b_0+b_1*x_i[i]))
            error.append(error_temp**2)

        variance = (1/(n-2))*sum(error)
        print(variance)

#opgave_2_5('d')


def opgave_3_1():
    mean = 210
    std_dev = 35
    sample_mean = 200

    n = 25
    T_25 = T_Test(sample_mean, mean, n, std_dev)
    Z = Z_score(0.95)
    #T_Ting = t(n-1).ppf(T)
    P = t(n-1).cdf(T_25)
    print('T_25=', T_25)
    print('Z =', Z)
    print('P =', P)

    n = 64
    T_64 = T_Test(sample_mean, mean, n, std_dev)
    Z = Z_score(0.95)
    #T_Ting = t(n-1).ppf(T)
    P = t(n-1).cdf(T_64)
    print('T_64=', T_64)
    print('Z =', Z)
    print('P =', P)

#opgave_3_1()
''' (Israels interpretation) In this case, we cannot reject H0 when the sample size is n = 25. This is because, even
though the sample mean is lower than the value of µ0 > µ^n, this outcome is not so extreme
with µ0 and a relatively small sample size of 25 as indicated by the p-value of 0.0766.
As the sample size increases, it would be expected that extreme outcomes in the sample mean
happen more rarely because the standard deviation of the sample mean std_dev/√
n decreases as n
increases. However, this is not the case and the outcome for a sample mean of 200 is considered
an extreme case as indicated by the p-value of 0.0111. Therefore, H0 is rejected for n = 64 but
not for n = 25.'''

def opgave_3_2():
    n = 500
    k = 138
    p_0 = 0.255
    N_led = []
    p_0_i = []
    _1_p_0 = []
    for i in range(138, 500):
        N_led.append(math.factorial(n) / (math.factorial(i)*math.factorial(n-i)))
        p_0_i.append(p_0 ** i)
        _1_p_0.append((1-p_0)**(n-i))

    perm = 0
    for i in range(len(N_led)):
        temp = N_led[i]*p_0_i[i]*_1_p_0[i]
        perm += temp 

    print(perm)
    #print(perm)
    '''Der er en anden løsning til denne som jeg ikke helt har fået lavet endnu'''
#opgave_3_2()


#def opgave_3_3():
    






