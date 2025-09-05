from struct import pack, unpack
from machine import Pin, SoftI2C
from MPU6050dmp20 import MPU6050dmp
from time import sleep_ms

def displayData():
    while True:
        mpu.resetFIFO()     # empty buffer
        mpu.getIntStatus()
        while mpu.getFIFOCount() != 42:  # wait for next record
            if mpu.getFIFOCount() > 42:  # if more than 1 record
                mpu.resetFIFO()          # empty buffer and wait
        buf = mpu.getFIFOBytes(42)         # load FIFO buffer
        acc = mpu.dmpGetFifoAccelRaw(buf)  # read linear acceleration
        om  = mpu.dmpGetFifoGyroRaw(buf)   # and angular velocity
        print('acc:({},{},{})  gyro:({},{},{})'.format(*acc, *om))
        quat = mpu.dmpGetQuaternion(buf)
        grav = mpu.dmpGetGravity(quat)
        yaw, pitch, roll = mpu.dmpGetYawPitchRoll(quat, grav)
        theta, phi, psi  = mpu.dmpGetEuler(quat)
        print('qw:{:5.2f}  qx:{:5.2f}  qy:{:5.2f}  qz:{:5.2f}'.format(*quat))
        print('            gx:{:5.2f}  gy:{:5.2f}  gz:{:5.2f}'.format(*grav))
        print('           yaw:{:5.2f} pitch:{:5.2f}  roll:{:5.2f}'.format(yaw, pitch, roll))
        print('           theta:{:5.2f} phi:{:5.2f}  psi:{:5.2f}'.format(theta, phi, psi))
        sleep_ms(1000)

i2c = SoftI2C(scl=Pin(3),sda=Pin(4),freq=400_000)
mpu = MPU6050dmp(i2c,axOff=-58,ayOff=-791,azOff=877,gxOff=84,gyOff=47,gzOff=31)
mpu.dmpInitialize()
mpu.setDMPEnabled(True)
mpu.getIntStatus()

displayData()