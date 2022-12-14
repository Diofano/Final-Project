from math import floor
from adafruit_rplidar import RPLidar
import numpy as np
import time

#### fuzzy 
cog = 0.0
sigma_alfa_out= 0.0
sigma_alfa = 0.0

lowpos = 1.0 # # low tunning
medpos = 2.0  # #med tunning
highpos = 4.0  ## high tunning

miux = np.zeros((3,), dtype=float)
miuy = np.zeros((3,), dtype=float)
rule = np.zeros((3,3), dtype=float)
alfa = 0.0
rule00  = 0.0  
rule01 = 0.0 
rule02 = 0.0
rule10 = 0.0
rule11 = 0.0 
rule12 = 0.0
rule20 = 0.0
rule21 = 0.0 
rule22 = 0.0

##### PID 
p = 0.0
i = 0.0
d = 0.0
sumerr = 0.0
selisih = 0.0
vpid = 0.0
e2 = 0.0
pv = 0.0
st = 0.0
vpid_new = 0.0

setpoint = 18.0    # #setpoint
de  = 0.0 
e   = 0.0         ## inputan fuzzyPID

kp = 2.0
ki = 1.5  ## ki1 = 0.33
kd = 0.0  ## kd1 = 0.33

kp_out = 0.0
ki_out = 0.0
kd_out = 0.0

timeiID  = 0.0
timenow  = 0.0
timelast = 0

##############################################


# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME, timeout=3)

array0 = np.zeros((20,), dtype=float)
array1 = np.zeros((20,), dtype=float)
array2 = np.zeros((20,), dtype=float)
array3 = np.zeros((20,), dtype=float)
array4 = np.zeros((20,), dtype=float)
array5 = np.zeros((20,), dtype=float)
# used to scale data to fit on the screen
max_distance = 0
tambah0 = 0.0
tambah1 = 0.0
tambah2 = 0.0
tambah3 = 0.0
tambah4 = 0.0
tambah5 = 0.0

tambah6 = 0.0
tambah7 = 0.0
tambah8 = 0.0
tambah9 = 0.0
tambah10 = 0.0
tambah11 = 0.0

def process_data():
    global jarakk
    global angle
    print(jarakk)

#def process_data(jaraku,derajat):
    #print(jaraku)
#    if derajat > 340 and derajat < 359:
#        global tambah0
#        #print(jaraku)
##        for i in range(20):
#            array0[i] = jaraku
#            tambah0 += array0[i]
##            #print(array0)
#           penjumlah0 = tambah0 / 19   
#        if i == 19:
#            #print(penjumlah0)
##            penjumlah0 = 0
 #           tambah0 = 0


        
    #print("Derajat :" , derajat , "", "jarak :", jarak)


scan_data = [0]*360

try:
    print(lidar.get_info())
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance 
            jarakk =scan_data[min([359, floor(angle)])] / 10
        #(scan_data)

except KeyboardInterrupt:
    print('Stopping.')

process_data()
def fuzzyeror():
    ## untuk low
    if (e <= 10):
        miux[0] = 0
    
    elif (e > 10 and e <= 13):
        miux[0] = ((e) - 10) / (3)
    
    elif (e > 13 and e <= 16):
        miux[0] = (16 - (e)) / (3)
    
    else :
        miux[0] = 0
    

    # untuk med
    if (e <= 13): ## KENAPA E < 13
        miux[1] = 0
    
    if (e > 13 and e <= 16):
        miux[1] = ((e) - (13)) / (3)
    
    elif (e > 16 and e <= 19):    
        miux [1] = (19 - (e)) / (3)
    
    else:
        miux[1] = 0
    

    ## untuk high
    if (e <= 16):
        miux[2] = 0
    
    if (e > 16 and e <= 19):
        miux[2] = ((e) - 16) / (3)
    
    elif (e > 19 and e <= 22):
        miux[2] = (22 - (e)) / (3)
    
    else:
        miux[2] = 0
    

def fuzzydeltaerror():
    # untuk  low2
    if (de <= 0):
        miuy[0] = 0
    
    elif(de > 0 and de <= 0.75):
        miuy[0] = ((de) - 0) / (0.75)
    
    elif(de > 0.75 and de <= 1.5):
        miuy[0] = (1.5 - (de)) / (0.75)
    
    else:
        miuy[0] = 0
    

    # untuk med2
    if (de <= 0.75):
        miuy[1] = 0
    
    if (de > 0.75 and de <= 1.5):
        miuy[1] = ((de) - (0.75)) / (0.75)
    
    elif(de > 1.5 and de <= 2.25):
        miuy[1] = (2.25 - de) / (0.75)
    
    else:
        miuy[1] = 0
    

    # untuk high2
    if (de <= 1.5):
        miuy[2] = 0
    
    if (de > 1.5 and de <= 2.25):
        miuy[2] = ((de) - 1.5) / (0.75)
    
    elif(de > 2.25 and de <= 3):
        miuy[2] = (3 - (de)) / (0.75)
    
    else:
        miuy[2] = 0
    


def rules():
    
    i = 0
    j = 0
    for i in range(3):
        for i in range(3):
            alfa = max(miux[i], miuy[j])
            rule[i][j] = alfa

    rule00 = rule[0][0] # (low,low2 = LOW)
    rule01 = rule[0][1] # (med,low2 = MED)
    rule02 = rule[0][2] # (high,low2 = LOW)

    rule10 = rule[1][0] # (low,med2 = MED)
    rule11 = rule[1][1] # (med,med2 = MED)
    rule12 = rule[1][2] # (high,med2 = HIGH)

    rule20 = rule[2][0] # (low,high2 = HIGH)
    rule21 = rule[2][1] # (med,high2 = HIGH)
    rule22 = rule[2][2] # (high,high2 = LOW)
    defuzzy(rule00,rule01,rule02,rule10,rule11,rule12,rule20,rule21,rule22)

def defuzzy(rule00,rule01,rule02,rule10,rule11,rule12,rule20,rule21,rule22):
    global cog
    sigma_alfa_out = (rule00 * lowpos) + (rule01 * medpos) + (rule02 * lowpos) + (rule10 * medpos) + (rule11 * medpos) + (rule12 * highpos) + (rule20 * highpos) + (rule21 * highpos) + (rule22 * lowpos);
    sigma_alfa = rule00 + rule01 + rule02 + rule10 + rule11 + rule12 + rule20 + rule21 + rule22

    cog = sigma_alfa_out / sigma_alfa
    if (sigma_alfa_out == 0 or sigma_alfa == 0):
        cog = 0
  
def pid():

    ## konstanta 
    kp_out = cog * kp
    ki_out = cog * ki
    kd_out = cog * kd

    # inputan pv
    
    ############
    p = kp_out * e
    i = ki_out * sumerr
    d = kd_out * selisih

    sumerr = e * timeiID
    selisih = de / timeiID

    e = setpoint - pv

    de = e - e2
    de = abs(de)

    vpid = p + i + d
    #print(vpid)


    e2 = e
    timelast = timenow

###############################

##### Jalan kan lidar
lidar.stop()
lidar.stop_motor()
lidar.disconnect()



