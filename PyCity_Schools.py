#!/usr/bin/env python
# coding: utf-8

# In[98]:


import pandas as pd
import numpy as np


# In[99]:


schools = pd.read_csv("Resources/schools_complete.csv")


# In[100]:


students = pd.read_csv("Resources/students_complete.csv")


# In[101]:


#renames for merge
schools.rename(columns = {'school_name': 'school'}, inplace = True)
students.rename(columns = {'school_name': 'school'}, inplace = True)

merged_df = students.merge(schools, how = 'left', on = 'school')
merged_df.head()


# In[102]:


#create array of unique school names
all_school_names = schools['school'].unique()
all_school_names


# In[103]:


#gives the length of unique school names to give us how many schools
school_count = len(all_school_names)
school_count


# In[104]:


#district student count
dist_student_count = schools['size'].sum()
dist_student_count


# In[105]:


#student count from student file
total_student_rec = students['student_name'].count()
total_student_rec


# In[106]:


#total budget
total_budget = schools['budget'].sum()
total_budget


# In[107]:


#total and percent passing reading
total_pass_read = students.loc[students['reading_score'] >= 70]['reading_score'].count()
perc_pass_read = total_pass_read/total_student_rec
print('Total Passing Reading:', total_pass_read, 'Percent Passing Reading:', perc_pass_read)


# In[108]:


# total and % passing math
total_pass_math = students.loc[students['math_score'] >= 70]['math_score'].count()
perc_pass_math = total_pass_math/total_student_rec
print(total_pass_math, perc_pass_math)


# In[109]:


#average math score 
avg_math_score = students['math_score'].mean()
#average reading score calculation
avg_reading_score = students['reading_score'].mean()
print(avg_math_score, avg_reading_score)


# In[110]:


#Overall Passing Rate 
overall_pass = students[(students['math_score'] >= 70) & (students['reading_score'] >= 70)]['student_name'].count()/total_student_rec
overall_pass


# In[111]:


# district dataframe from dictionary

district_summary = pd.DataFrame({
    
    "Total Schools": [school_count],
    "Total Students": [dist_student_count],
    "Total Budget": [total_budget],
    "Average Reading Score": [avg_reading_score],
    "Average Math Score": [avg_math_score],
    "% Passing Reading":[perc_pass_read],
    "% Passing Math": [perc_pass_math],
    "Overall Passing Rate": [overall_pass]

})


# In[112]:


#store as different df to change order
dist_sum = district_summary[["Total Schools", 
                             "Total Students", 
                             "Total Budget", 
                             "Average Reading Score", 
                             "Average Math Score", 
                             '% Passing Reading', 
                             '% Passing Math', 
                             'Overall Passing Rate']]


# In[113]:


#format cells
dist_sum.style.format({"Total Budget": "${:,.2f}", 
                       "Average Reading Score": "{:.1f}", 
                       "Average Math Score": "{:.1f}", 
                       "% Passing Math": "{:.1%}", 
                       "% Passing Reading": "{:.1%}", 
                       "Overall Passing Rate": "{:.1%}"})


# In[139]:


#groups by school
by_school = merged_df.set_index('school').groupby(['school'])
by_school.head()


# In[115]:


#school types
sch_types = schools.set_index('school')['type']


# In[116]:


# total students by school
stu_per_sch = by_school['Student ID'].count()


# In[117]:


# school budget
sch_budget = schools.set_index('school')['budget']


# In[118]:


#per student budget
stu_budget = schools.set_index('school')['budget']/schools.set_index('school')['size']
stu_budget


# In[119]:


#avg scores by school
avg_math = by_school['math_score'].mean()
avg_read = by_school['reading_score'].mean()
print(avg_math, avg_read)


# In[120]:


# % passing scores
pass_math = merged_df[merged_df['math_score'] >= 70].groupby('school')['Student ID'].count()/stu_per_sch 
pass_read = merged_df[merged_df['reading_score'] >= 70].groupby('school')['Student ID'].count()/stu_per_sch 


# In[121]:


overall = merged_df[(merged_df['reading_score'] >= 70) & (merged_df['math_score'] >= 70)].groupby('school')['Student ID'].count()/stu_per_sch


# In[122]:


sch_summary = pd.DataFrame({
    "School Type": sch_types,
    "Total Students": stu_per_sch,
    "Per Student Budget": stu_budget,
    "Total School Budget": sch_budget,
    "Average Math Score": avg_math,
    "Average Reading Score": avg_read,
    '% Passing Math': pass_math,
    '% Passing Reading': pass_read,
    "Overall Passing Rate": overall
})
sch_summary.head()


