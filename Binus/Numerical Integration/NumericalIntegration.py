# Written by: Callista Roselynn, Clarissa Indriyani, Claudia Rachel

# Modules Used:

# importing everything in the tkinter module
from tkinter import *
# from tkinter import filedialog

# ttk stands for themed tkinter.
# Used to improve the aesthetic of buttons & widgets
from tkinter import ttk

# used to show a pop up window
import tkinter.messagebox
import tkinter.simpledialog

# used to load images
from PIL import Image

# used to plot and calculate
import math
from sympy import *
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

# ----------------------------------------------------------------- #
# Creating a window

window = Tk()
# window.get_themes()  # Returns a list of all themes that can be set
# window.set_theme("clearlooks")  # Sets the theme

# changing the bg color of the window
window.configure(background="white")

# changing the title of the window
window.title("Numerical Integration Calculator")

# ----------------------------------------------------------------- #
# Creating the statusbar

# SUNKEN makes it look like a button
# anchor parameter provides the location of the text
# side parameter of pack is for the orientation and differentiates it from text
# fill parameter expands the status bar to either ends of the window

statusbar = ttk.Label(window, text="Welcome :)", relief=SUNKEN, font=("Times New Roman", 14, "italic"))
# statusbar.configure(bg="#b8d2d5")
statusbar.pack(side=BOTTOM, fill=X)

# Creating the menu bar

menubar = Menu(window)
# ensures that the menu bar appears at the top and prepares the menubar so it can receive submenus
window.config(menu=menubar)


# ----------------------------------------------------------------- #
# Creating functions for the submenu
# Might put in class to make it more uniformed - lets see if we hep time hohoho

class Actions:
    def about(self):
        tkinter.messagebox.showinfo("About this project", "This is a Semester 2 project which is aimed to help other people get a better understanding on Numerical integration.")

    def inProgress(self):
        tkinter.messagebox.showinfo("This feature is currently under maintainace.\n Sorry for any inconvenience.")

    def trapBG(self):
        # Reading the image
        self.img = Image.open("/Users/bella/PycharmProjects/Numerical Integration/background/Trapezoid.png")

        # Showing the image
        self.img.show()

    def simpsonBG(self):
        # Reading the image
        self.img = Image.open("/Users/bella/PycharmProjects/Numerical Integration/background/Simpson.png")

        # Showing the image
        self.img.show()

    def gaussianBG(self):
        # Reading the image
        self.img = Image.open("/Users/bella/PycharmProjects/Numerical Integration/background/Quadrat.png")

        # Showing the image
        self.img.show()

    # Creating other functions for buttons

    # To clear all the fields
    def reset(self):
        eq.set("")
        upL.set("")
        lowL.set("")
        inter.set("")
        result.set("")
        return

    def quitting(self):
        window.quit()
        window.destroy()

# ----------------------------------------------------------------- #
# Creating the Functions class to
# contains the commands for the buttons

a = eval(input("Enter lower limit: "))
b = eval(input("Enter upper limit: "))
n = eval(input("Enter number of interval: "))
func = "1 - x - 4x^3 + 2x^5"
area = 0

