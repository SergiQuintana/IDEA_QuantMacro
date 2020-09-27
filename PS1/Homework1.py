# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 09:05:10 2020

@author: Sergi
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression
import os
os.chdir(r'C:\Users\Sergi\Desktop\Universitat\Master\Second Year\Quantitative Macroeconomics\Problem Sets\PS1')
#Read the data:
data= pd.read_csv(r'C:\Users\Sergi\Desktop\Universitat\Master\Second Year\Quantitative Macroeconomics\Problem Sets\PS1\Data_1.txt')

#Generate a dummy variable to see if employed or not:
emp_map = {10:1,
           12:1,
           21:0,
           22:0
    } #This generates an instruction to then do the mapping.

data ["EMPLOYMENT"]=data["EMPSTAT"].map(emp_map) #This does a mapping following the instruction

#This computes the employment rate for each month:
employment= data.groupby(["YEAR","MONTH"])["EMPLOYMENT"].mean()

#ANOTHER WAY OF DOING GRAPHS:
#emp_rate = pd.DataFrame(employment)
#emp_rate["Date"]= pd.date_range(start='2018/01/01', periods=32, freq='M')
#emp_rate.plot(x="Date",y="EMPLOYMENT" ,linewidth=2.0, label ="Real" )


#This is the employment rate during 2018-2019 (2020 excluded)
employment_no2020 = employment[employment.index.get_level_values('YEAR') <= 2019]

#To detrend and deseasonalize the data we will compute the average of 2018/2019
#as a predicted value for 2020
#Compute the average monthly employment rate of 2018 and 2019
no2020 = data.loc[data['YEAR'] <= 2019] #Create a dataframe without 2020

#Change the year name for 2020, since we will want the predicted: 
no2020.loc[no2020['YEAR']<2020,'YEAR'] = 2020

predicted_2020=no2020.groupby(["YEAR","MONTH"])["EMPLOYMENT"].mean()



# Here I take the actual data with 2020 removed and merge it with predicted values. 
#So employment_no2020 is the same as employment until 2020 where I have replaced the 2020 values with the predicted ones. 
#Since the 2018-2019 values are the same you can plot the two series over each other and they will depart at 2020. 

employment_predicted = pd.concat([employment_no2020, predicted_2020])

    
#Plot monthly employment rate:


fig,ax = plt.subplots()

employment_predicted.plot(label="Predicted Employment Rate")
employment.plot(label="Real Employment Rate")

plt.xlabel('Time')
plt.ylabel('Monthly Employment Rate')
plt.legend()
plt.title ('Impact of Covid on Monthly Employment Rate (US)')
plt.show()
#Notice that if I were able to drop some values I could do it better....

######################ANOTHER WAY########################
#Trans forms the Series into DataFrames:
    #emp_predicted = pd.DataFrame(employment_predicted)
    #emp = pd.DataFrame (employment)
    #emp_predicted["Date"]= pd.date_range(start='2018/01/01', periods=36, freq='M')
    #emp["Date"]= pd.date_range(start='2018/01/01', periods=32, freq='M')
    #fig,ax = plt.subplots()
    #emp_predicted.plot(y="EMPLOYMENT",x="Date",label="Predicted Employment Rate")
    #emp.plot(y="EMPLOYMENT",label="Real Employment Rate")
    

##############################################################################
#Redo the computations by education level:

##Generate the different education groups:
#To do so I will now generate column that will be used to group by education level 
data["EDU_GROUP"]="" #Generates an empty column
data.loc[data["EDUC"] <= 72,"EDU_GROUP"] = 1 #EDU_GROUP=NO_HS if no highschool
data.loc[data["EDUC"] == 73,"EDU_GROUP"] = 2 #EDU_GROUP=HS if HS.
data.loc[(data["EDUC"] > 73) & (data["EDUC"]<111),"EDU_GROUP"] = 3 #EDU_GRUP=LESS_BD if less than Bachelor
data.loc[data["EDUC"] == 111,"EDU_GROUP"] = 4 #EDU_GROUP=BD if Bachelor Degree
data.loc[data["EDUC"]>=123 ,"EDU_GROUP"] = 5#EDU_GROUP=MORE_BD if more than Bachelor

