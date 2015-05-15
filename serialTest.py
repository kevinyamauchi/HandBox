def rescale(OldNumber, OldMin, OldMax, NewMin, NewMax):

	OldRange = OldMax - OldMin

	NewRange = NewMax - NewMin

	NewNumber = NewMin + ((OldNumber - OldMin) / OldRange) * NewRange

	return NewNumber


import serial
import time

x = 1.0
y = 1.0
z = 100.0

x_rescaled = int(rescale(x, 0, 100, 0, 255))
y_rescaled = int(rescale(y, 0, 100, 0, 255))
z_rescaled = int(rescale(z, 0, 100, 0, 255))

print(x_rescaled)
print(y_rescaled)
print(z_rescaled)

NewCoords = "c" + chr(x_rescaled) + chr(y_rescaled) + chr(z_rescaled)

print(NewCoords)

port_name = "/dev/tty.usbmodem1421"
baud_rate = 9600


# Initialize the 
serial_port = serial.Serial (port_name, baud_rate, serial.EIGHTBITS,
            serial.PARITY_NONE, serial.STOPBITS_ONE, 0)

# Wait for the Arduino to start up
time.sleep(2)

serial_port.write("g")

time.sleep(5)

serial_port.write(NewCoords)


