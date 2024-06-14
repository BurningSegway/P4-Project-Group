import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Exercise 1: Use one of the files with data in the moodle materials folder to plot the absolute, relative, and normalized histograms of (choose one):
#a) The latency for communication in our Starlink setup (file: Starlink latency.csv)
#b) The temperature measured by a sensor during a PhD course at Oulu University (file:temperature.csv)
#Try different numbers of bins. Is the data approximately normal?


def opgave_1():
    #Starlink_data = pd.read_csv("Starlink_latency.csv")
    df = pd.read_csv("temperature.csv")
    print(df.keys())

    #absolut
    plt.hist(df[" 26.7"], bins=10, color="red")

    #Normalized
    plt.hist(df[" 26.7"], bins=10, color="blue", density=True)

    #Relative - Denne er meget mindre i værdi og læser derfor ikke så godt når de andre værdier også bliver plottet
    plt.hist(df[" 26.7"], bins=10, color="black", weights=np.ones_like(df[" 26.7"]) / len(df[" 26.7"]))

    #df.plot.hist()
    plt.show()

opgave_1()


#Exercise 2: Simulate rolling a fair dice n times.
#a) Calculate the sample mean Xi and variance Si2 for all i = 1, 2, . . . , n.
#b) Plot the sample mean Xi and Xi ± Si.
#c) Plot a normalized histogram with the n outcomes. How many times do you need to roll the dice so the histogram resembles the pmf of a uniform RV?
#Tip: You can use the code dice loln.py in the moodle page as a base


Terning = np.random.randint(1,7, 100)



def opgave_2():
    df2 = pd.DataFrame({"die": np.random.randint(1,7,100)})
    df2_empty = []
    df2_mean = []
    df2_x = []
    #print(df.mean())
    print(len(df2))

    for i in range(len(df2)):
        df2_empty.append(df2["die"][i])
        df2_mean.append(np.mean(df2_empty))
        df2_x.append(i)
        

    plt.plot(df2_x, df2_mean, color ="green") 
    plt.show()





#Exercise 3: Consider the case of flipping a fair coin n times and let Hn be the random variable (RV) of the number of heads.
#Also recall that the sum of n Bernoulli RVs is a Binomial random variable with mean np and variance np(2−p).
#Calculate and compare the probability of observing H10 ≥ 7 and H100 ≥ 70 using each of the following methods.
#a) Summing over the formula for the probability mass function (pmf) of Binomial RVs (Bliver ikke lavet, det er vidst mere sandsynlighed)
#b) Using the central limit theorem


#Når man skal bruge the central limit theorom skal man finde den normaliserede mean
coin = pd.DataFrame({"heads":np.random.randint(0,2,100)})


