emp_education= data.groupby(["YEAR","MONTH","EDU_GROUP"])["EMPLOYMENT"].mean() #group averaging employment
education = pd.DataFrame(emp_education)
indexs=["No_HighSchool", "HighSchool", "Less_BachelorDegree", "BachelorDegree", "More_BachelorDegree"]
education["indexs"]=indexs*32
#Since the order is Years, Month and Group, we will find that once created the
#Series is ordered as Year x, MOnth x, group 1 ,2 3,.... . Therefore, by creating an index 
#it will match each group. 

dates= pd.date_range(start='2018/01/01', periods=32, freq='M')
fig, ax = plt.subplots(facecolor="w")
for index in indexs:
    edu_level = education[education["indexs"] == index]
    ax.plot(dates, edu_level["EMPLOYMENT"], label=f"{index}")
plt.xticks(rotation=45)
ax.set_ylabel("Employment Rate")
plt.title("Employment Rate by Education Level")
plt.legend()
plt.show()

##############################################################################
#Redo the computations for Occupation levels
##Create the differenet class of workers:
workers_key={13:1,
             14:1,
             21:2,
             22:2,
             23:2,
             24:3,
             25:3,
             26:3,
             27:3,
             28:3,
             29:4}
#Classes are as follows: 
    #1-->Self-employed
    #2-->Private employed
    #3-->Government employed
    #4-->Unpaid family worker
#Use the Key to generate a new variable on the DataFrame:
data["OCCU_CLASS"]=data["CLASSWKR"].map(workers_key)

#Now group by Occupation class:
ocup = data.groupby(["YEAR","MONTH","OCCU_CLASS"])["EMPLOYMENT"].mean()
ocup_emp = pd.DataFrame(ocup)

#Generate a reference to call for each class:
refs=["Self_Employed","Private_Employed","Government_Employed","Family_Worker"]
ocup_emp["refs"]=refs*32

#Plot the Figure:
fig, ax = plt.subplots(facecolor="w")
for ref in refs:
    ocu_group = ocup_emp[ocup_emp["refs"] == ref]
    ax.plot(dates, ocu_group["EMPLOYMENT"], label=f"{ref}")
plt.xticks(rotation=45)
ax.set_ylabel("Employment Rate")
plt.title("Employment Rate by Occupation Class")
plt.legend()
plt.show()

