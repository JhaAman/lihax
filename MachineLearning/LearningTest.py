import numpy as np
import matplotlib.pyplot as plt
import socket, struct
from SimUI import UI

def read_udp_data():
    ui = UI()
    speed_array = []
    angle_array = []
    lidar_distance_at_zero = []
    minimum_distance_at_frame = []
    percentage_below_distance = []  # currently set to 15 meters
    difference_between_right_and_left_min = []
    avg_difference_between_right_and_left = []
    # add more variable arrays here
    host_ip = socket.gethostname()
    portOne = 4510
    portTwo = 5520
    sockOne = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockTwo = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockOne.bind((host_ip, portOne))
    sockTwo.bind((host_ip, portTwo))
    while True:
        packetOne = sockOne.recv(6000)
        packetTwo = sockTwo.recv(6000)
        # print repr(packetOne)
        try:
            if struct.unpack("4s", packetOne)[0] == "STOP":
                print struct.unpack("4s", packetOne)[0]
                break
        except struct.error:
            pass
        try:
            print "Current Speed: %.2f" % struct.unpack("2f", packetOne)[0]
            speed_array.append(float("%.2f" % struct.unpack("2f", packetOne)[0]))
            print "Current Steering Angle: %.2f" % struct.unpack("2f", packetOne)[1]
            angle_array.append(float("%.2f" % struct.unpack("2f", packetOne)[1]))
        except struct.error:
            pass
        try:
            print "Distance In Front: %.2f" % struct.unpack("1080f", packetTwo)[539]
            lidar_distance_at_zero.append(float("%.2f" % struct.unpack("1080f", packetTwo)[539]))
        except struct.error:
            pass
        try:
            print "Minimum Distance: %.2f" % min(struct.unpack("1080f", packetTwo))
            minimum_distance_at_frame.append(float("%.2f" % min(struct.unpack("1080f", packetTwo))))
        except struct.error:
            pass
        try:
            print "Percentage of Pts Below Distance of 15m: %.2f" % (sum(i < 15 for i in struct.unpack("1080f", packetTwo))/len(struct.unpack("1080f", packetTwo)))
            percentage_below_distance.append(float("%.2f" % (sum(i < 15 for i in struct.unpack("1080f", packetTwo))/len(struct.unpack("1080f", packetTwo)))))
        except struct.error:
            pass
        try:
            print "Difference between min on right and left: %.2f" % (min(struct.unpack("1080f", packetTwo)[0:540])-min(struct.unpack("1080f", packetTwo)[540:1080]))
            difference_between_right_and_left_min.append(float("%.2f" % (min(struct.unpack("1080f", packetTwo)[0:540])-min(struct.unpack("1080f", packetTwo)[540:1080]))))
        except struct.error:
            pass
        try:
            print "Difference between mean distances on right and left: %.2f" % float(np.mean(struct.unpack("1080f", packetTwo)[0:540])-np.mean(struct.unpack("1080f", packetTwo)[540:1080]))
            avg_difference_between_right_and_left.append(float("%.2f" % float(np.mean(struct.unpack("1080f", packetTwo)[0:540])-np.mean(struct.unpack("1080f", packetTwo)[540:1080]))))
        except struct.error:
            pass

        print "--------------------------------------------------"

    sockOne.close()
    sockTwo.close()
    print "Finished collecting data\nStarting data analysis... "
    theta_speed = []
    theta_angle = []
    if ui.get_choice()[0] == "lidar_distance_at_zero":
        theta_speed = learn(np.array(speed_array), np.array(lidar_distance_at_zero))
    elif ui.get_choice()[0] == "minimum_distance_at_frame":
        theta_speed = learn(np.array(speed_array), np.array(minimum_distance_at_frame))
    elif ui.get_choice()[0] == "percentage_below_distance":
        theta_speed = learn(np.array(speed_array), np.array(percentage_below_distance))
    if ui.get_choice()[1] == "difference_between_right_and_left_min":
        theta_angle = learn(np.array(angle_array), np.array(difference_between_right_and_left_min))
    elif ui.get_choice()[1] == "avg_difference_between_right_and_left":
        theta_angle = learn(np.array(angle_array), np.array(avg_difference_between_right_and_left))
    theta_full = theta_speed + theta_angle
    move_car(theta_full)