class Functions:
    def __init__(self):
        self.statusbar = statusbar
        self.area = area
        self.a = a
        self.b = b
        self.n = n
        self.func = "1 - x - 4x^3 + 2x^5"
        self.area = 0
        self.relativeTError = 0
        self.cList = [[], [1.0, 1.0], [0.55555, 0.88888, 0.55555], [0.34785, 0.65214, 0.65214, 0.34785],
                 [0.23692, 0.47862, 0.56888, 0.47862, 0.23692], [0.17132, 0.36076, 0.46791, 0.46791, 0.36076, 0.17132]]

        self.xList = [[], [-0.57735, 0.57735], [-0.77459, 0.0, 0.77459], [-0.86113, -0.33998, 0.33998, 0.86113],
                 [-0.93246, -0.53846, 0.0, 0.53846, 0.90617], [-0.93246, -0.66120, -0.23861, 0.23861, 0.66120, 0.93246]]

    def f(self, x):
        return 1 - x - 4 * x ** 3 + 2 * x ** 5

    def actual(self):
        return self.Df(b) - self.Df(a)

    def Df(self, x):
        return x - (x**2 / 2) - (x ** 4) + (x ** 6 /3)

    # f = np.vectorize(func)

    def trapezoid(self, a, b, n):

        # Grid spacing
        h = (b - a) / n

        # Compute firsts and last term
        s = (self.f(a) + self.f(b))
        i = 1
        while i < n:
            s += 2 * self.f(a + i * h)
            i += 1

        self.area = ((h / 2) * s)
        return self.area

    def simpson13(self, a, b, n):
        # Calculating the value of h
        h = (b - a) / n

        # List for storing value of x and f(x)
        x = []
        fx = []

        # Calcuting values of x and f(x)
        i = 0
        while i <= n:
            x.append(a + i * h)
            fx.append(self.f(x[i]))
            i += 1

        # Calculating result
        res = 0
        i = 0
        while i <= n:
            if i == 0 or i == n:
                res += fx[i]
            elif i % 2 != 0:
                res += 4 * fx[i]
            else:
                res += 2 * fx[i]
            i += 1
        self.area = res * (h / 3)
        return self.area

    def simpson38(self, a, b, n):
        interval_size = (float(b - a) / n)
        sum = self.f(a) + self.f(b);

        # Calculates value till integral limit
        for i in range(1, n):
            if (i % 3 == 0):
                sum = sum + 2 * self.f(a + i * interval_size)
            else:
                sum = sum + 3 * self.f(a + i * interval_size)

        self.area = ((float(3 * interval_size) / 8) * sum)
        return self.area

    def gaussQuad(self, a, b, n):
        n = n - 1
        s = 0
        c1 = (b - a) / 2
        c2 = (b + a) / 2
        for i in range(len(self.cList[n])):
            s = s + (c1 * self.cList[n][i] * self.f(c1 * self.xList[n][i] + c2))

        return s

    def graphIntegral(self):
        x = np.linspace(-1, self.b + 1, 100)
        plt.plot(x, self.f(x))
        plt.axhline(color="black")
        plt.fill_between(x, self.f(x), where=[(x > self.a) and (x < self.b) for x in x], color='blue', alpha=0.3)
        plt.show()

    def y(self, x, a, b):
        global xs
        xs = np.linspace(a, b, 100)
        return 1 - x - 4 * x ** 3 + 2 * x ** 5

    # TRAPEZOID
    """""
    def graphTrapezoid(self, f, xs):
        x_range = []
        y_range = []
        resultst = []

        for x in xs:
            x_range.append(x)
            y_range.append(f(x))
            integral = integrate.trapz(y_range, x_range, 1)
            resultst.append(integral)

        return resultst
    """

    def tgraph(self):
        x = np.linspace(self.a, self.b, n+1)
        y = self.f(x)
        plt.plot(x, y)

        for i in range(n):
            xs = [x[i], x[i], x[i+1], x[i+1]]
            ys = [0, self.f(x[i]), self.f(x[i+1]), 0]
            plt.fill(xs, ys, "b", edgecolor="b", alpha=0.2)

        plt.title("Trapezoid Rule, N = {}".format(n))
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()


    def calculateTrapezoid(self):
        self.area = self.trapezoid(self.a, self.b, self.n)
        result.set(self.area)

        terror = self.trapezoidError(self.a, self.b)
        trueError.set(terror)

        relTrueError = self.relativeError(terror)
        print(relTrueError)
        relativeTrueError.set(relTrueError)

        self.statusbar["text"] = "calculating area using trapezoidal rule..."
        return

    # SIMPSON
    def graphSimpson(self, f, xs):
        x_range = []
        y_range = []
        resultss = []
        for x in xs:
            x_range.append(x)
            y_range.append(f(x))
            integral = integrate.simps(y_range, x_range, 1)
            self.resultss.append(integral)
        return results

    def sgraph(self):
        xs = np.linspace(self.a, self.b, 100)
        plt.plot(xs, self.graphSimpson(lambda x: self.y(x, self.a, self.b), xs))
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()

    def calculateSimpson13(self):
        self.area = self.simpson13(self.a, self.b, self.n)
        result.set(self.area)

        s13error = self.simpson13Error(self.a, self.b)
        trueError.set(s13error)

        relTrueError = self.relativeError(s13error)
        print(relTrueError)
        relativeTrueError.set(relTrueError)

        self.statusbar["text"] = "calculating area using Simpson's 1/3 rule..."
        return

    def calculateSimpson38(self):
        self.area = self.simpson38(self.a, self.b, self.n)
        result.set(self.area)

        s38error = self.simpson38Error(self.a, self.b)
        trueError.set(s38error)

        relTrueError = self.relativeError(s38error)
        print(relTrueError)
        relativeTrueError.set(relTrueError)

        self.statusbar["text"] = "calculating area using Simpson's 3/8 rule..."
        return

    # GAUSSIAN
    def calculateQuadrature(self):
        self.area = self.gaussQuad(self.a, self.b, self.n)
        result.set(self.area)

        gerror = self.gaussQuadError(self.a, self.b)
        trueError.set(gerror)

        relTrueError = self.relativeError(gerror)
        print(relTrueError)
        relativeTrueError.set(relTrueError)

        self.statusbar["text"] = "calculating area using Gaussian Quadrature..."
        return

    # Relative True Error

    def trapezoidError(self, a, b):
        A = self.actual() # True Value
        B = self.trapezoid(a, b, n) # Approx Value
        return abs((A - B) * 10 ** -6)

    def simpson13Error(self, a, b):
        A = self.actual()  # True Value
        B = self.simpson13(a, b, n)
        return abs((A - B) * 10 ** -6)

    def simpson38Error(self, a, b):
        A = self.actual()  # True Value
        B = self.simpson38(a, b, n)
        return abs((A - B) * 10 ** -6)

    def gaussQuadError(self, a, b):
        A = self.actual() # True Value
        B = self.gaussQuad(a, b, n)
        return abs((A - B) * 10 ** -6)

    def relativeError(self, trueError):
        A = self.actual()  # True Value
        self.relativeTError = (trueError / A) * 100
        return self.relativeTError