##############################################################################
#Redo for Industry levels:
key_telework={170:0,
              180:0,
              190:0,
              270:0,
              280:0,
              290:0,
              370:0,
              390:0,
              470:0,
              490:0,
              770:0,
              1070:0,
              1080:0,
              1090:0,
              1170:0,
              1180:0,
              1190:0,
              1270:0,
              1280:0,
              1290:0,
              1370:0,
              1470:0,
              1480:0,
              1490:0,
              1570:0,
              1590:0,
              1670:0,
              1680:0,
              1690:0,
              1770:0,
              1790:0,
              3770:0,
              3780:0,
              3790:0,
              3875:0,
              1870:0,
              1880:0,
              1890:0,
              1990:0,
              2070:0,
              2090:0,
              2170:0,
              2180:0,
              2190:0,
              2270:0,
              2280:0,
              2290:0,
              2370:0,
              2380:0,
              2390:0,
              2470:0,
              2480:0,
              2490:0,
              2590:0,
              2670:0,
              2680:0,
              2690:0,
              2770:0,
              2780:0,
              2790:0,
              2870:0,
              2880:0,
              2890:0,
              2970:0,
              2980:0,
              2990:0,
              3070:0,
              3080:0,
              3095:0,
              3170:0,
              3180:0,
              3190:0,
              3365:0,
              3370:0,
              3380:0,
              3390:0,
              3470:0,
              3490:0,
              3570:0,
              3580:0,
              3590:0,
              3670:0,
              3680:0,
              3690:0,
              3895:0,
              3960:0,
              3970:0,
              3980:0,
              3990:0,
              4070:0,
              4080:0,
              4090:0,
              4170:0,
              4180:0,
              4195:0,
              4265:0,
              4270:0,
              4280:0,
              4290:0,
              4370:0,
              4380:0,
              4390:0,
              4470:0,
              4480:0,
              4490:0,
              4560:0,
              4570:0,
              4580:0,
              4585:1,
              4590:1,
              4670:0,
              4680:0,
              4690:0,
              4770:0,
              4780:0,
              4795:0,
              4870:0,
              4880:0,
              4890:0,
              4970:0,
              4980:0,
              4990:0,
              5070:0,
              5080:0,
              5090:0,
              5190:0,
              5275:0,
              5280:0,
              5295:0,
              5370:0,
              5380:0,
              5390:0,
              5470:0,
              5480:0,
              5490:0,
              5570:0,
              5580:0,
              5590:1,
              5591:1,
              5592:1,
              5670:0,
              5680:1,
              5690:0,
              5790:0,
              6070:0,
              6080:0,
              6090:0,
              6170:0,
              6180:0,
              6190:0,
              6270:0,
              6280:0,
              6290:0,
              6370:0,
              6380:0,
              6390:0,
              570:0,
              580:0,
              590:0,
              670:0,
              680:0,
              690:0,
              6470:1,
              6480:1,
              6490:1,
              6570:0,
              6590:0,
              6670:1,
              6672:1,
              6680:1,
              6690:1,
              6695:1,
              6770:0,
              6780:1,
              6870:1,
              6880:1,
              6890:1,
              6970:1,
              6990:1,
              7070:1,
              7080:1,
              7170:1,
              7180:1,
              7190:1,
              7270:1,
              7280:1,
              7290:1,
              7370:1,
              7380:1,
              7390:1,
              7460:1,
              7470:1,
              7480:0,
              7490:0,
              7570:1,
              7580:1,
              7590:1,
              7670:1,
              7680:1,
              7770:1,
              7780:1,
              7790:0,
              7860:1,
              7870:1,
              7880:1,
              7890:1,
              7970:0,
              7980:0,
              7990:0,
              8070:0,
              8080:0,
              8090:0,
              8170:0,
              8180:0,
              8190:0,
              8270:0,
              8290:0,
              8370:0,
              8380:0,
              8390:0,
              8470:0,
              8560:0,
              8570:0,
              8580:0,
              8590:0,
              8660:0,
              8670:0,
              8680:0,
              8690:0,
              8770:0,
              8780:0,
              8790:0,
              8870:0,
              8880:0,
              8970:0,
              8990:0,
              9070:0,
              9080:0,
              9090:0,
              9160:0,
              9170:0,
              9180:1,
              9190:1,
              9290:0,
              9370:0,
              9380:0,
              9390:0,
              9470:0,
              9480:1,
              9490:1,
              9570:1,
              9590:0,
              9890:0,
              }
#Find the meaning of each category at --> https://cps.ipums.org/cps/codes/ind_2014_codes.shtml

#Create telework variable:
    
data["TELEWORK"]=data["IND"].map(key_telework)
telework= data.groupby(["YEAR","MONTH","TELEWORK"])["EMPLOYMENT"].mean()
emp_telework= pd.DataFrame(telework)
groups=["No_Telework","Telework"]
emp_telework["groups"]=groups*32

fig, ax = plt.subplots()

for group in groups:
    telegroup = emp_telework[emp_telework["groups"]==group]
    ax.plot(dates,telegroup["EMPLOYMENT"],label=f"{group}")
