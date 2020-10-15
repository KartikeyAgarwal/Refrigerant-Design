import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import numpy as np
ca=[]
o=[]
cl=[]
h=[]
f=[]
n=[]
db=[]
rin=[]
#print("hello")
for p in range(12):
    for q in range(4):
        for r in range(6):
            for s in range(10):
                for t in range(9):
                  for u in range(2):
                    for v in range(2):
                      for w in range(2): 
                        print(p,q,r,s,t,u,v,w)
                        ca.append(p)
                        # ca.append(p)
                        o.append(q)
                        cl.append(r)
                        h.append(s)
                        f.append(t)
                        n.append(u)
                        db.append(v)
                        rin.append(w)
df=pd.read_excel("Features.xlsx")
dic={"carbon":ca,"oxygen":o,"chlorine":cl,"hydrogen":h,"fluorine":f,"nitrogen":n,"double":db,"rings":rin}
df1=pd.DataFrame(dic)    

input=[("scale",StandardScaler()),("polynomial",PolynomialFeatures(degree=3)),("model",LinearRegression())]
pipe=Pipeline(input)
pipe.fit(df[["C","Ox","Cl","Hy","Fl","N","DoubleBonds","NoofRings"]],df["Efficiency(COP)"])
yhat=pipe.predict(df1[["carbon","oxygen","chlorine","hydrogen","fluorine","nitrogen","double","rings"]])
max_eff=np.amax(yhat)
index = np.where(yhat == np.amax(yhat))
x = index[0][0]
print(max_eff)
print("carbon",ca[x],"oxygen",o[x],"chlorine",cl[x],"hydrogen",h[x],"fluorine",f[x],"nitrogen",n[x],"double",db[x],"rings",rin[x])
