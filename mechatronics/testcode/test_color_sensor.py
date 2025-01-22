from qtpyControl import QTPYControl_1, QTPYControl_2

import serial
import serial.tools.list_ports
import time
import threading 
import queue

def scanSerial() :
    output = []
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports) :
        # port, description, hwid string, and serial number
        try:
            output.append([port, hwid, hwid.split(" ")[2].split("=")[1]])
        except:
            continue
    return output

def readQTPY1(q,QTPY1):
  response = QTPY1.serialPort.readline().decode().strip()
  QTPY1.handle_action(response)

def readQTPY2(q,QTPY2):
  response = QTPY2.serialPort.readline().decode().strip()
  QTPY2.handle_action(response)

serport1 = "85438303233351815100"
serport2 = "626DA1425154465336202020FF150C0B"

for i in scanSerial():
  if i[2] == serport1:
    port1 = i[0]
  elif i[2] == serport2:
    port2 = i[0]
    
ser1 = serial.Serial(port1, 9600)  
ser2 = serial.Serial(port2, 9600)  

QTPY1 = QTPYControl_1(ser1)
QTPY2 = QTPYControl_2(ser2)

# Get initial color reading
first_color = QTPY2.serialPort.readline().decode().strip()

QTPY1.color = "BLU"
prev = QTPY1.cs

opts = ["sort", "go", "stop"]
ind = 0
count = 0

q1 = queue.Queue()
q2 = queue.Queue()

while True:
  
  t1 = threading.Thread(target = readQTPY1, args = (q1,QTPY1))
  t1.start()
  t2 = threading.Thread(target = readQTPY2, args= (q2,QTPY2))
  t2.start()
 
  time.sleep(1)

  
  if ((not QTPY1.cs) and (QTPY1.ps)):
    QTPY1.actuate_servo("rej")
  elif (QTPY1.cs and QTPY1.ps):
    QTPY1.actuate_servo("acc")
    print("ACC")
    count = count+1
  else:
    print("PASS")

  if count >= 3:
    QTPY1.actuate_servo("dis")
    count = 0
  
  #QTPY1.color = QTPY2.color
    
  