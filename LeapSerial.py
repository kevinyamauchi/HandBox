def rescale(OldNumber, OldMin, OldMax, NewMin, NewMax):

	OldRange = OldMax - OldMin

	NewRange = NewMax - NewMin

	NewNumber = NewMin + ((OldNumber - OldMin) / OldRange) * NewRange

	# Handle the out-of-bounds cases
	NewNumber = NewMax if (NewNumber > NewMax) else NewNumber
	NewNumber = NewMin if (NewNumber < NewMin) else NewNumber

	return NewNumber


import sys
import serial
import time
import pygame

# Add the Leap libraries to the path
sys.path.insert(0, "./lib")
import Leap


class LeapListener(Leap.Listener):

	def on_init(self, controller):

		# Create the py
		file = 'rick.mp3'

		pygame.mixer.init()
		pygame.mixer.music.load(file)

		# Initialize the scrolling flag
		self.scrolling = False

		port_name = "/dev/tty.usbmodem1411"

		baud_rate = 9600

		self.serialPort = serial.Serial (port_name, baud_rate, serial.EIGHTBITS,
			serial.PARITY_NONE, serial.STOPBITS_ONE, 0)

		time.sleep(2)

		print "arduino connected"
		

	def on_connect(self, controller):

		print "Connected"





	def on_frame(self, controller):

		frame = controller.frame()

		if(self.scrolling & (len(frame.hands) == 0 )):
			self.serialPort.write("s")
			pygame.mixer.music.fadeout(500)
			self.scrolling = False

		
		for hand in frame.hands:

			if (self.scrolling == False):

				self.serialPort.write("g")

				pygame.mixer.music.play(-1)

				self.scrolling = True

			
			x = hand.palm_position[0]
			z = hand.palm_position[2]

			print(x)

			x_rescaled = int(rescale(x, -50., 50., 1, 255))
			y_rescaled = int(rescale((z + x), -50, 100, 1, 255))
			z_rescaled = int(rescale(z, 5, 100, 1, 255))
			
			NewCoords = "c" + chr(x_rescaled) + chr(y_rescaled) + chr(z_rescaled)
			NewCoords_read = "c" +  " " + str(x_rescaled) + " " +  str(y_rescaled) + " " +  str(z_rescaled)

			print(NewCoords_read)

			self.serialPort.write(NewCoords)

			time.sleep(0.1)
			


def main ():

	# Create a sample listener and controller
    listener = LeapListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
    	controller.remove_listener(listener)

if __name__ == "__main__":
    main()





# NewCoords = "c" + chr(x_rescaled) + chr(y_rescaled) + chr(z_rescaled)

# print(NewCoords)

# port_name = "/dev/tty.usbmodem1421"
# baud_rate = 9600


# # Initialize the 
# serial_port = serial.Serial (port_name, baud_rate, serial.EIGHTBITS,
#             serial.PARITY_NONE, serial.STOPBITS_ONE, 0)

# # Wait for the Arduino to start up
# time.sleep(2)

# serial_port.write("g")

# time.sleep(5)

# serial_port.write(NewCoords)


