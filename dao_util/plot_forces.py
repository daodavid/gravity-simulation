# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 15:51:54 2019

@author: David
"""






import matplotlib.pyplot as plt
from matplotlib import animation, rc
from IPython.display import HTML
from random import *
import numpy as np


def show_force_image():


    a = [1,1]
    b = [4,4]
    c = [-4,4]
    plt.scatter(a[0],a[1],color='black',linewidths=8)
    plt.scatter(b[0],b[1],color='black',linewidths=8)
    plt.scatter(c[0],c[1],color='black',linewidths=8)
    plt.quiver(a[0],a[1],c[0]-a[0],c[1]-a[1],width=0.01,scale=40,color='blue')
    
    plt.quiver(a[0],a[1],c[0]-a[0],c[1]-a[1],width=0.01,scale=40,color='blue')
    plt.text(a[0]-1,a[1]+1,r'$\vec F_{12}$',color = 'red',fontsize=20)
    
    plt.quiver(a[0],a[1],b[0]-a[0],b[1]-a[1],width=0.01,scale=40,color='blue')
    plt.text(a[0]+1,a[1]+1,r'$\vec F_{13}$',color = 'red',fontsize=20)
    
    
    plt.quiver(b[0],b[1],a[0]-b[0],a[1]-b[1],width=0.01,scale=40,color='blue')
    plt.text(b[0]-1,b[1]-1,r'$\vec F_{21}$',color = 'red',fontsize=20)
    
    plt.quiver(b[0],b[1],c[0]-b[0],c[1]-b[1],width=0.01,scale=40,color='blue')
    plt.text(b[0]-2.5,b[1],r'$\vec F_{23}$',color = 'red',fontsize=20)
    
    
    plt.quiver(c[0],c[1],a[0]-c[0],a[1]-c[1],width=0.01,scale=40,color='blue')
    plt.text(c[0]+1,c[1],r'$\vec F_{32}$',color = 'red',fontsize=20)
    
    plt.quiver(c[0],c[1],a[0]-c[0],b[1]-c[1],width=0.01,scale=40,color='blue')
    plt.text(c[0],c[1]-1,r'$\vec F_{31}$',color = 'red',fontsize=20)
    
    ax = plt.gca()
    plt.axis('equal')
    
    
    plt.show