# ----------------------------------------------------------------- #
# Creating the submenu

subMenu = Menu(menubar, tearoff=0)  # using menubar instead of window to differentiate the two types of menu
menubar.add_cascade(label="File", menu=subMenu)  # cascade = dropdown menu
subMenu.add_command(label="About", command=Actions().about)
subMenu.add_command(label="Reset", command=Actions().reset)
subMenu.add_command(label="Force Quit", command=window.destroy)

subMenu = Menu(menubar, tearoff=0)  # using menubar instead of window to differentiate the two types of menu
menubar.add_cascade(label="Trapezoidal", menu=subMenu)  # cascade = dropdown menu
subMenu.add_command(label="Calculate", command=Functions().calculateTrapezoid)
subMenu.add_command(label="Graph", command=Functions().tgraph)
subMenu.add_command(label="Background", command=Actions().trapBG)

subMenu = Menu(menubar, tearoff=0)  # using menubar instead of window to differentiate the two types of menu
menubar.add_cascade(label="Simpson's 1/3", menu=subMenu)  # cascade = dropdown menu
subMenu.add_command(label="Calculate", command=Functions().calculateSimpson13)
subMenu.add_command(label="Graph", command=Actions().inProgress)
subMenu.add_command(label="Background", command=Actions().simpsonBG)

subMenu = Menu(menubar, tearoff=0)  # using menubar instead of window to differentiate the two types of menu
menubar.add_cascade(label="Simpson's 3/8", menu=subMenu)  # cascade = dropdown menu
subMenu.add_command(label="Calculate", command=Functions().calculateSimpson38)
subMenu.add_command(label="Graph", command=Actions().inProgress)
subMenu.add_command(label="Background", command=Actions().simpsonBG)

subMenu = Menu(menubar, tearoff=0)  # using menubar instead of window to differentiate the two types of menu
menubar.add_cascade(label="Gaussian", menu=subMenu)  # cascade = dropdown menu
subMenu.add_command(label="Calculate", command=Functions().calculateQuadrature)
subMenu.add_command(label="Graph", command=Actions().inProgress)
subMenu.add_command(label="Background", command=Actions().gaussianBG)

# ----------------------------------------------------------------- #
# Creating the Top Frame
# Contains the textfield to prompt user to input the equation

topFrame = Frame(window)
topFrame.configure(background="white")
topFrame.pack(padx=10, pady=5)

eq = StringVar()
upL = StringVar()
lowL = StringVar()
inter = StringVar()
result = StringVar()
trueError = StringVar()
relativeTrueError = StringVar()

equationLabel = Label(topFrame, text="Function: ")
equationLabel.grid(row=0)
equation = Entry(topFrame, width=30, textvariable=eq)
equation.grid(row=0, column=1)

upperLabel = Label(topFrame, text="Upper Limit: ")
upperLabel.grid(row=1, column=0)
upperLimit = Entry(topFrame, width=30, textvariable=upL)
upperLimit.grid(row=1, column=1)

lowerLabel = Label(topFrame, text="Lower Limit: ")
lowerLabel.grid(row=2, column=0)
lowerLimit = Entry(topFrame, width=30, textvariable=lowL)
lowerLimit.grid(row=2, column=1)

intervalLabel = Label(topFrame, text="Intervals: ")
intervalLabel.grid(row=3, column=0)
intervals = Entry(topFrame, width=30, textvariable=inter)
intervals.grid(row=3, column=1)

resultLabel = Label(topFrame, text="Area after Integration: ")
resultLabel.grid(row=4, column=0)
results = Entry(topFrame, width=30, text=result)
results.grid(row=4, column=1)

trueErrorLabel = Label(topFrame, text="True Error: ")
trueErrorLabel.grid(row=5, column=0)
trueErrors = Entry(topFrame, width=30, text=trueError)
trueErrors.grid(row=5, column=1)

relativeTrueErrorLabel = Label(topFrame, text="Relative True Error: ")
relativeTrueErrorLabel.grid(row=6, column=0)
relativeTrueErrors = Entry(topFrame, width=30, text=relativeTrueError)
relativeTrueErrors.grid(row=6, column=1)


eq.set(func)
upL.set(b)
lowL.set(a)
inter.set(n)

# ----------------------------------------------------------------- #

# Creating the Button Frame for the different methods of Integration

# Button frame contains the play, pause and stop Music buttons
# Acts as a grouper so whatever you edit on this frame will not affect the entire window
# pad parameter creates space for the three buttons
# grid system automatically gives space on the sides so no need for padx

buttonFrame = Frame(window, relief=RAISED)
buttonFrame.configure(background="white")
buttonFrame.pack(pady=5)

graphButton = Button(buttonFrame, text="Graph", command=Functions().graphIntegral)
graphButton.grid(row=1, column=10)

# ----------------------------------------------------------------- #
# Quits the window without giving error

# protocol handler tells the x button what to do
window.protocol("WM_DELETE_WINDOW", Actions().quitting)

# makes sure the window doesn't disappear
window.mainloop()
