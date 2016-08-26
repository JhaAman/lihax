import numpy as np
import matplotlib.pyplot as plt

def main():
    plt.ion()
    graph = plt.subplot(111, projection='polar')
    while True:
        theta_vals = []
        r_vals = []
        graph.clear()
        f = open("C:/Users/Jacob/workspace/lihax/Aggressive Simulator/Frame.txt")
        if "END" in f.readline():
            plt.ioff()
            break
        for data in f.readlines():
            theta_vals.append(np.deg2rad(float(data.split(',')[0]) + 90.0))
            r_vals.append(float(data.split(',')[1]))
        # graph.plot(theta_vals, r_vals)
        plt.scatter(theta_vals, r_vals)
        plt.draw()
        plt.pause(0.0001)
    print "Closing all windows... "
    plt.close('all')


if __name__=="__main__":
    main()