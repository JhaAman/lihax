import numpy as np
import math

# simple class to contain the node's variables and code
class PotentialField:
    # class constructor; subscribe to topics and advertise intent to publish
    def __init__(self):
        # initialize potential field variables
        self.charge_laser_particle = 0.07
        self.charge_forward_boost = 25.0
        self.boost_distance = 0.5
        self.p_speed = 0.05       
        self.p_steering = 1.0

        #socket initialization
        self.host_ip = socket.gethostname()
        self.receiving_port = 5510
        self.sending_port = 6510
        self.sockR = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockS = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockS.connect((self.host_ip, self.sending_port))
        self.sockR.bind((self.host_ip, self.recieving_port))

	self.speedHist = 1.0

    def scan_callback(self):
        while True:
            packet = self.sockR.recvfrom(65565)[0]
            ranges = struct.unpack("1080f", packet)[180:901]
        
            # Create potential gradients for middle 180 degrees of laser scan particles
            scan_rad_angles = ( (0.25 * np.arange(1081, dtype=float)) ) # + msg.angle_min??
            scan_rad_angles = scan_rad_angles[180:901]
    
            scan_x_unit_vectors = -np.cos(scan_rad_angles)
            scan_y_unit_vectors = -np.sin(scan_rad_angles)
    
            scan_x_components = (self.charge_laser_particle * scan_x_unit_vectors) / np.square(msg.ranges)
            scan_y_components = (self.charge_laser_particle * scan_y_unit_vectors) / np.square(msg.ranges)

            # Add the potential for the point behind the robot (to give it a kick)
            kick_x_component = np.ones(1) * self.charge_forward_boost / self.boost_distance**2.0
            kick_y_component = np.zeros(1)

            # Add together the gradients to create a global gradient showing the robot which direction to travel in
            total_x_component = np.sum(scan_x_components) + kick_x_component
            total_y_component = np.sum(scan_y_components) + kick_y_component

            # Now, create a steering command to send to the vesc.
            steering_angle = (self.p_steering * np.sign(total_x_component) * math.atan2(total_y_component, total_x_component))
            speed = (self.p_speed * np.sign(total_x_component) * math.sqrt(total_x_component**2 + total_y_component**2))
            speed = self.kickOut(command_msg.drive.speed)
            # send to socket
            message = struct.pack("2f", speed, steering_angle)
            self.sockS.send(message)
        self.sockR.close()


    def kickOut(self, speed):
	self.speedHist = (self.speedHist * .75) + (abs(speed) * .25)
	print self.speedHist
	if self.speedHist < 0.2:
		return -1.0
	else:
		return speed
		
    pf = PotentialField()
    pf.scan_callback()