# In[123]:


#munging
sch_summary = sch_summary[['School Type', 
                          'Total Students', 
                          'Total School Budget', 
                          'Per Student Budget', 
                          'Average Math Score', 
                          'Average Reading Score',
                          '% Passing Math',
                          '% Passing Reading',
                          'Overall Passing Rate']]
sch_summary.head()


# In[124]:


#formatting
sch_summary.style.format({'Total Students': '{:,}', 
                          "Total School Budget": "${:,}", 
                          "Per Student Budget": "${:.0f}",
                          'Average Math Score': "{:.1f}", 
                          'Average Reading Score': "{:.1f}", 
                          "% Passing Math": "{:.1%}", 
                          "% Passing Reading": "{:.1%}", 
                          "Overall Passing Rate": "{:.1%}"})


# In[125]:


#Top performing schools by passing rate
# sort values by passing rate and then only print top 5 
top_5 = sch_summary.sort_values("Overall Passing Rate", ascending = False)
top_5.head().style.format({'Total Students': '{:,}',
                           "Total School Budget": "${:,}", 
                           "Per Student Budget": "${:.0f}", 
                           "% Passing Math": "{:.1%}", 
                           "% Passing Reading": "{:.1%}", 
                           "Overall Passing Rate": "{:.1%}"})


# In[126]:


#Bottom five school by passing rate, worse to best
#take tail of top5 sort and re-sort from worst to best
bottom_5 = top_5.tail()
bottom_5 = bottom_5.sort_values('Overall Passing Rate')
bottom_5.style.format({'Total Students': '{:,}', 
                       "Total School Budget": "${:,}", 
                       "Per Student Budget": "${:.0f}", 
                       "% Passing Math": "{:.1%}", 
                       "% Passing Reading": "{:.1%}", 
                       "Overall Passing Rate": "{:.1%}"})


# In[127]:


#creates grade level average math scores for each school 
ninth_math = students.loc[students['grade'] == '9th'].groupby('school')["math_score"].mean()
tenth_math = students.loc[students['grade'] == '10th'].groupby('school')["math_score"].mean()
eleventh_math = students.loc[students['grade'] == '11th'].groupby('school')["math_score"].mean()
twelfth_math = students.loc[students['grade'] == '12th'].groupby('school')["math_score"].mean()

math_scores = pd.DataFrame({
        "9th": ninth_math,
        "10th": tenth_math,
        "11th": eleventh_math,
        "12th": twelfth_math
})
math_scores = math_scores[['9th', '10th', '11th', '12th']]
math_scores.index.name = "School"


# In[128]:


math_scores.style.format({'9th': '{:.1f}', 
                          "10th": '{:.1f}', 
                          "11th": "{:.1f}", 
                          "12th": "{:.1f}"})


# In[129]:


#Reading Scores by grade
#creates grade level average reading scores for each school
ninth_reading = students.loc[students['grade'] == '9th'].groupby('school')["reading_score"].mean()
tenth_reading = students.loc[students['grade'] == '10th'].groupby('school')["reading_score"].mean()
eleventh_reading = students.loc[students['grade'] == '11th'].groupby('school')["reading_score"].mean()
twelfth_reading = students.loc[students['grade'] == '12th'].groupby('school')["reading_score"].mean()

#merges the reading score averages by school and grade together
reading_scores = pd.DataFrame({
        "9th": ninth_reading,
        "10th": tenth_reading,
        "11th": eleventh_reading,
        "12th": twelfth_reading
})
reading_scores = reading_scores[['9th', '10th', '11th', '12th']]
reading_scores.index.name = "School"

#format
reading_scores.style.format({'9th': '{:.1f}', 
                             "10th": '{:.1f}', 
                             "11th": "{:.1f}", 
                             "12th": "{:.1f}"})


# In[130]:


#Scores by school spending
# create spending bins
bins = [0, 584.999, 614.999, 644.999, 999999]
group_name = ['< $585', "$585 - 614", "$615 - 644", "> $644"]
merged_df['spending_bins'] = pd.cut(merged_df['budget']/merged_df['size'], bins, labels = group_name)

#group by spending
by_spending = merged_df.groupby('spending_bins')

