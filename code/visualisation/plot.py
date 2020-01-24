"""
plot.py

Tom Kamstra, Izhar Hamer, Julia Linde

Functions to plot the results with matplotlib
"""
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

def make_grid(layers, size):
    fig = plt.figure()
    ax = plt.axes(projection="3d")
    for i in range(layers): 
        GridX = np.linspace(0, size, (size + 1))
        GridY = np.linspace(0, size, (size + 1))
        X, Y = np.meshgrid(GridX, GridY)
        Z = (np.sin(np.sqrt(X ** 2 + Y ** 2)) * 0) + i
        # Plot grid
        # ax.plot_wireframe(X, Y, Z, lw=0.5,  color='grey')
    #configure axes
    ax.set_zlim3d(0, layers)
    ax.set_xlim3d(-1, size)
    ax.set_ylim3d(-1, size)

    return ax

# Enter coordinates as list with: [X, Y, Z]
def draw_line(crdFrom, crdTo, colour, ax):  
    Xline = [crdFrom[0], crdTo[0]]
    Yline = [crdFrom[1], crdTo[1]]
    Zline = [crdFrom[2], crdTo[2]]
    # Draw line
    print("LineFromTo",crdFrom , "To",crdTo, colour)
    ax.plot(Xline, Yline, Zline,lw=2,  color=colour, ms=12)

def set_gate(crd, ax):
    PointX = [crd[0]]
    PointY = [crd[1]]
    PointZ = [crd[2]]
    # s = str(1)
    # Plot points
    # ax.text(PointX, PointY, s, fontsize=12)
    # plt.text(60, .025, r'$\mu=100,\ \sigma=15$')

    # plt.text(PointX, PointY,  '1', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
    ax.plot(PointX, PointY, PointZ, ls="None", marker="o", color='red')
    # ax.plot(PointX, PointY, PointZ, ls="None", marker="$gate$", color='black')