plt.xticks(rotation=45)
ax.set_ylabel("Employment Rate")
plt.title("Employment Rate by Industry Class")
plt.legend()
plt.show()

#Notice that the classification of telework industry is pure subjective, still it seems there is a difference

##############################################################################
#########################REDO BY AVERAGE WEEKLY HOURS#########################
#Compute Average Weekly Hours:
week_hours = data[data["AHRSWORKT"]<999].groupby(["YEAR","MONTH"])["AHRSWORKT"].mean()
week = pd.DataFrame(week_hours)
worked_hours = week["AHRSWORKT"]
week["MONTH"]=[1,2,3,4,5,6,7,8,9,10,11,12,1,2,3,4,5,6,7,8,9,10,11,12,1,2,3,4,5,6,7,8]
fig, ax = plt.subplots()

ax.plot(dates,worked_hours,label="Average Weekly Worked Hours")
plt.xticks(rotation=45)
plt.legend()
plt.show()

#Detrend and desonalize 2020 prediction:
month = pd.get_dummies(week['MONTH'])
model = LinearRegression()
model.fit(month[:-8], week["AHRSWORKT"][:-8])
pred_2020 = model.predict(month[-8:]) #Generate a prediction for the first 8 months of 2020

#Now I will merge the predictions with the real series: 2018+2019 (Real) + 2020 (Predicted) to have the same observation lenght_

pred_week_hours= pd.concat([week["AHRSWORKT"][:-8],pd.Series(pred_2020)]) #Merge the two
real_week_hours = week["AHRSWORKT"] #Real data

#Plot Real/Predicted data on a date x axis. 

fig, ax = plt.subplots()

ax.plot(dates,pred_week_hours,label="Predicted")
ax.plot(dates,real_week_hours,label="Real")
plt.ylabel("Average Weekly Worked Hours")
plt.legend()
plt.xticks(rotation=45)
plt.title("Agerage Weekle Worked Hours (REAL Vs PREDICTED)")
plt.show()
##############################################################################
#Redo for education group:
    
emp_education= data[data["AHRSWORKT"]<999].groupby(["YEAR","MONTH","EDU_GROUP"])["AHRSWORKT"].mean() #group averaging employment
education = pd.DataFrame(emp_education)
indexs=["No_HighSchool", "HighSchool", "Less_BachelorDegree", "BachelorDegree", "More_BachelorDegree"]
education["indexs"]=indexs*32

fig, ax = plt.subplots()
for index in indexs:
    edu_level = education[education["indexs"] == index]
    ax.plot(dates, edu_level["AHRSWORKT"], label=f"{index}")
plt.xticks(rotation=45)
ax.set_ylabel("Average Weekly Hours Worked")
plt.title("Average Weekly Hours Worked by Education Level")
plt.legend()
plt.show()
##############################################################################
#Redo for occupation group

ocup = data[data["AHRSWORKT"]<999].groupby(["YEAR","MONTH","OCCU_CLASS"])["AHRSWORKT"].mean()
ocup_emp = pd.DataFrame(ocup)

#Generate a reference to call for each class:
ocup_emp["refs"]=refs*32

#Plot the Figure:
fig, ax = plt.subplots()
for ref in refs:
    ocu_group = ocup_emp[ocup_emp["refs"] == ref]
    ax.plot(dates, ocu_group["AHRSWORKT"], label=f"{ref}")
plt.xticks(rotation=45)
ax.set_ylabel("Average Weekly Worked Hours")
plt.title("Average Weekle Hours by Occupation Class")
plt.legend()
plt.show()

#Delete Family Workers: 
refs= ["Self_Employed","Private_Employed","Government_Employed"]

fig, ax = plt.subplots()
for ref in refs:
    ocu_group = ocup_emp[ocup_emp["refs"] == ref]
    ax.plot(dates, ocu_group["AHRSWORKT"], label=f"{ref}")
