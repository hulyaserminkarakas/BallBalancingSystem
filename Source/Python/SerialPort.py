import serial

port = "COM3"
baud = 9600

ser = serial.Serial(port, baud, timeout=1)

if ser.is_open:
    print(ser.name + ' is open...')


while True:
    cmd = input("Enter command or 'exit'")

    if cmd == 'exit':
        ser.close()
        exit()
    else:
        ser.write(cmd.encode())
        out = ser.read()
        print('Receiving...'+str(out))