import numpy as np
import matplotlib.pyplot as plt
import scipy
import csv

x_data1 = []
y_data1 = []

with open('d1.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x_data1.append(row[0])
        y_data1.append(float(row[1]))

plt.plot(x_data1, y_data1, color='b')
plt.show()