def plot_data(y_vals, x_vals, t, ms, x_label="Population", y_label="Profit"):
    plt.plot(x_vals, y_vals, t, markersize=ms)
    plt.axis([0, max(x_vals) + 10, min(y_vals) - 10, max(y_vals) + 10])
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.autoscale()

def compute_cost(x_val_mat, y_val_mat, theta):
    m = y_val_mat.size
    H = theta * x_val_mat
    S = np.sum(np.asarray(H - y_val_mat)**2, axis=1)[0]
    return S/(2*m)  # J (cost) value

def gradient_descent(x_val_mat, y_val_mat, theta, iterations, alpha):
    print "Performing gradient descent... "
    m = y_val_mat.size
    for i in range(0, iterations):
        HY = (theta * x_val_mat) - y_val_mat
        SA = HY * x_val_mat.transpose()
        SA *= alpha/m
        theta = theta - SA
        if i%(iterations/100) == 0:
            print str((float(i)/float(iterations))*100)+"% finished... "
        if np.any(np.isnan(theta)):
            raise ValueError("Smaller learning rate needed!")
    return theta

def learn(xvals, yvals, degree=3, iterations=150000, learning_rate=0.01):
    succeeded = False
    theta = "0 "*degree + "0"
    theta = np.matrix(theta)
    # xvals, yvals = np.loadtxt("ex1data1.txt", delimiter=",", unpack=True)
    x_vals = [np.ones(len(xvals))]
    for d in range(1, degree+1):
        x_vals = np.append(x_vals, [xvals**d], axis=0)
    x_val_mat = np.matrix(x_vals)
    y_val_mat = np.matrix(yvals)
    plot_data(xvals, yvals, "rs", 6.0)
    cost = compute_cost(x_val_mat, y_val_mat, theta)
    print "Initial cost: " + str(cost)
    theta_new = theta
    while not succeeded:
        try:
            print "Current learning rate: " + str(learning_rate)
            theta_new = np.asarray(gradient_descent(x_val_mat, y_val_mat, theta, iterations, learning_rate))[0]
            print "Theta values found: " + str(theta_new)
            succeeded = True
        except ValueError:
            print "Learning rate too large, trying a smaller one... "
            learning_rate /= 10
    cost_new = compute_cost(x_val_mat, y_val_mat, theta_new)
    print "Final cost: " + str(cost_new)
    template = np.arange(0, max(xvals) + 10, 0.2)
    function = theta_new[0]
    for l in range(1, len(theta_new)):
        function += theta_new[l]*(template**l)
    plot_data(template, function, "b-", 6.0)
    print "Plotting data... "
    plt.show()
    return theta_new

def move_car(theta):
    ui = UI()
    host_ip = socket.gethostname()
    portReceive = 5520
    portSend = 6510
    sockReceive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockSend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockReceive.bind((host_ip, portReceive))
    sockSend.connect((host_ip, portSend))
    while True:
        packet = sockReceive.recv(6000)
        lidar_array = struct.unpack("1080f", packet)
        function = [0,0]
        if ui.get_choice()[0] == "lidar_distance_at_zero":
            var = lidar_array[539]
            function[0] = theta[0]
            for l in range(1, len(theta)/2):
                function[0] += theta[l] * (var ** l)
        elif ui.get_choice()[0] == "minimum_distance_at_frame":
            var = min(lidar_array)
            function[0] = theta[0]
            for l in range(1, len(theta)/2):
                function[0] += theta[l] * (var ** l)
        elif ui.get_choice()[0] == "percentage_below_distance":
            var = sum(i < 15 for i in lidar_array)/len(lidar_array)
            function[0] = theta[0]
            for l in range(1, len(theta)/2):
                function[0] += theta[l] * (var ** l)
        if ui.get_choice()[1] == "difference_between_right_and_left_min":
            var = min(lidar_array[0:540]) - min(lidar_array[540:1080])
            function[1] = theta[0]
            for l in range(len(theta)/2, len(theta)):
                function[1] += theta[l] * (var ** l)
        elif ui.get_choice()[1] == "avg_difference_between_right_and_left":
            var = float(np.mean(lidar_array[0:540])-np.mean(lidar_array[540:1080]))
            function[1] = theta[0]
            for l in range(len(theta)/2, len(theta)):
                function[1] += theta[l] * (var ** l)
        msg = struct.pack("2f", function[0], function[1])
        sockSend.send(msg)

if __name__=="__main__":
    read_udp_data()
    # learn()