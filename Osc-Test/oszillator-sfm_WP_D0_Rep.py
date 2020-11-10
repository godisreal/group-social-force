"""
Implementation of SFM to investigate oscillations. 
"""
#-------------------------------------------------------------
# from numpy import *

import numpy as np
from numpy import *
import logging
import time
import matplotlib.pyplot as plt
from sys import *

#----------------------- Parameter ---------------------------------------

fps = 16      # frames per second
dt = 0.001    # [s] integrator step length
t_end = 10    # [s] integration time
N_ped = 3     # number of pedestrians
Length = 10   # [m] length of corridor. *Closed boundary conditions*
RK4 = 0       # 1 --> RK4. 0 --> Euler. Euler with very small dt converges to RK4.


#======================================================
# init (x_n, dx_n) for n=0 --> N-1
def init(N):

    shift = float(Length)/N
    x_n = 0.5*shift + shift*np.arange(N)
    dx_n = np.zeros(N)
    d0 = np.ones(N)*d0_init
     
    Fd = np.zeros(N)
    Fr = np.zeros(N)
    v0 = np.ones(N)*v0_init
    dd0 = np.zeros(N)

    #return np.vstack( [x_n, dx_n] ), Fd, Fr
    return np.vstack( [x_n, dx_n, d0] ), Fd, Fr, v0, dd0
#======================================================
# runge-kutta solver
def rk4(x, h, y, f):
    k1 = h * f(x, y)
    k2 = h * f(x + 0.5*h, y + 0.5*k1)
    k3 = h * f(x + 0.5*h, y + 0.5*k2)
    k4 = h * f(x + h, y + k3)
    return x + h, y + (k1 + 2*(k2 + k3) + k4)/6.0
#======================================================
def euler(t, h, y, f):
    y_new, Fd, Fr, v0, dd0 = f(t, y)
    return t + h, y + h * y_new, Fd, Fr, v0, dd0
#======================================================
#Not Used
def get_state_vars(state):
    """
    state variables and dist 
    """
    x_n = state[0,:]       # x_n  
    x_m = np.roll(x_n, -1)    # x_{n+1}
    x_m[ -1 ] += Length    # the first one goes ahead by Length
    dx_n = state[1,:]      # dx_n
    dx_m = np.roll(dx_n, -1)  # dx_{n+1}
    dist = x_m - x_n
    #d0 = state[2,:]
    return x_n, x_m, dx_n, dx_m, dist
#======================================================
def model(t, state):
    """
    exp-distance model nature 2000
    """
    #x_n, x_m, dx_n, dx_m, dist = get_state_vars(state)
    x_n = state[0,:]       # x_n  
    x_m = np.roll(x_n, -1)    # x_{n+1}
    x_m[ -1 ] += Length    # the first one goes ahead by Length
    dx_n = state[1,:]      # dx_n
    dx_m = np.roll(dx_n, -1)  # dx_{n+1}
    dist = x_m - x_n
    d0 = state[2,:]
    #v0 = m*(d0-dist)

    #print('d0:', d0, '\n')
    #(I, J) = np.shape(d0)
    #print('shape of d0:', (I, J), '\n')
    for i in range(0, len(v0)):
        if d0[i]-dist[i]<d_range and d0[i]-dist[i]>-d_range:
            v0[i] = v0[i] #k1*(d0[i]-dist[i]) + k3*(dx_m[i]-dx_n[i])  #v0[i] #-dd0[i]+
        else:
            v0[i] = v0[i]
    
    #get acceleration => sum of forces
    f_drv = (v0 - dx_n)/tau
    f_rep = -a*np.exp((d0-dist)/b) #*(d0-dist)
    #f_rep = -a*(v0+dx_m-dx_n)^2/dist

    Fd = f_drv
    Fr = f_rep

    ########################
    a_n = f_rep + f_drv
    ########################
    x_n_new = dx_n
    dx_n_new = a_n

    #dd0 = np.zeros(N)
    #dd0 = -0.2*(d0-dist)

    #(I, J) = np.shape(d0)
    for i in range(0, len(dd0)):
        if d0[i]-dist[i]<d_range and d0[i]-dist[i]>-d_range:
            dd0[i] = k2*(d0[i]-dist[i]) #k3*(dx_m[i]-dx_n[i])
        else:
            dd0[i] = 0.0

    x_n_new[-1] = 0   #ped 2 should not move
    dx_n_new[-1] = 0  #ped 2 should not move
    dd0[-1] = 0

    d0_new = dd0

    new_state = np.vstack([x_n_new, dx_n_new, d0_new])
    return new_state, Fd, Fr, v0, dd0