plt.xticks(rotation=45)
ax.set_ylabel("Average Weekly Worked Hours")
plt.title("Average Weekle Hours by Occupation Class")
plt.legend()
plt.show()

##############################################################################
# Redo for Industry class:
telework= data[data["AHRSWORKT"]<999].groupby(["YEAR","MONTH","TELEWORK"])["AHRSWORKT"].mean()
emp_telework= pd.DataFrame(telework)
emp_telework["groups"]=groups*32

fig, ax = plt.subplots()

for group in groups:
    telegroup = emp_telework[emp_telework["groups"]==group]
    ax.plot(dates,telegroup["AHRSWORKT"],label=f"{group}")
plt.xticks(rotation=45)
ax.set_ylabel("Average Weekly Worked Hours")
plt.title("Average Weekly Worked Hours by Industry Class")
plt.legend()
plt.show() 

##############################################################################
############# REDO FOR WAGE (INCOME) #########################################
#Compute average weekly earnings:
    
earnings = data[data["EARNWEEK"]<9999].groupby(["YEAR","MONTH"])["EARNWEEK"].mean()
e_week = pd.DataFrame(earnings)
week_earnings = e_week["EARNWEEK"]

fig, ax = plt.subplots()

ax.plot(dates,week_earnings,label="Average Weekly Earnings")
plt.xticks(rotation=45)
plt.ylabel("Average Earnings")
plt.legend()
plt.title("Average Weekle Earnings")
plt.show()

#Detrend and desonalize 2020 prediction:
model = LinearRegression()
model.fit(month[:-8], e_week["EARNWEEK"][:-8])
e_pred_2020 = model.predict(month[-8:]) #Generate a prediction for the first 8 months of 2020

#Now I will merge the predictions with the real series: 2018+2019 (Real) + 2020 (Predicted) to have the same observation lenght_

pred_week_earnings= pd.concat([e_week["EARNWEEK"][:-8],pd.Series(e_pred_2020)]) #Merge the two
real_week_earnings = e_week["EARNWEEK"] #Real data

#Plot Real/Predicted data on a date x axis. 

fig, ax = plt.subplots()

ax.plot(dates,pred_week_earnings,label="Predicted")
ax.plot(dates,real_week_earnings,label="Real")
plt.ylabel("Average Weekly Earnings")
plt.legend()
plt.xticks(rotation=45)
plt.title("Average Weekly Earnings (REAL Vs PREDICTED)")
plt.show()
##############################################################################
#Compute by education level:
emp_education= data[data["EARNWEEK"]<9999].groupby(["YEAR","MONTH","EDU_GROUP"])["EARNWEEK"].mean() #group averaging employment
education = pd.DataFrame(emp_education)
indexs=["No_HighSchool", "HighSchool", "Less_BachelorDegree", "BachelorDegree", "More_BachelorDegree"]
education["indexs"]=indexs*32

fig, ax = plt.subplots()
for index in indexs:
    edu_level = education[education["indexs"] == index]
    ax.plot(dates, edu_level["EARNWEEK"], label=f"{index}")
plt.xticks(rotation=45)
ax.set_ylabel("Average Weekly Earnings")
plt.title("Average Weekly Earnings by Education Level")
plt.legend()
plt.show()


##############################################################################
#Compute by Occupation group:
ocup = data[data["EARNWEEK"]<9999].groupby(["YEAR","MONTH","OCCU_CLASS"])["EARNWEEK"].mean()
ocup_emp = pd.DataFrame(ocup)

#Generate a reference to call for each class:
refs=["Private_Employed","Government_Employed"]
ocup_emp["refs"]=["Private_Employed","Government_Employed"]*26+["Self_Employed"]+["Private_Employed","Government_Employed"]*6

#Plot the Figure:
fig, ax = plt.subplots()
for ref in refs:
    ocu_group = ocup_emp[ocup_emp["refs"] == ref]
    ax.plot(dates, ocu_group["EARNWEEK"], label=f"{ref}")
