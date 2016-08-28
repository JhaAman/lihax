#!/usr/bin/env python

import math, socket, struct, numpy as np


# Get the gradient of the potential of an obstacle
# particle at (ox, oy) with the origin at (mx, my)


# Get the potential of an obstacle particle at (ox, oy)
# with the origin at (mx, my)
def potential(mx, my, ox, oy):
    1.0 / ((mx - ox)**2 + (my - oy)**2)**0.5

class PotentialField():
    def __init__(self):
        #socket initialization
        self.host_ip = socket.gethostname()
        self.receiving_port = 5510
        self.sending_port = 6510
        self.sockR = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockS = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockS.connect((self.host_ip, self.sending_port))
        self.sockR.bind((self.host_ip, self.receiving_port))
        
        # cumulative speed - used to build up momentum
        self.speed_c = 0
    def grad(self,dist, mx, my, ox, oy):
        c = -1/((mx - ox)**2 + (my - oy)**2)**1.5
        return c*(mx - ox), c*(my - oy)
    # calculate the total gradient from an array of lidar ranges
    # with origin at (my_x, my_y)
    def calc_gradient(self, ranges, my_x, my_y):
        gradient_x = 0 # sum of dU/dx
        gradient_y = 0 # sum of dU/dy
        
        # ignore the edges of the lidar FOV, usually noisy
        for i in range(len(ranges) - 180, 180, -1):
            r = ranges[i]
            deg = -(270.0/1080) * i # convert index of range to degree of range
            deg += 225 # lidar FOV starts at -45 deg
            px = r * math.cos(math.radians(deg)) # convert from polar to x coord
            py = r * math.sin(math.radians(deg)) # convert from polar to y coord
            gx, gy = self.grad(r, my_x, my_y, px, py) # compute gradient at rectangular coordinates
            
            # add point's gradient into sum
            gradient_x += gx
            gradient_y += gy
        
        return (gradient_x, gradient_y)
    
    # lidar subscriber callback
    def receive_lidar(self, STEER_BIAS=0, PUSH_MULTIPLIER=19.5, STEER_GRAD_PROPORTION=20.0, SPEED_GRAD_PROPORTION=-0.001, MOMENTUM_MU=0.95, UPDATE_INFLUENCE=0.11, REVERSE_SPEED_MULTIPLIER=-2.3, MIN_SPEED_CLAMP=-0.7, MAX_SPEED_CLAMP=1.0):
        
        while True:
            f = open("C:/Users/Jacob/workspace/lihax/Aggressive Simulator/Frame.txt")
            if "END" in f.readline():
                break
            packet = self.sockR.recvfrom(65565)[0]
            ranges = struct.unpack("1080f", packet)
    
            # compute gradient sums from lidar ranges
            grad_x, grad_y = self.calc_gradient(ranges, 0, 0)
        
            grad_x += STEER_BIAS * self.grad(0.1, 0, 0, 0.1, 0)[0]
            # place repelling particle behind origin (the car) to
            # push the car forward. 14 is a multiplier to give more push.
            grad_y += PUSH_MULTIPLIER * self.grad(0.1, 0, 0, 0, -0.1)[1]
            
            # magnitude of gradient (euclidian dist)
            grad_magnitude = math.sqrt(grad_x**2 + grad_y**2)
        
            # steering proportional to potential gradient w.r.t. x
            steer = grad_x / STEER_GRAD_PROPORTION # OR? math.atan2(grad_x, grad_y)
        
            # the speed update at this instance: proportional to gradient magnitude
            # and sign depends of sign of gradient w.r.t y
            speed = (SPEED_GRAD_PROPORTION * grad_magnitude * np.sign(grad_y))*100-194
        
            # update the cumulative momentum using the speed update at this instance.
            # speed_c is multiplied by some constant < 1 to simulate friction and
            # speed is multiplied by some constant > 0 to determine the influence of the
            # speed update at this instance.
            self.speed_c = MOMENTUM_MU*self.speed_c + UPDATE_INFLUENCE * speed
        
        
        
            # if speed is less than -1, clamp it. also, the steering is multiplied
            # by a negative constant < -1 to make it back out in a way that
            # orients the car in the direction it would want to turn if it were
            # not too close.
            speed_now = self.speed_c
            if self.speed_c < 0:
                if self.speed_c > -0.2:
                    speed_now = -0.7
                steer *= REVERSE_SPEED_MULTIPLIER
                print("reversing")
        
            if self.speed_c < MIN_SPEED_CLAMP:
                    speed_now = MIN_SPEED_CLAMP
            elif self.speed_c > MAX_SPEED_CLAMP:
                # if speed is greater than 1, clamp it
                    speed_now = MAX_SPEED_CLAMP

            # create and publish drive message using steer and speed_c
            # print "Speed: " + str(speed)
            # print "Speed c: " + str(self.speed_c)
            # print "Speed now: " + str(speed_now)
            message = struct.pack("2f", speed_now, -steer)
            self.sockS.send(message)

        self.sockR.close()
        self.sockS.close()


pf = PotentialField()
pf.receive_lidar()