#======================================================
def simulation(N, t_end, state, Fd, Fr, v0, dd0):
    t = 0
    frame = 0
    ids = np.arange(N_ped)
    while t <= t_end:
        if frame%(1/(dt*fps)) < 1e-8: # one frame per second

            T = t*np.ones(N_ped)
            output = np.vstack([ids, T, state, Fd, Fr, v0, dd0]).transpose()
            np.savetxt(f, output, fmt="%d\t %f\t %f\t %f\t %f\t %f\t%f\t%f\t%f")
            f.flush()

        if RK4: # Runge-Kutta 4
            t, state = rk4(t, dt, state, model)
        else: # Euler
            t, state, Fd, Fr, v0, dd0 = euler(t, dt, state, model)

        frame += 1


#===================== MAIN =================================
if __name__=="__main__":
    b =3.6 #0.5 #0.08
    a = 2.4 #300 #2000
    tau = 0.5
    v0_init = 1.2
    d0_init = 0.6
    d_range = 1.8
    k1= 6.2
    k2= 0.0 #-1.8
    k3=3.0

    filename = "Rep_k3TestV0_traj_N%d_a%.2f_b%.2f_v0%.2f_d0%.2f_tau%.2f.txt"%(N_ped, a, b, v0_init, d0_init, tau) #trajectory file

    f = open(filename, 'w+')

    state, Fd, Fr, v0, dd0 = init(N_ped)

    t1 = time.clock()

    print 'filename ', filename
    constant = float(a)/b*(tau**2)
    if constant < 0.25:
        print 'No oscillations: constant = %.3f'%constant
    else:
        print 'Oscillations: constant = %.3f'%constant
     ######################################################
    simulation(N_ped, t_end, state, Fd, Fr, v0, dd0)
    ######################################################
    t2 = time.clock()
    f.close()


    #==========Plot the data============
    ms = 10
    fs = 20
    lw = 2
    file1 = filename
    print 'load file ',file1
    A1 = loadtxt(file1)#, delimiter=",")
    print 'finished loading'
    ids = unique(A1[:,0]).astype(int)
    frames = A1[:,1]
    print "ids=", ids
    Length = 200
    figname = file1.split(".txt")[0]+".pdf"
    for i in ids[::]:
        #print "i=",i
        p = A1[ A1[:,0] == i ]
        x1 = p[:,1] #time
        y1 = fmod(p[:,2], Length) #x
        abs_d_data = abs(diff(y1))
        abs_mean = abs_d_data.mean()
        abs_std = abs_d_data.std()
        if abs_std <=0.5*abs_mean:
            T = []
            plt.plot(x1, y1,'-r',lw=lw)
        else:
            T = nonzero(abs_d_data > abs_mean + 3*abs_std)[0] 
            start = 0
            for t in T:
                print "start=",start, "t=",t
                #plt.plot(y1[start:t], x1[start:t],'-k',ms=lw, lw=lw)
                plt.plot(x1[start:t],y1[start:t],'-k',ms=lw, lw=lw)
                start = t+1
            plt.plot(x1[start:],y1[start:],'-k',ms=lw, lw=lw)
            #plt.plot(y1[start:], x1[start:],'-k',ms=lw, lw=lw)
    plt.ylabel(r'$x_n\; \rm{[m]}$', size=20)
    plt.xlabel(r'$t\; \rm{[s]}$', size=20)

    plt.savefig(figname)
    print 'fgname: ', figname
    plt.show()