plt.xticks(rotation=45)
ax.set_ylabel("Average Weekly Earnings")
plt.title("Average Weekly Earnings by Occupation Class")
plt.legend()
plt.show()

##############################################################################
#Compute by Industry group:

telework= data[data["EARNWEEK"]<9999].groupby(["YEAR","MONTH","TELEWORK"])["EARNWEEK"].mean()
emp_telework= pd.DataFrame(telework)
emp_telework["groups"]=groups*32

fig, ax = plt.subplots()

for group in groups:
    telegroup = emp_telework[emp_telework["groups"]==group]
    ax.plot(dates,telegroup["EARNWEEK"],label=f"{group}")
plt.xticks(rotation=45)
ax.set_ylabel("Average Weekly Earnings")
plt.title("Average Weekly Earnings by Industry Class")
plt.legend()
plt.show() 

##############################################################################
################ I WILL NOW ANALYZE CERTAIN INDUSTRIES ########################
##############################################################################
#Different Industry:
    #Legend to know industries: 
        #0-->Others
        #1-->Food
        #2--> Health (Pharmaceutical,medical equipment,health care, nursing,hospitals)
        #3--> Manufacturing
        
key_industry={170:1,
              180:1,
              190:0,
              270:3,
              280:1,
              290:1,
              370:0,
              390:0,
              470:0,
              490:0,
              770:0,
              1070:1,
              1080:1,
              1090:1,
              1170:1,
              1180:1,
              1190:1,
              1270:1,
              1280:1,
              1290:1,
              1370:0,
              1470:0,
              1480:0,
              1490:0,
              1570:0,
              1590:0,
              1670:0,
              1680:0,
              1690:0,
              1770:0,
              1790:0,
              3770:0,
              3780:0,
              3790:0,
              3875:0,
              1870:0,
              1880:0,
              1890:0,
              1990:0,
              2070:0,
              2090:0,
              2170:3,
              2180:3,
              2190:2,
              2270:3,
              2280:3,
              2290:3,
              2370:3,
              2380:3,
              2390:3,
              2470:3,
              2480:3,
              2490:3,
              2590:3,
              2670:3,
              2680:3,
              2690:0,
              2770:0,
              2780:0,
              2790:3,
              2870:3,
              2880:3,
              2890:3,
              2970:3,
              2980:3,
              2990:3,
              3070:3,
              3080:3,
              3095:3,
              3170:3,
              3180:3,
              3190:3,
              3365:3,
              3370:3,
              3380:3,
              3390:3,
              3470:3,
              3490:3,
              3570:3,
              3580:3,
              3590:3,
              3670:3,
              3680:3,
              3690:3,
              3895:3,
              3960:3,
              3970:3,
              3980:3,
              3990:3,
              4070:0,
              4080:0,
              4090:0,
              4170:0,
              4180:0,
              4195:0,
              4265:0,
              4270:0,
              4280:0,
              4290:0,
              4370:0,
              4380:0,
              4390:0,
              4470:0,
              4480:0,
              4490:0,
              4560:0,
              4570:0,
              4580:0,
              4585:0,
              4590:0,
              4670:0,
              4680:0,
              4690:0,
              4770:0,
              4780:0,
              4795:0,
              4870:0,
              4880:0,
              4890:0,
              4970:0,
              4980:0,
              4990:0,
              5070:0,
              5080:0,
              5090:0,
              5190:0,
              5275:0,
              5280:0,
              5295:0,
              5370:0,
              5380:0,
              5390:0,
              5470:0,
              5480:0,
              5490:0,
              5570:0,
              5580:0,
              5590:0,
              5591:0,
              5592:0,
              5670:0,
              5680:0,
              5690:0,
              5790:0,
              6070:0,
              6080:0,
              6090:0,
              6170:0,
              6180:0,
              6190:0,
              6270:0,
              6280:0,
              6290:0,
              6370:0,
              6380:0,
              6390:0,
              570:0,
              580:0,
              590:0,
              670:0,
              680:0,
              690:0,
              6470:0,
              6480:0,
              6490:0,
              6570:0,
              6590:0,
              6670:0,
              6672:0,
              6680:0,
              6690:0,
              6695:0,
              6770:0,
              6780:0,
              6870:0,
              6880:0,
              6890:0,
              6970:0,
              6990:0,
              7070:0,
              7080:0,
              7170:0,
              7180:0,
              7190:0,
              7270:0,
              7280:0,
              7290:0,
              7370:0,
              7380:0,
              7390:0,
              7460:0,
              7470:0,
              7480:0,
              7490:0,
              7570:0,
              7580:0,
              7590:0,
              7670:0,
              7680:0,
              7770:0,
              7780:0,
              7790:0,
              7860:0,
              7870:0,
              7880:0,
              7890:0,
              7970:0,
              7980:0,
              7990:0,
              8070:0,
              8080:0,
              8090:0,
              8170:2,
              8180:2,
              8190:2,
              8270:2,
              8290:2,
              8370:0,
              8380:0,
              8390:0,
              8470:0,
              8560:0,
              8570:0,
              8580:0,
              8590:0,
              8660:0,
              8670:0,
              8680:0,
              8690:0,
              8770:0,
              8780:0,
              8790:0,
              8870:0,
              8880:0,
              8970:0,
              8990:0,
              9070:0,
              9080:0,
              9090:0,
              9160:0,
              9170:0,
              9180:0,
              9190:0,
              9290:0,
              9370:0,
              9380:0,
              9390:0,
              9470:0,
              9480:0,
              9490:0,
              9570:0,
              9590:0,
              9890:0,
              }
