from Tkinter import *

class UI:

    def __init__(self):
        self.root = Tk()
        self.root.geometry("600x300")

        self.topFrame = Frame(self.root, width=600, height=200)
        self.topFrame.pack()
        self.middleFrame = Frame(self.root, width=600, height=200)
        self.middleFrame.pack()
        self.bottomFrame = Frame(self.root, width=600, height=200)
        self.bottomFrame.pack(side=BOTTOM)

        self.var1 = IntVar()
        self.var2 = IntVar()

        self.choice = []

        Label(self.topFrame, text="Choose a variable to compare against speed:").grid(row=0)
        Radiobutton(self.topFrame, text="lidar distance at zero", variable=self.var1, value=1).grid(row=1)
        Radiobutton(self.topFrame, text="minimum distance at frame", variable=self.var1, value=2).grid(row=2)
        Radiobutton(self.topFrame, text="percentage below distance", variable=self.var1, value=3).grid(row=3)
        Label(self.topFrame, text="Choose a variable to compare against steering:").grid(row=9)
        Radiobutton(self.middleFrame, text="difference between right and left min", variable=self.var2, value=1).grid(row=10)
        Radiobutton(self.middleFrame, text="average distance between right and left", variable=self.var2, value=2).grid(row=11)

        Button(self.bottomFrame, text="GO", command=self.callback).pack()

        self.root.mainloop()

    
    def getSpeedVar(self):
        if self.var1.get() == 1:
            return "lidar_distance_at_zero"
        elif self.var1.get() == 2:
            return "minimum_distance_at_frame"
        else:
            return "percentage_below_distance"

    def getSteeringVar(self):
        if self.var2.get() == 1:
            return "difference_between_right_and_left_min"
        else:
             return "avg_difference_between_right_and_left"

    def callback(self):
        self.root.destroy()
        self.choice = [self.getSpeedVar(), self.getSteeringVar()]
        return [self.getSpeedVar(), self.getSteeringVar()]

    def get_choice(self):
        return self.choice


ui = UI()
