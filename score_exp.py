import numpy as np
import pandas as pd

data = pd.read_excel('experience.xlsx')

total_rows=data['Experience'].count()

print (total_rows)

#for i in (1,total_rows):
data.fillna("none", inplace=True)    
data.head()


dic1={"Basic":1,"Intermediate":2,"Professional":3, "none":0}
data["SkillProficiency"]=data["SkillProficiency"].apply(lambda x : dic1[x])

dic2={"Implemented":2,"Acquired":1,"none":0}
data["Implementation"]=data["Implementation"].apply(lambda x: dic2[x])

data.head()


data.head()
for i in range(1,10):
    data["SkillProficiency."+str(i)]=data["SkillProficiency."+str(i)].apply(lambda x : dic1[x])
    data["Implementation."+str(i)]=data["Implementation."+str(i)].apply(lambda x: dic2[x])


score=[]

for i in range(0,total_rows):
    score.append(data["Implementation"].values[i]*data["SkillProficiency"].values[i]+
                 data["Implementation.1"].values[i]*data["SkillProficiency.1"].values[i]+
                 data["Implementation.2"].values[i]*data["SkillProficiency.2"].values[i]+
                 data["Implementation.3"].values[i]*data["SkillProficiency.3"].values[i]+
                 data["Implementation.4"].values[i]*data["SkillProficiency.4"].values[i]+
                 data["Implementation.5"].values[i]*data["SkillProficiency.5"].values[i]+
                 data["Implementation.6"].values[i]*data["SkillProficiency.6"].values[i]+
                 data["Implementation.7"].values[i]*data["SkillProficiency.7"].values[i]+
                 data["Implementation.8"].values[i]*data["SkillProficiency.8"].values[i]+
                 data["Implementation.9"].values[i]*data["SkillProficiency.9"].values[i])
                           
print(score)
#before taking into account the duration

for i in range(0,total_rows):
    score[i]*=data['Duration'].values[i]
    

net_dur =0
for i in range(0,total_rows):
    net_dur+=data['Duration'].values[i]
net_score=0
for i in range(0,total_rows):
    net_score+=score[i]
    
score

print(net_dur)
print(net_score)

Exp=net_score/net_dur
print("The net score of the student is",Exp)