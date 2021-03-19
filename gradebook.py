#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
url="https://raw.githubusercontent.com/realpython/materials/master/pandas-gradebook-project/data/roster.csv"
res=requests.get(url,allow_redirects=True)
with open('roster.csv','wb') as file:
    file.write(res.content)
roster=pd.read_csv('roster.csv',converters={"NetID": str.lower, "Email Address": str.lower})


# In[2]:


roster.head()


# In[3]:


roster.tail()


# In[4]:


url="https://raw.githubusercontent.com/realpython/materials/master/pandas-gradebook-project/data/hw_exam_grades.csv"
res=requests.get(url,allow_redirects=True)
with open('hm_exams_grades.csv','wb') as file:
    file.write(res.content)
hm_exams_grades=pd.read_csv('hm_exams_grades.csv')


# In[5]:


hm_exams_grades.head()


# In[6]:


url1="https://raw.githubusercontent.com/realpython/materials/master/pandas-gradebook-project/data/quiz_1_grades.csv"
url2="https://raw.githubusercontent.com/realpython/materials/master/pandas-gradebook-project/data/quiz_2_grades.csv"
url3="https://raw.githubusercontent.com/realpython/materials/master/pandas-gradebook-project/data/quiz_3_grades.csv"
url4="https://raw.githubusercontent.com/realpython/materials/master/pandas-gradebook-project/data/quiz_4_grades.csv"
url5="https://raw.githubusercontent.com/realpython/materials/master/pandas-gradebook-project/data/quiz_5_grades.csv"
res1=requests.get(url1,allow_redirects=True)
with open('quiz_1.csv','wb') as file:
    file.write(res1.content)
quiz_1=pd.read_csv('quiz_1.csv')

res2=requests.get(url2,allow_redirects=True)
with open('quiz_2.csv','wb') as file:
    file.write(res2.content)
quiz_2=pd.read_csv('quiz_2.csv')

res3=requests.get(url3,allow_redirects=True)
with open('quiz_3.csv','wb') as file:
    file.write(res3.content)
quiz_3=pd.read_csv('quiz_3.csv')

res4=requests.get(url4,allow_redirects=True)
with open('quiz_4.csv','wb') as file:
    file.write(res4.content)
quiz_4=pd.read_csv('quiz_4.csv')

res5=requests.get(url5,allow_redirects=True)
with open('quiz_5.csv','wb') as file:
    file.write(res5.content)
quiz_5=pd.read_csv('quiz_5.csv')


# In[7]:


quiz_1.rename(columns={"Grade":"Quiz 1"},inplace=True)
quiz_1.drop(labels=['Last Name','First Name'],axis=1,inplace=True)
quiz_1


# In[8]:


quiz_2.rename(columns={"Grade":"Quiz 2"},inplace=True)
quiz_2.drop(labels=['Last Name','First Name'],axis=1,inplace=True)
# quiz_2.set_index('Email',inplace=True)
quiz_2


# In[9]:


quiz_3.rename(columns={"Grade":"Quiz 3"},inplace=True)
quiz_3.drop(labels=['Last Name','First Name'],axis=1,inplace=True)
# quiz_3.set_index('Email',inplace=True)
quiz_3.head()


# In[10]:


quiz_4.rename(columns={"Grade":"Quiz 4"},inplace=True)
quiz_4.drop(labels=['Last Name','First Name'],axis=1,inplace=True)
# quiz_4.set_index('Email',inplace=True)
quiz_4.head()


# In[11]:


quiz_5.rename(columns={"Grade":"Quiz 5"},inplace=True)
quiz_5.drop(labels=['Last Name','First Name'],axis=1,inplace=True)
# quiz_5.set_index('Email',inplace=True)
quiz_5.head()


# In[12]:


roster


# In[13]:


roster.drop(axis=1,labels=['ID','Name'],inplace=True)


# In[14]:


roster


# In[15]:


roster.set_index('NetID',inplace=True)


# In[16]:


roster.head()


# In[17]:


hm_exams_grades.head()


# In[18]:


hm_exams_grades.drop(axis=1,labels=['First Name','Last Name'],inplace=True)


# In[19]:


hm_exams_grades.set_index('SID',inplace=True)
hm_exams_grades.head()


# In[20]:


quiz_grades1=pd.merge(quiz_1,quiz_2,on='Email')
quiz_grades2=pd.merge(quiz_grades1,quiz_3,on='Email')
quiz_grades3=pd.merge(quiz_grades2,quiz_4,on='Email')
quiz_grades_final=pd.merge(quiz_grades3,quiz_5,on='Email')
quiz_grades_final


# In[21]:


quiz_grades_final.set_index('Email',inplace=True)
quiz_grades_final.head()


