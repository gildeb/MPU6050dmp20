> __MPU6050dmp20.py__ : micropython driver for MPU6050 Digital Motion Processor 2.0 (python transcription of Jeff Rowberg driver)
>
> For ESP01, the module is too large and it must be compiled with the firmware
> 
> __firmware-combined.bin__ : micropython firmware including MPU6050dmp20 for ESP01/ESP8266

## How to use

```python
>>> from machine import Pin, SoftI2C
>>> from MPU6050dmp20 import MPU6050dmp
>>> i2c = SoftI2C(scl=Pin(3),sda=Pin(4),freq=400_000) # replace pin numbers with adequate
>>> mpu = MPU6050dmp(i2c)
```

First, measure accelerometer and gyro offsets. Lay the sensor horizontally with z-axis pointing upward, then :

```python
>>> mpu.calibrate()
```

and wait untill the offsets stabilize, or issue CTRL-C if one (more often gyro) oscillate. 

You can now initialize the sensor with the correct values :

```python
>>> mpu = MPU6050dmp(i2c,axOff=-58,ayOff=-791,azOff=877,gxOff=84,gyOff=47,gzOff=31) 
>>> mpu.dmpInitialize()
>>> mpu.setDMPEnabled(True)
>>> mpu.getIntStatus()
```

## Extracting data

_displayData.py_ read and display data after dmp initialization :

```python
>>> import displayData
```
