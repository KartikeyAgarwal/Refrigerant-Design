import pandas as pd
from math import log 
import numpy as np
from scipy.optimize import fsolve

data1=pd.read_excel("all the data.xlsx")
columns=["cr_temp(K)","t_condensor","p_condensor","t_evaporator","pres_evap(Pa)","deltah_vap(J/mol)","omega","cr_pressure(Pa)"]

#P_c=float(input("Enter the value of Critical Pressure"))
T_c1=[]
t_condenser1=[]
p_condenser1=[]
t_evaporator1=[]
p_evaporator1=[]
delta_h_vap1=[]
w1=[]
P_c1=[]

for column in columns:
    if column=="cr_temp(K)":
        tc=data1[column].tolist()
        print(len(tc))
        for j in range(len(tc)):
            T_c1.append(tc[j])
    if column=="t_condensor":
        tcond=data1[column].tolist()
        for j in range(len(tcond)):
            t_condenser1.append(tcond[j])
    if column=="p_condensor":
        pcond=data1[column].tolist()
        for j in range(len(pcond)):
            p_condenser1.append(pcond[j])
    if column=="t_evaporator":
        tevap=data1[column].tolist()
        for j in range(len(tevap)):
            t_evaporator1.append(tevap[j])
    if column=="pres_evap(Pa)":
        pevap=data1[column].tolist()
        for j in range(len(pevap)):
            p_evaporator1.append(pevap[j])
    if column=="deltah_vap(J/mol)":
        delh=data1[column].tolist()
        for j in range(len(delh)):
            delta_h_vap1.append(delh[j])
    if column=="omega":
        omeg=data1[column].tolist()
        for j in range(len(omeg)):
            w1.append(omeg[j])
    if column=="cr_pressure(Pa)":
        crpres=data1[column].tolist()
        for j in range(len(crpres)):
            P_c1.append(crpres[j])


#T_c=float(input("Enter the value of Critical Temperature"))

#w=float(input("Enter the value of accentric factor"))

#p_condenser=float(input("Enter the value of Pressure after the condenser"))#Would be calculated by antoine equation but input would be given 

#p_evaporator=float(input("Enter the value of Pressure after the Evaporator"))#30 psig

#t_condenser=float(input("Enter the value of temperature after the condenser"))#80 F

#t_evaporator=float(input("Enter the value of temperature after the Evaporator"))#Again by antoine equation 

A=[]
B=[]
C=[]
D=[]
cop=[]
with open("coefficients_cp",'r') as file:
    for line in file:
        line=line.strip()
        space=line.split()
        A.append(space[0])
        B.append(space[1])
        C.append(space[2])
        D.append(space[3])
    
