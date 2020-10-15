import pandas as pd
from sklearn.preprocessing import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
df=pd.read_excel("Features.xlsx")
'''
lm=LinearRegression()
x_train,x_test,y_train,y_test=train_test_split(df[["C","Ox","Cl","Hy","Fl","N","DoubleBonds","NoofRings"]],df["Efficiency(COP)"],test_size=0.3,random_state=0)
Rsqu_test=[]
for n in range(1,12):
    pr=PolynomialFeatures(degree=n)
    x_train_pr=pr.fit_transform(x_train[["C","Ox","Cl","Hy","Fl","N","DoubleBonds","NoofRings"]])
    x_test_pr=pr.fit_transform(x_test[["C","Ox","Cl","Hy","Fl","N","DoubleBonds","NoofRings"]])
    lm.fit(x_train_pr,y_train)
    Rsqu_test.append(lm.score(x_test_pr,y_test))
print(x_test_pr)
print()
print(Rsqu_test)    
'''
input=[("scale",StandardScaler()),("polynomial",PolynomialFeatures(degree=3)),("model",LinearRegression())]
pipe=Pipeline(input)
pipe.train=(df["C","Ox","Cl","Hy","Fl","N","DoubleBonds","NoofRings"],df["Efficiency(COP)"])
yhat=


