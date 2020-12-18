
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 02:43:16 2020

@author: justi
"""


# Fist Import the desired packages 
# sciprog to read Dst file
import sciprog
# numpy to do Maths
import numpy as np

# matplotlib.pyplot to make a Histogram
import matplotlib.pyplot as plt


# Read in the Dst file to a data dictonary
data = sciprog.read_Dst('./Dst_July2000.dat')

# calculate the Maximum and Minimum Dst over the time range
maxi = np.max(data['Dst_hrly'])
mini = np.min(data['Dst_hrly'])
# Calculate the index of the Max Dst value, divide by 24 as the data structure is a (31,24) matrix
Max_arg = np.argmax(data['Dst_hrly'])
Max_arg = Max_arg//24
# Get the date of the Maximum Dst value
maxi_date = data['Date'][Max_arg]

# Calculate the index of the Min Dst value, divide by 24 as the data structure is a (31,24) matrix
Min_arg = np.argmin(data['Dst_hrly'])
Min_arg = Min_arg//24
# Get the date of the Minimum Dst value
mini_date = data['Date'][Min_arg]

# Calculate other statistical Stuffs such as median, mean, and std
median = np.median(data['Dst_hrly'])
mean = np.mean(data['Dst_hrly'])
std = np.std(data['Dst_hrly'])

# This block calculate Hourly Means of the data accross all days, but I decided no to plot or display this data
hrly_means = np.zeros(len(data['Dst_hrly']))
temp = np.zeros(len(data['Dst_hrly']))
for j in range(len(data['Hour'])):
    for i in range(len(data['Dst_hrly'])):  
        temp[i] = data['Dst_hrly'][i][j]
    hrly_means[j] = np.mean(temp)
    
    
# Fancily Output Maximum and Minimum Dst and the date at which they occur
print(f"The Maximum Dst value for the time span provided is {maxi: .2f} nT and it occurs on {maxi_date.date():%B %d, %Y}")
print(f"The Minimum Dst value for the time span provided is {mini: .2f} nT and it occurs on {mini_date.date():%B %d, %Y}")
print("")
# Fancily Output Mean and Median and compare for a suprise conslusion
print(f"The Mean Dst value for the time span provided is {mean: .2f} nT")
print(f"The Median Dst value for the time span provided is {median: .2f} nT")
print("The Mean and Median are not equal, indicating the data is not a Normal Distribution *WINK* ")

#Create Distribution to be displayed in a Histogram
Dis = np.zeros(24*len(data['Dst_hrly']))
for j in range(len(data['Dst_hrly'])):
    for i in range(len(data['Hour'])):
        Dis[j*len(data['Hour'])+i] = data['Dst_hrly'][j][i]

# Find Start and End data from data
Start_date= data['Date'][0]
End_date = data['Date'][-1]

# Create histogram from Distribution
x=plt.hist(Dis,bins=100)

# Add title and axis labels to Histogram 
plt.title(f"Histogram of Dst over the interval {Start_date.date():%B %d, %Y} to {End_date.date():%B %d, %Y}")
plt.ylabel("Amplitude")
plt.xlabel("Dst Value")

# Plot a dashed black line indicating the mean of the distribution
plt.axvline(mean, color='k', linestyle='dashed', linewidth=1)

# Find min and max y values
min_ylim, max_ylim = plt.ylim()

#label Mean 
plt.text(mean*4.25, max_ylim*0.85, 'Mean: {:.2f}'.format(mean))

# Plot a dashed red line indication the median of the distribution, and create a corresponding label
plt.axvline(median, color='r', linestyle='dashed', linewidth=1)
plt.text(mean*0.74, max_ylim*0.96, 'Meidan: {:.2f}'.format(median), color = 'r')

# Show the plot
plt.show()

## ** NOTE: The following code is created with prior knowledge of the data. If I didnt already know it was only a month of data, I would do this differently **

# Get Start Day and Get End Day
x1 = int(f"{Start_date.date():%d}")
xn = int(f"{End_date.date():%d}") 
# Create a list of Days
t = [ x+1 for x in range(xn)] 

# Create a Connected Scatter plot of Daily Mean Dst values
plt.scatter(t, data['Mean_Dst'])
plt.plot(t, data['Mean_Dst'])

# Create a title, and label axis accordingly
plt.title(f"Daily Mean Dst over the interval {Start_date.date():%B %d, %Y} to {End_date.date():%B %d, %Y}")
plt.ylabel("Mean Dst Value")
plt.xlabel("Day")



