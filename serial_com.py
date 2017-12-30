import serial

port = "COM3"
baud = 115200

ser = serial.Serial(port, baud, timeout=1)

if ser.is_open:
    print(ser.name + ' is open...')


def set_angles(out_x, out_y):
    cmd = str(out_x+90)+':'+str(out_y+90)+'$'
    ser.write(cmd.encode())
    #print(out_x, out_y)

def close_connection():
    ser.close()