#calculations
avg_math = by_spending['math_score'].mean()
avg_read = by_spending['reading_score'].mean()
pass_math = merged_df[merged_df['math_score'] >= 70].groupby('spending_bins')['Student ID'].count()/by_spending['Student ID'].count()
pass_read = merged_df[merged_df['reading_score'] >= 70].groupby('spending_bins')['Student ID'].count()/by_spending['Student ID'].count()
overall = merged_df[(merged_df['reading_score'] >= 70) & (merged_df['math_score'] >= 70)].groupby('spending_bins')['Student ID'].count()/by_spending['Student ID'].count()


# In[131]:


# df build            
scores_by_spend = pd.DataFrame({
    "Average Math Score": avg_math,
    "Average Reading Score": avg_read,
    '% Passing Math': pass_math,
    '% Passing Reading': pass_read,
    "Overall Passing Rate": overall
            
})


# In[132]:


#reorder columns
scores_by_spend = scores_by_spend[[
    "Average Math Score",
    "Average Reading Score",
    '% Passing Math',
    '% Passing Reading',
    "Overall Passing Rate"
]]

scores_by_spend.index.name = "Per Student Budget"
scores_by_spend = scores_by_spend.reindex(group_name)


# In[133]:


#formating
scores_by_spend.style.format({'Average Math Score': '{:.1f}', 
                              'Average Reading Score': '{:.1f}', 
                              '% Passing Math': '{:.1%}', 
                              '% Passing Reading':'{:.1%}', 
                              'Overall Passing Rate': '{:.1%}'})


# In[134]:


#Scores by school size
# create size bins
bins = [0, 999, 1999, 99999999999]
group_name = ["Small (<1000)", "Medium (1000-2000)" , "Large (>2000)"]
merged_df['size_bins'] = pd.cut(merged_df['size'], bins, labels = group_name)

#group by spending
by_size = merged_df.groupby('size_bins')


# In[135]:


#calculations 
avg_math = by_size['math_score'].mean()
avg_read = by_size['math_score'].mean()
pass_math = merged_df[merged_df['math_score'] >= 70].groupby('size_bins')['Student ID'].count()/by_size['Student ID'].count()
pass_read = merged_df[merged_df['reading_score'] >= 70].groupby('size_bins')['Student ID'].count()/by_size['Student ID'].count()
overall = merged_df[(merged_df['reading_score'] >= 70) & (merged_df['math_score'] >= 70)].groupby('size_bins')['Student ID'].count()/by_size['Student ID'].count()


# In[136]:


# df build            
scores_by_size = pd.DataFrame({
    "Average Math Score": avg_math,
    "Average Reading Score": avg_read,
    '% Passing Math': pass_math,
    '% Passing Reading': pass_read,
    "Overall Passing Rate": overall
            
})


# In[137]:


#reorder columns
scores_by_size = scores_by_size[[
    "Average Math Score",
    "Average Reading Score",
    '% Passing Math',
    '% Passing Reading',
    "Overall Passing Rate"
]]

scores_by_size.index.name = "Total Students"
scores_by_size = scores_by_size.reindex(group_name)

#formating
scores_by_size.style.format({'Average Math Score': '{:.1f}', 
                              'Average Reading Score': '{:.1f}', 
                              '% Passing Math': '{:.1%}', 
                              '% Passing Reading':'{:.1%}', 
                              'Overall Passing Rate': '{:.1%}'})

# In[138]:


# group by type of school
by_type = merged_df.groupby("type")

#calculations 
avg_math = by_type['math_score'].mean()
avg_read = by_type['math_score'].mean()
pass_math = merged_df[merged_df['math_score'] >= 70].groupby('type')['Student ID'].count()/by_type['Student ID'].count()
pass_read = merged_df[merged_df['reading_score'] >= 70].groupby('type')['Student ID'].count()/by_type['Student ID'].count()
overall = merged_df[(merged_df['reading_score'] >= 70) & (merged_df['math_score'] >= 70)].groupby('type')['Student ID'].count()/by_type['Student ID'].count()

# df build            
scores_by_type = pd.DataFrame({
    "Average Math Score": avg_math,
    "Average Reading Score": avg_read,
    '% Passing Math': pass_math,
    '% Passing Reading': pass_read,
    "Overall Passing Rate": overall})
    
#reorder columns
scores_by_type = scores_by_type[[
    "Average Math Score",
    "Average Reading Score",
    '% Passing Math',
    '% Passing Reading',
    "Overall Passing Rate"
]]
scores_by_type.index.name = "Type of School"


#formating
scores_by_type.style.format({'Average Math Score': '{:.1f}', 
                              'Average Reading Score': '{:.1f}', 
                              '% Passing Math': '{:.1%}', 
                              '% Passing Reading':'{:.1%}', 
                              'Overall Passing Rate': '{:.1%}'})





