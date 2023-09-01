import serial
port = '/dev/cu.usbmodem14201'
baud_rate=115200
arduino = serial.Serial(port, baud_rate)

while True:
    x = input
    if x!='':
        string = 'X{0:d}'.format(int(x))
        arduino.write(string.encode('utf-8'))
