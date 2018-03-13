#!/usr/bin/python
# -*- coding: utf-8 -*-

# IMU exercise
# Copyright (c) 2015-2018 Kjeld Jensen kjen@mmmi.sdu.dk kj@kjen.dk

##### Insert initialize code below ###################

## Uncomment the file to read ##
#fileName = 'imu_razor_data_static.txt'
#fileName = 'imu_razor_data_pitch_55deg.txt'
#fileName = 'imu_razor_data_roll_65deg.txt'
fileName = 'imu_razor_data_yaw_90deg.txt'

## IMU type
#imuType = 'vectornav_vn100'
imuType = 'sparkfun_razor'

## Variables for plotting ##
showPlot = True
plotData = []

## Initialize your variables here ##
myValue = 0.0
relAng_z= 0.0
relAng_x= 0.0
relAng_y= 0.0
t_min = 0.0
t_max = 0.0
all_time = []
all_angle =[]
#bias =  2.5645783787785335
bias =  0.0004507093880603014
staticData = False
dataWithBias = True



######################################################

# import libraries
from math import pi, sqrt, atan2
import matplotlib.pyplot as plt

# open the imu data file
f = open (fileName, "r")

# initialize variables
count = 0

# looping through file

for line in f:
	count += 1

	# split the line into CSV formatted data
	line = line.replace ('*',',') # make the checkum another csv value
	csv = line.split(',')

	# keep track of the timestamps
	ts_recv = float(csv[0])
	if count == 1:
		ts_now = ts_recv # only the first time
 	ts_prev = ts_now
	ts_now = ts_recv

	if imuType == 'sparkfun_razor':
		# import data from a SparkFun Razor IMU (SDU firmware)
		acc_x = int(csv[2]) / 1000.0 * 4 * 9.82;
		acc_y = int(csv[3]) / 1000.0 * 4 * 9.82;
		acc_z = int(csv[4]) / 1000.0 * 4 * 9.82;
		gyro_x = int(csv[5]) * 1/14.375 * pi/180.0;
		gyro_y = int(csv[6]) * 1/14.375 * pi/180.0;
		gyro_z = int(csv[7]) * 1/14.375 * pi/180.0;

	elif imuType == 'vectornav_vn100':
		# import data from a VectorNav VN-100 configured to output $VNQMR
		acc_x = float(csv[9])
		acc_y = float(csv[10])
		acc_z = float(csv[11])
		gyro_x = float(csv[12])
		gyro_y = float(csv[13])
		gyro_z = float(csv[14])
	 		
	##### Insert loop code below #########################

	# Variables available
	# ----------------------------------------------------
	# count		Current number of updates		
	# ts_prev	Time stamp at the previous update
	# ts_now	Time stamp at this update
	# acc_x		Acceleration measured along the x axis
	# acc_y		Acceleration measured along the y axis
	# acc_z		Acceleration measured along the z axis
	# gyro_x	Angular velocity measured about the x axis
	# gyro_y	Angular velocity measured about the y axis
	# gyro_z	Angular velocity measured about the z axis

	## Insert your code here ##
	delta_t = ts_now -ts_prev
	
	#ex 4.2.1 integrate angular velocity to relative angle
	
	if dataWithBias == True:
		tmp = gyro_z*180.0/pi
		relAng_z += delta_t*(tmp -bias)
		#tmp = gyro_x -bias
		#relAng_x += tmp*delta_t
		#myValue = pitch # relevant for the first exercise, then change this.
		myValue = relAng_z
		#plotData.append (myValue*180.0/pi)
		# in order to show a plot use this function to append your value to a list:
		plotData.append (myValue)
	else:
		relAng_z += delta_t*gyro_z
		#myValue = pitch # relevant for the first exercise, then change this.
		myValue = relAng_z
		# in order to show a plot use this function to append your value to a list:
		plotData.append (myValue*180.0/pi)
		
	all_time.append(ts_now)
	all_angle.append(relAng_z)
	
	
	
	

	######################################################
	
t_min= min(all_time)
t_max= max(all_time)
ang_min=min(all_angle)
ang_max=max(all_angle)
if staticData==True:
    bias = (ang_max*180.0/pi)/count

if dataWithBias == True:
	print("time ",t_max-t_min,"  drift angle ",ang_max)
	print("drift ", ang_max/(t_max-t_min),"degrees/seconds")
	print("bias ",bias)
else:
	print("time ",t_max-t_min,"  drift angle ",ang_max*180.0/pi)
	print("drift ",(ang_max*180.0/pi)/(t_max-t_min),"degrees/seconds")
	print("bias ",bias)
# closing the file	
f.close()

# show the plot
if showPlot == True:
	plt.plot(plotData)
	#plt.savefig('gyro_calc_rel_angle_90_degree_w_bias.png')
	plt.show()


