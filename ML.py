import pandas as pd
ca=[]
o=[]
cl=[]
h=[]
f=[]
n=[]
db=[]
rin=[]
print("hello")
'''for p in range(16):
    for q in range(16):
        for r in range(16):
            for s in range(16):
                for t in range(16):
                    for u in range(16):
                        for v in range(16):
                            for w in range(16):'''
                               ca.append(p)
                               o.append(q)
                               cl.append(r)
                               h.append(s)
                               f.append(t)
                               n.append(u)
                               db.append(v)
                               rin.append(w)
                               
zipp=list(zip(ca,o,cl,h,f,n,db,r)) 
df=pd.DataFrame(zipp,columns=["carbon","oxygen","chlorine","hydrogen","fluorine","nitrogen","double","rings"])
print(df.head())