for i in range(len(T_c1)):
    T_c=T_c1[i]
    t_condenser=t_condenser1[i]
    p_condenser=p_condenser1[i]
    t_evaporator=t_evaporator1[i]
    p_evaporator=p_evaporator1[i]
    delta_h_vap=delta_h_vap1[i]
    a=float(A[i])
    b=float(B[i])
    c=float(C[i])
    d=float(D[i])
    w=w1[i]
    P_c=P_c1[i]
    P_r1=p_condenser/P_c
    
    T_r1=t_condenser/T_c
    
    P_r2=p_evaporator/P_c
    
    T_r2=t_evaporator/T_c
   # a=float(input("Enter the value of a"))
    #b=float(input("Enter the value of b"))
    #c=float(input("Enter the value of c"))
    #d=float(input("Enter the value of d"))
    
    #delta_h_vap=float(input("Enter the value of Enthalpy"))
    
    
    B01=0.083-0.422/(T_r1**1.6)
    
    B11=0.139-0.172/(T_r1**4.2)
    B02=0.083-0.422/(T_r2**1.6)
    
    B12=0.139-0.172/(T_r2**4.2)
    r=8.314
    Q_cold=5275.28
    
    
    
    
    
    def G_residual(pr,tr,b0,b1):
    	return (b0+w*b1)*(pr/tr)
    
    def H_residual(pc,tc,pr,tr,b0,b1,t):
    	H_r=((0.6752*(tc**1.6)/t**2.6 + 0.7224*(tc**4.2)*w/t**5.2)*(pr/tr) - ((b0+w*b1)*pr*tc/t**2))*t
    	return -H_r
    
    def delta_H_ig(a,b,c,d,t,t0):
        tou=t/t0
        r=8.314
        meanh=((a+b/2*t0*(tou+1)+ c/3*t0**2*(tou**2+tou+1) +d/(tou*t0**2))*r)*(t-t0)
        return meanh
    
    
    def S_residual(pc,tc,pr,tr,b0,b1,t):
    	S_r=r*(H_residual(pc,tc,pr,tr,b0,b1,t)-G_residual(pr,tr,b0,b1))
    	return S_r
    
    def delta_S_ig(a,b,c,d,p1,p2,t0,t1):
        S_ig= r*(a*log(t1/t0)+b*(t1-t0)+c*(t1**2-t0**2)/2- d/2*(1/t1**2-1/t0**2))+r*log(p1/p2)
        return S_ig
    
    
    #Expansion Valve and Evaporator combined
    delta_H_residual = r*t_evaporator*H_residual(P_c,T_c,P_r2,T_r2,B02,B12,t_evaporator)-r*t_condenser*(H_residual(P_c,T_c,P_r1,T_r1,B01,B11,t_condenser))
    
    delta_H_ig1=delta_H_ig(a,b,c,d,t_evaporator,t_condenser)
    
    m_dot=Q_cold/(delta_H_ig1+delta_H_residual+delta_h_vap)
    
    
    # Temperature calculation at the outlet of compressor
    
    def T_using_entropy(T):
    	t=T
    	T_r3=t/T_c
    	B03=0.083-0.422/(T_r3**1.6)
    	B13=0.139-0.172/(T_r3**4.2)
    	delta_S_ig1=delta_S_ig(a,b,c,d,p_evaporator,p_condenser,t_evaporator,t)
    	delta_S_residual=S_residual(P_c,T_c,P_r1,T_r3,B03,B13,t)-S_residual(P_c,T_c,P_r2,T_r2,B02,B12,t_evaporator)
    	f=delta_S_ig1+delta_S_residual
    
    	return f
    
    
    
    initialguess=330
    t_compressor1=fsolve(T_using_entropy,initialguess)
    t_compressor=t_compressor1[0]
    #print(t_compressor)
    T_r3=t_compressor/T_c
    B03=0.083-0.422/(T_r3**1.6)
    B13=0.139-0.172/(T_r3**4.2)
    
    #Calculating work input in compressor
    
    
    
    delta_H_residual_compressor=r*t_compressor*H_residual(P_c,T_c,P_r1,T_r3,B03,B13,t_compressor)-r*t_evaporator*(H_residual(P_c,T_c,P_r2,T_r2,B02,B12,t_evaporator))
    #print("H_residual(P_c,T_c,P_r1,T_r3,B03,B13,t_compressor):",H_residual(P_c,T_c,P_r1,T_r3,B03,B13,t_compressor))
    #print("(H_residual(P_c,T_c,P_r2,T_r2,B02,B12,t_evaporator)",(H_residual(P_c,T_c,P_r2,T_r2,B02,B12,t_evaporator)))
    delta_H_ig_compressor=delta_H_ig(a,b,c,d,t_compressor,t_evaporator)
    #print("value of no of moles:",m_dot)
    #print("Value of deltaH_ig_compressor:",delta_H_ig_compressor)
    #print("delta_H_residual_compressor:",delta_H_residual_compressor)
    W_compressor=m_dot*(delta_H_ig_compressor + delta_H_residual_compressor)
    
    
    COP=Q_cold/W_compressor
    cop.append(COP)
    
for i in range(len(cop)):
    print(cop[i])
    #print(cop[i],data1["compound"].tolist()[i] )