#Create food industry variable:
    
data["INDUS"]=data["IND"].map(key_industry)
inds= data.groupby(["YEAR","MONTH","INDUS"])["EMPLOYMENT"].mean()
emp_inds= pd.DataFrame(inds)
groups=["Others","Food","Health","Manufacturing"]
emp_inds["groups"]=groups*32

fig, ax = plt.subplots()
for group in groups:
   indsgroup = emp_inds[emp_inds["groups"]==group]
   ax.plot(dates,indsgroup["EMPLOYMENT"],label=f"{group}")
plt.xticks(rotation=45)
ax.set_ylabel("Employment Rate")
plt.title("Employment Rate at Key Idustries")
plt.legend()
plt.show()

##############################################################################
# For the sake of investigation I will also check differences by race:
race_key = {100:1,
            200:2,
            651:3}
data["RACE_GROUP"]= data["RACE"].map(race_key)
race_group = data.groupby(["YEAR","MONTH","RACE_GROUP"])["EMPLOYMENT"].mean()
race = pd.DataFrame(race_group)
indexs = ["White","Black","Asian"]
race["indexs"]=indexs*32

fig, ax = plt.subplots()
for index in indexs:
    racegroup = race[race["indexs"]==index]
    ax.plot(dates,racegroup["EMPLOYMENT"],label=f"{index}")
plt.xticks(rotation=45)
ax.set_ylabel("Employment Rate")
plt.title("Employment Rate by Race")
plt.legend()
plt.show()
##############################################################################
#####QUESTION 3: Is behavior of aggregate hours driven by employment or by av week hours?
#First we need to compute total hours worked.
    # We already average weekly hours (worked_hours), so we need total hours: 
    # We need to compute the total number of people working:
worked_workers = data.groupby(["YEAR","MONTH"])["EMPLOYMENT"].sum()
workers = pd.DataFrame(worked_workers)
hours= workers["EMPLOYMENT"]*worked_hours
total_hours=  pd.DataFrame(hours) #Total Hours Worked 

#Plot:
fig, ax = plt.subplots()
ax.plot(dates,total_hours,label="Total Hours Worked")
plt.xticks(rotation=45)
plt.legend()
plt.title("Total Hours Worked")
plt.ylabel("Hours Worked")
plt.show()