# In[22]:


roster.head(1)


# In[23]:


hm_exams_grades.head(1)


# In[24]:


final_data=pd.merge(roster,hm_exams_grades,left_index=True,right_index=True)
final_data.head()


# In[25]:


final_data=pd.merge(final_data,quiz_grades_final,left_on="Email Address", right_index=True)
final_data.head()

# now data is ready to analyse
# # fill in nan values

# In[26]:


final_data=final_data.fillna(0)
final_data.head()


# # calculating the total score

# In[27]:


n_exams = 3
for n in range(1, n_exams + 1):
    final_data[f"Exam {n} Score"] = (
        final_data[f"Exam {n}"] / final_data[f"Exam {n} - Max Points"]
    )


# # Calculating the homework score

# In[28]:


homework_scores = final_data.filter(regex=r"^Homework \d\d?$", axis=1)
homework_max_points = final_data.filter(regex=r"^Homework \d\d? - Max Points$", axis=1)


# In[29]:


sum_of_hw_scores = homework_scores.sum(axis=1)
sum_of_hw_max = homework_max_points.sum(axis=1)
final_data["Total Homework"] = sum_of_hw_scores /sum_of_hw_max


# In[30]:


hw_scores=final_data.filter(regex=r"^Hw \d$",axis=1)


# In[31]:


homework_max_points.head()


# In[32]:


homework_scores.head()


# In[33]:


homework_scores.columns


# In[34]:


hw_max_renamed = homework_max_points.set_axis(homework_scores.columns, axis=1)


# In[35]:


hw_max_renamed.head()


# In[36]:


average_hw_scores = (homework_scores / hw_max_renamed).sum(axis=1)
average_hw_scores.head()


# In[37]:


homework_scores.shape[1]


# In[38]:


final_data["Average Homework"] = average_hw_scores / homework_scores.shape[1]


# In[39]:


final_data["Homework Score"] = final_data[
    ["Total Homework", "Average Homework"]
].max(axis=1)


# In[40]:


final_data.head()


# # Calculating the quiz csore

# In[41]:


quiz_scores=final_data.filter(regex=r"^Quiz \d$",axis=1)
quiz_max_points = pd.Series(
    {"Quiz 1": 11, "Quiz 2": 15, "Quiz 3": 17, "Quiz 4": 14, "Quiz 5": 12}
)
sum_quiz_score=quiz_scores.sum(axis=1)
sum_quiz_max_points=quiz_max_points.sum()
final_data["Total quizzes"]=sum_quiz_score/sum_quiz_max_points
avg_quiz_scores = (quiz_scores/quiz_max_points).sum(axis=1)
final_data["Avg quizzes"]=avg_quiz_scores/quiz_scores.shape[1]
final_data["Quiz Score"]=final_data[["Total quizzes","Avg quizzes"]].max(axis=1)
final_data.head()


# In[42]:


weightings = pd.Series(
    {
        "Exam 1 Score": 0.05,
        "Exam 2 Score": 0.1,
        "Exam 3 Score": 0.15,
        "Quiz Score": 0.30,
        "Homework Score": 0.4,
    }
)


# In[43]:


import numpy as np
final_data["Final Score"] = (final_data[weightings.index] * weightings).sum(
    axis=1
)
final_data["Ceiling Score"] = np.ceil(final_data["Final Score"] * 100)


# In[44]:


grades = {
    90: "A",
    80: "B",
    70: "C",
    60: "D",
    0: "F",
}
def grade_mapping(value):
    for key,letter in grades.items():
        if value>=key:
            return letter


# In[45]:


letter_grades = final_data["Ceiling Score"].map(grade_mapping)
final_data["Final Grade"] = pd.Categorical(
    letter_grades, categories=grades.values(), ordered=True
)


# In[55]:


final_data.head()


# # plotting summary statistics

# In[69]:


import matplotlib.pyplot as plt
import scipy.stats


# In[70]:


grade_counts = final_data["Final Grade"].value_counts().sort_index()
grade_counts.plot.bar()
plt.xlabel("Grades")
plt.ylabel("No of students")
plt.show()


# In[77]:


final_data["Final Score"].plot.hist(bins=20, label="Histogram")
final_data["Final Score"].plot.density(
    linewidth=4, label="Kernel Density Estimate"
)

final_mean = final_data["Final Score"].mean()
final_std = final_data["Final Score"].std()
x = np.linspace(final_mean - 5 * final_std, final_mean + 5 * final_std, 200)
normal_dist = scipy.stats.norm.pdf(x, loc=final_mean, scale=final_std)
plt.plot(x, normal_dist, label="Normal Distribution", linewidth=4)
plt.legend()
plt.show()


# In[ ]:




