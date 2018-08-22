#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: ZhangYaoZhong
"""

import numpy as np
import matplotlib.pyplot as plt


class quard_copter(object):
    
    def __init__(self):
        self.Speed = np.zeros(3)
        self.Acc = np.zeros(3)
        self.Angle = np.zeros(3)
        self.dAngle = np.zeros(3)
        self.Force = np.zeros(4)
        self.pqr = np.zeros(3)
        self.dpqr = np.zeros(3)
        self.I = np.array([3.828,
                           3.828,
                           7.135])
        self.P = np.zeros(3)
        self.Mass = 0.4
        self.L = 0.205
#        self.sim_Counter = 0
        
    def set_speed(self,speed=np.random.rand(3)):
        self.Speed = speed   
    def set_acceleration(self,acc=np.random.rand(3)):
        self.Acc = acc     
    def set_location(self,loc=np.zeros(3)):
        self.P = loc
    def set_angle(self,angle=np.random.uniform(-0.04,0.04,3)):
        self.Angle = angle
    def set_dangle(self,dangle=np.zeros(3)):
        self.dAngle = dangle
    def set_pqr(self,pqr=np.random.uniform(-0.04,0.04,3)):
        self.pqr = pqr
    def set_I(self,I):
        self.I = I
    def set_dpqr(self,dpqr=np.random.rand(3)):
        self.dpqr = dpqr
    def set_Force(self,force=np.zeros(4)):
        self.Force = force
    def set_Mass(self,mass):
        self.Mass = mass
    def set_L(self,L):
        self.L = L

    def check_stable_stat(self,state):
        P,Speed,Angle,pqr = state
        phi_threshold = 0.1
        theta_threshold = 0.1
        safe_zone = np.array([5,5,5])
        
        done = np.abs(Angle[0]) > phi_threshold or\
               np.abs(Angle[1]) > theta_threshold or\
               np.abs(P[0]) > safe_zone[0] or \
               np.abs(P[1]) > safe_zone[1] or \
               np.abs(P[2]) > safe_zone[2]
        done = bool(done)
        
        if not done:
            reward = 1
        else:
            reward = 0
        
        return reward,done
    
    def step(self,Force,reward_fn=check_stable_stat,dt=0.01):
        self.Force = Force
        
        
        sins = np.sin(self.Angle)
        coss = np.cos(self.Angle)
        
        mass = self.Mass
        self.Acc[0] = np.sum(Force*(sins[0]*sins[2]+coss[0]*sins[1]*coss[2]))/mass
        self.Acc[1] = np.sum(Force*(-sins[0]*coss[2]+coss[0]*sins[1]*sins[2]))/mass
        self.Acc[2] = np.sum(Force*(coss[0]*coss[1]))/mass-9.8
        
        p,q,r = self.pqr
        self.dAngle[0] = (p*coss[1]+q*sins[0]*sins[1]+r*coss[0]*sins[1])/coss[1]
        self.dAngle[1] = q*coss[0]+r*sins[0]
        self.dAngle[2] = (q*sins[0]+r*coss[0])/coss[1]
        
        Ix,Iy,Iz = self.I
        L = self.L
        self.dpqr[0] = (L*(Force[3]-Force[1])+q*r*(Iy-Iz))/Ix
        self.dpqr[1] = (L*(Force[2]-Force[0])+p*r*(Iz-Ix))/Iy
        self.dpqr[2] = (L*(Force[1]+Force[3]-Force[0]-Force[2])+q*r*(Ix-Iy))/Iz
        
        self.P += self.Speed*dt
        self.Speed += self.Acc*dt
        self.Angle += self.dAngle*dt
        self.pqr += self.dpqr*dt
        
        state = [self.P,self.Speed,self.Angle,self.pqr]
        reward,done = reward_fn(self,state)
        
        return state,reward,done
    
    def reset(self):
        self.set_acceleration()
        self.set_angle()
        self.set_dangle()
        self.set_pqr()
        self.set_dpqr()
        self.set_speed()
        self.set_Force()
        self.set_location()
        
        state = [self.P,self.Speed,self.Angle,self.pqr]
        return state





