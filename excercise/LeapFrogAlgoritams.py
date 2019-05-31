import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani


"""
Leap Frog Algoritams

http://faculty.smu.edu/shampine/stablemidpoint.pdf

"""

def leapFrog(u, v, x0, y0, vx_0, vy_0, n=1000, h=0.1,c = 1):
    """
    solving 4 order system ode
        see  #https://people.ucsc.edu/~mmrosent/talks_notes/num_int_pres.pdf
    :param u:  u = u(t,x,y) = e1
    :param v:   u = v(t,x,y) = e2
    :param x0:
    :param y0:
    :param vx_0:
    :param vy_0:
    :param n:  numbet of step
    :param h:  step
    :param c = can be some constant as mass
    :return:
    """

    x = x0
    y = y0
    vx = vx_0
    vy = vy_0
    t = 0
    y_args = [y]  # y_args array for y arguments
    x_args = [x]  # x_args array for arguments
    t_args = [t]  # time interval
    x_speed = [vx]
    y_speed = [vy]

    for i in range(n):
        x = x + vx * (h / 2)/c
        y = y + vy * (h / 2)/c

        vx = (vx + h * u(t, x, y))/c
        vy = (vy + h * v(t, x, y))/c

        x = x + vx * (h / 2)
        y = y + vy * (h / 2)

        t = t + h
        x_speed.append(vx)
        y_speed.append(vy)
        t_args.append(t)
        x_args.append(x)
        y_args.append(y)
    return np.array([x_args, y_args, x_speed, y_speed, t_args]).T
