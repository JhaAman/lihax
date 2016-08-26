import numpy as np
import matplotlib.pyplot as plt
import socket, struct, sys

def read_udp_data():
    speed_array = []
    angle_array = []
    # add more variable arrays here
    host_ip = socket.gethostname()
    port = 4510
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host_ip, port))
    while True:
        packet = sock.recvfrom(65565)[0]
        # print repr(packet)
        try:
            if struct.unpack("4s", packet)[0] == "STOP":
                print struct.unpack("4s", packet)[0]
                break
        except struct.error:
            try:
                print "Current Speed: " + str("%.2f" % struct.unpack("f", packet[0:4])[0])
                speed_array.append(float("%.2f" % struct.unpack("f", packet[0:4])[0]))
                print "Current Steering Angle: " + str("%.2f" % struct.unpack("f", packet[4:8])[0])
                angle_array.append(float("%.2f" % struct.unpack("f", packet[4:8])[0]))
            except struct.error:
                print "ERROR IN DECODING DATA"
    sock.close()
    print "Finished collecting data\nStarting data analysis... "
    learn(np.array(speed_array), np.array(angle_array))  # Enter the two sets of data you would like to analyze


def plot_data(x_vals, y_vals, t, ms, x_label="Population", y_label="Profit"):
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

def learn(xvals, yvals, degree=3, iterations=1500000, learning_rate=0.01):
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

if __name__=="__main__":
    read_udp_data()
    # learn()