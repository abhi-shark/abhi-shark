import serial
import serial.tools.list_ports

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

output = scanSerial()
print(output)
f = open("serial_nums.tst","w")
f.write(output[0][2])
f.write(",")
f.write(output[1][2])
f.close()