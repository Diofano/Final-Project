

from math import floor
from adafruit_rplidar import RPLidar
import numpy as np

# Setup the RPLidar
PORT_NAME = "/dev/ttyUSB0"
lidar = RPLidar(None, PORT_NAME, timeout=3)

data1 = np.zeros((20,), dtype = float)
jarakk = 0.0
tambah = 0.0
hasil = 0.0

# used to scale data to fit on the screen
max_distance = 0 


def process_data(jarak, derajat):
    global tambah
    derajat = int(derajat)
    if derajat > 79 and derajat < 101:
       # print(jarak)
        for i in range(20):
            data1[i] = jarak
            tambah += data1[i]
            if i == 19:
                hasil = tambah / 20
                tambah = 0 
        print(hasil)

   #177


scan_data = [0] * 360

try:
    #    print(lidar.get_info())
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance / 10
            jarakk = scan_data[min([359, floor(angle)])]
            process_data(jarakk,angle)

except KeyboardInterrupt:
    print("Stopping.")

lidar.stop()
lidar.stop_motor()
lidar.disconnect()
