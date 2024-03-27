import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv("Pierres Mappe/Statistics/Starlink_latency.csv")
latency = df['latency'] #you can also use df['column_name']

print(latency)

lat = df['latency'].to_numpy()

print(lat)

#plotting the first histogram

bin_num = 40

plt.figure(figsize=(12,4))
plt.subplot(1, 3, 1)
plt.hist(lat, bins=bin_num, color='green')
plt.title('Histogram')
plt.xlabel('Temperature')
plt.ylabel('Frequency')

plt.subplot(1, 3, 2)
plt.hist(latency, bins=bin_num, color='red', density=True)
plt.title('Normalized Histogram')
plt.xlabel('Temperature')
plt.ylabel('Normalized Frequency')

plt.subplot(1, 3, 3)
plt.hist(latency, bins=bin_num, color='blue', weights=np.ones(len(latency)) / len(latency))
plt.title('Histogram with weights')
plt.xlabel('Temperature')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()