# Senior Design Project Fall 2023 - PAQ Lite

The purpose of this project is to create a low-cost, portable air quality monitor for individuals with chronic 
respiratory disease to monitor levels of formaldehyde and particulate matter (PM) in the air. The two sensors in 
the device are the Sensiron SFA30-D-T to detect formaldehyde, and the Honeywell HPMA115CO-004 to detect PM. 
The SFA30-D-T also has temperature and humidity sensing capabilities. Both sensors are integrated using a 
Raspberry Pi Zero W. A previous design iteration used a Raspberry Pi Pico, but the Pico could not successfully
read data from either sensor. The user will be alerted to dangerous concentrations of formaldehyde and PM in the 
air via vibration and a warning message displayed on the onboard LCD. When levels of PM and formaldehyde begin to 
decrease, indicating that the user has moved to a safer location, the device will cease vibrating.

This repository contains the firmware code necessary to operate the device.