#Compute now percentage change on employment: 
emp = pd.DataFrame(employment)
emplo = emp["EMPLOYMENT"]
emp_percentage = [100 * e1 / e2 - 100 for e1, e2 in zip(emplo[1:], emplo)] #Employment percentage change

#And do the same for average weekly hours: 
worked_percentage = [100 * e1 / e2 - 100 for e1, e2 in zip(worked_hours[1:], worked_hours)]


#Redo Dates:
dates= pd.date_range(start='2018/02/01', periods=31, freq='M')
fig, ax = plt.subplots()
ax.plot(dates,emp_percentage,label="Employment Change")
ax.plot(dates,worked_percentage,label="Hours Worked Change")
plt.ylabel("Percentage Change")
plt.legend()
plt.title("Percentage Change of Employment and Hours Worked")
plt.xticks(rotation=45)
plt.show()

##############################################################################
##############################################################################
############################ REDO FOR SPAIN ##################################
##############################################################################
spain1= pd.read_csv(r'C:\Users\Sergi\Desktop\Universitat\Master\Second Year\Quantitative Macroeconomics\Problem Sets\PS1\spain1.txt')
spain2= pd.read_csv(r'C:\Users\Sergi\Desktop\Universitat\Master\Second Year\Quantitative Macroeconomics\Problem Sets\PS1\spain2.txt')

#Generate Employment without 2020:
spain1_no2020 = spain1[:-2]
spain1_no2020["grp"] = [1,2,3,4,1,2,3,4]
emp_no2020 = spain1_no2020["Value"]
spain1_mean  = spain1_no2020.groupby("grp")["Value"].mean()
predicted2020  = spain1_mean[:-2]
employment_predicted = pd.concat([emp_no2020, predicted2020]) #Real employment + Predicted
employment_real = spain1["Value"] 

dates= pd.date_range(start='2018/01/01', periods=10, freq='QS')
fig, ax = plt.subplots()
ax.plot(dates,employment_predicted, label="Predicted")
ax.plot(dates,employment_real, label="Real")
plt.legend()
plt.xticks(rotation=45)
plt.ylabel("Employment Rate %")
plt.title("Employment Rate Spain (REAL Vs PREDICTED")
plt.show()


#Employment Rate by Education level: 
levels = ["Primary","Secondary","Tertiary"]
spain2["levels"]=levels*10
fig, ax = plt.subplots()
for level in levels:
    educ_level = spain2[spain2["levels"]==level]
    ax.plot(dates,educ_level["Value"],label=f"{level}")
plt.legend()
plt.ylabel("Employment Rate %")
plt.xticks(rotation=45)
plt.title("Employment Rate by Education Group (Spain)")

#Average Hours Worked: 
spain3= pd.read_excel(r'C:\Users\Sergi\Desktop\Universitat\Master\Second Year\Quantitative Macroeconomics\Problem Sets\PS1\spain3.xlsx')
#Compute prediction: 
av_no2020 = spain3[:-2]
av_horas_no2020=av_no2020["AV_HORAS"]
av_no2020["INDEX"]=[1,2,3,4,1,2,3,4]
#av_mean =av_no2020.groupby("TRIM")["AV_HORAS"].mean() --> Why is it not working?
av_mean =av_no2020.groupby(["INDEX"])["AV_HORAS"].mean()
av_predicted = av_mean[:-2]

#Generate the two (REAL,PREDICTED):

avpredicted = pd.concat([av_horas_no2020,av_predicted])
avreal = spain3["AV_HORAS"]

fig, ax = plt.subplots()
ax.plot(dates,avpredicted,label="Predicted")
ax.plot(dates,avreal,label="Real")
plt.ylabel("Average Hours Worked")
plt.title("Average Weekly Hours Worked (REAL Vs PREDICTED)")
plt.legend()
plt.xticks(rotation=45)
plt.show()