import serial
ser_motor = serial.Serial(r"/dev/ttyUSB2",baudrate=9600,timeout=0.1)
ser_motor.write("0".encode())
ser_motor.write("3".encode())
