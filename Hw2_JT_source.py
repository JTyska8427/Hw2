# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 15:05:02 2020

@author: justi
"""

# import numpuy so we can do MATH
import numpy as np
# import sciprog so we can read the imf data file
import sciprog

# I did not import datetime as the function read_imf already does

# Read the data file using the sicprog module's read_imf function
data = sciprog.read_imf('./imf_aug2005.dat')

# open a text file named 'magB.txt', with the intention to wirte ('w'). Call this object "f"
f = open('magB.txt','w')
# Write to f a header, formatted such that each column has 7 spaces and is center justified (^)
f.write(f"{'Bx': ^7} {'By': ^7} {'Bz': ^7} {'|B|': ^7} \n")
# open a text file named 'magV.txt', with the intention to wirte ('w'). Call this object "g"
g = open('magV.txt', 'w')
# Write to g a header, formatted such that each column has 8 spaces and is center justified (^)
g.write(f"{'Vx': ^8} {'Vy': ^8} {'Vz': ^8} {'|V|': ^8} \n")

# calculate the magnitudes of magnetic field and vleocity using numpy functions
magB = np.sqrt(np.square(data['bx'][:])+np.square(data['by'][:])+np.square(data['bz'][:]))
magV = np.sqrt(np.square(data['vx'][:])+np.square(data['vy'][:])+np.square(data['vz'][:]))

# A for loop that writes to both f and g the values corresponding to the header
for i, k, j, B, x, y, z, V in zip(data['bx'], data['by'], data['bz'],magB, data['vx'], data['vy'], data['vz'], magV) :
    f.write(f"{i: ^7.2f} {k: ^7.2f} {j: ^7.2f} {B: ^7.2f}\n")
    g.write(f"{x: ^8.2f} {y: ^8.2f} {z: ^8.2f} {V: ^8.2f}\n")

# Close both f and g
f.close()
g.close()

# Calculate the mean value of magB and magV
meanB = np.mean(magB)
meanV = np.mean(magV)

# initialize a Start and End time form the data provided
Start_time = data['time'][0]
End_time = data['time'][-1]

# Print the mean value of the magnetic field and velocity over the specified data range
print(f"The Mean value of the Interplanetary Magnetic Field from {Start_time.date()} to {End_time.date()} is{meanB: .2f}")
print(f"The Mean value of the Solare Wind Velocity from {Start_time.date()} to {End_time.date()} is{meanV: .2f}")