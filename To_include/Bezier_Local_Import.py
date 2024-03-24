import numpy as np
import matplotlib.pyplot as plt

def Linear(t,P0,P1):
    return [((1-t)*P0[0])+(t*P1[0]),((1-t)*P0[1])+(t*P1[1])]

def Quadratic(t,P0,P1,P2):
    return [((1-t)*Linear(t,P0,P1)[0])+(t*Linear(t,P1,P2)[0]),((1-t)*Linear(t,P0,P1)[1])+(t*Linear(t,P1,P2)[1])]

def deriv_quad(t,P0,P1,P2):
    return [-2*(1-t)*P0[0]+P1[0]*(2*(1-t)-2*t)+2*t* P2[0],-2*(1-t)*P0[1]+P1[1]*(2*(1-t)-2*t)+2*t*P2[1]]

def deriv2_quad(t,P0,P1,P2):  
    return [2*(P0[0]-2*P1[0]+P2[0]),2*(P0[1]-2*P1[1]+P2[1])]

def Cubic(t,P0,P1,P2,P3):
    return [((1-t)*Quadratic(t,P0,P1,P2)[0])+(t*Quadratic(t,P1,P2,P3)[0]),((1-t)*Quadratic(t,P0,P1,P2)[1])+(t*Quadratic(t,P1,P2,P3)[1])]  

def deriv_cub(t,P0,P1,P2,P3):
    return [3*(1-t)*(1-t)*(P1[0]-P0[0]) + 6*(1-t)*t*(P2[0]-P1[0]) + 3*t*t*(P3[0]-P2[0]),3*(1-t)*(1-t)*(P1[1]-P0[1]) + 6*(1-t)*t*(P2[1]-P1[1]) + 3*t*t*(P3[1]-P2[1])]

def deriv2_cub(t,P0,P1,P2,P3):
    return [6*(1-t)*(P2[0]-2*P1[0]+P0[0]) + 6*t*(P3[0]-2*P2[0]+P1[0]),6*(1-t)*(P2[1]-2*P1[1]+P0[1]) + 6*t*(P3[1]-2*P2[1]+P1[1])]

def deriv_quad_dydx(t,eps,P0,P1,P2):
    return ((deriv_quad(t+eps,P0,P1,P2)[1]/deriv_quad(t+eps,P0,P1,P2)[0])-(deriv_quad(t,P0,P1,P2)[1]/deriv_quad(t,P0,P1,P2)[0]))/eps

def deriv_cub_dydx(t,eps,P0,P1,P2,P3):
    return ((deriv_cub(t+eps,P0,P1,P2,P3)[1]/deriv_cub(t+eps,P0,P1,P2,P3)[0])-(deriv_cub(t,P0,P1,P2,P3)[1]/deriv_cub(t,P0,P1,P2,P3)[0]))/eps

def De_Casteljaus_Pij(XY,i,j,t):                                                                       
    if i==0:                            
        return XY[j]    ## En supposant XY la liste des points de contrôles du polygone principal  
    else:                                                                                               
        return (De_Casteljaus_Pij(XY,i-1,j,t)[0]*(1-t)+t*(De_Casteljaus_Pij(XY,i-1,j+1,t)[0]),De_Casteljaus_Pij(XY,i-1,j,t)[1]*(1-t)+t*(De_Casteljaus_Pij(XY,i-1,j+1,t)[1]))

def pp_line(P0,a,b,N,sign,eps):
    P=[P0[0],P0[1]]
    Norm=0
    while Norm<N:
        P[0]=P[0] + sign*eps
        P[1]=a*P[0] + b
        Norm=((P[0]-P0[0])**(2) + (P[1]-P0[1])**(2))**(0.5)
    return P

def rac(i,x):
    return (x)**(1/i)

def abs(x) :
    if x<0 :
        return -x
    else :
        return x

def sign(x) :
    if x>0 :
        return 1
    else :
        return -1
    
def PI_Trajectory(x, eps, a, sign, x0, y0) :
    """
    sign = -1 : Counter Clock-Wise
    sign = 1 : Clock-Wise
    a : Parabol's width
    """
    return y0 - eps + (a*(x - x0) - sign*rac(2, eps))**2

def quicksort(L) :
    if (len(L) <= 1) :
        return L
    else :
        x = L[0]
        left = [y for y in L[1:] if y<x]
        right = [y for y in L[1:] if y>=x]
        return quicksort(left) + [x] + quicksort(right)
    
def topleft_center(t, size) :
    return (t[0] - size[0]/2, t[1] - size[1]/2)

def digitilizer(integer, bits) : 
    L = []
    mod, part = 0, integer
    for i in range(bits) :
        mod = part % 10
        part = part // 10
        L.append(mod)
    return L

