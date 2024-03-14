import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Exercise 1: Use one of the files with data in the moodle materials folder to plot the absolute, relative, and normalized histograms of (choose one):
#a) The latency for communication in our Starlink setup (file: Starlink latency.csv)
#b) The temperature measured by a sensor during a PhD course at Oulu University (file:temperature.csv)
#Try different numbers of bins. Is the data approximately normal?



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


