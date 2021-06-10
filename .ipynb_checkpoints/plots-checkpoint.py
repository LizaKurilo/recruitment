import streamlit as st
import pandas as pd
import os
import pathlib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import plotly.graph_objects as go
from plotly import tools
import plotly.offline as py
import plotly.express as px


def make_plots_by_closed_position_list(df, date_1, date_2, download=False, path_to_download=''):
        
    
    def make_plot_recruitment_vacancies_by_time_period(df, date_1, date_2, download, path_to_download):
        
        recruiter_count  = df['Recruiter responsible'].value_counts() 
        recruiter_count_norm  = df['Recruiter responsible'].value_counts(normalize=True)* 100
        
        sns.set_style("whitegrid")
        bar,ax = plt.subplots(figsize=( 14, int(0.55 * len(recruiter_count))))
        ax = sns.barplot( recruiter_count.values, recruiter_count.index, alpha=0.8, orient="h")
        plt.title(f"Count of Closed vacancies by recruiterd from {date_1} to {date_2}",fontsize=18)
        plt.ylabel('Number of Closed Positions', fontsize=16)
        plt.xlabel('Recruiter', fontsize=16)
        plt.yticks(fontsize=13)
        plt.xticks(fontsize=13)
        
        i = 0
        for rect in ax.patches:
            ax.text ( rect.get_width(), rect.get_y() + rect.get_height() / 2, "%.2f%%"% recruiter_count_norm[i], weight='bold', fontsize=12 )
            i+=1
        
        if download:
            plt.savefig(path_to_download+f"/recruitment_vacancies_{date_1}_{date_2}.png")
        else:
            plt.show()
            st.pyplot(bar)
      #  st.bar_chart(recruiter_count.sort_values(ascending=False))
    
    
    
#         basic_chart = alt.Chart(recruiter_count
#                                 # legend=alt.Legend(title='Animals by year')
#         )
#         st.altair_chart(basic_chart)
        # st.line_chart(df.loc[df.Platform==platform_name]['Global_Sales'])

#         st.write('Geography wise sales')
#         temp = pd.melt(df.loc[df.Platform == platform_name, ['Platform', 'Year', 'NA_Sales', 'EU_Sales', 'JP_Sales', \
#                                                              'Other_Sales']], id_vars=['Platform', 'Year'], var_name='Geo',
#                        value_name='Sales')
#         # sns.barplot(x="Year", y="Sales", hue="Geo", data=temp)
#         temp = temp.groupby(['Platform', 'Year', 'Geo']).agg({'Sales': 'sum'}).reset_index()
#         stacked_bar = alt.Chart(temp).mark_bar().encode(
#             x='Year',
#             y='Sales',
#             color='Geo'
#         )
#         st.altair_chart(stacked_bar)
    
        
    def make_plot_skills_by_time_period(df, date_1, date_2, download, path_to_download):
    
        skills_count = df['Primary skill'].value_counts()
        skills_count_norm = df['Primary skill'].value_counts(normalize=True) * 100
        
        sns.set_style("whitegrid")
        bar,ax = plt.subplots(figsize=(15,int(0.55 * len(skills_count))))
        ax = sns.barplot( skills_count.values, skills_count.index, alpha=0.8, orient="h")
        plt.xlabel("Count of Closed vacancies by skills", labelpad=18)
        plt.ylabel("Skill", labelpad=16)
        plt.title(f"Count of Closed vacancies by skills from {date_1} to {date_2}", y=1.02, fontsize=16)
        plt.yticks(fontsize=13)
        plt.xticks(fontsize=13)
        
        i = 0
        for rect in ax.patches:
            ax.text ( rect.get_width(), rect.get_y() + rect.get_height() / 2, "%.2f%%"% skills_count_norm[i], weight='bold' , fontsize=12)
            i+=1
        if download:
            plt.savefig(path_to_download + f'/skills_{date_1}_{date_2}.png')
        else:
            plt.show()
            st.pyplot(bar)
        
    def make_plot_departments_by_time_period(df, date_1, date_2, download, path_to_download):
        
        sns.set_style("whitegrid")
        df['Department'] = df['Department'].fillna("Not determined")
        df.loc[:, 'Unit'] = df['Department'].map(lambda x: x.split('.')[0])
        department_count  = df['Unit'].value_counts()
        department_count_norm  = df['Unit'].value_counts(normalize=True) * 100
        bar,ax = plt.subplots(figsize=(16,12))
        ax = sns.barplot(department_count.index, department_count.values,  alpha=0.8)
        plt.title(f"Number of interviews by units from {date_1} to {date_2}")
        plt.ylabel('Number of interviews', fontsize=12)
        plt.xlabel('Unit')
        
        i = 0
        for rect in ax.patches:
            ax.text (rect.get_x() + rect.get_width() / 10, rect.get_height(),  f"#{department_count[i]}, {round(department_count_norm[i], 2)}%", weight='bold' )
            i+=1

        if download:
            plt.savefig(path_to_download + f'/departments_{date_1}_{date_2}.png')
        else:
            plt.show()
            st.pyplot(bar)
        
    def make_plot_seniority_by_time_period(df, date_1, date_2, download, path_to_download):
        
        sns.set_style("whitegrid")
        
        seniority_count_norm  = df['Seniority'].value_counts(normalize=True) * 100
        seniority_count = df['Seniority'].value_counts()
        
        bar,ax = plt.subplots(figsize=(12,8))
        ax = sns.barplot(seniority_count_norm.index, seniority_count.values, ci=None, palette="muted",orient='v' )
        ax.set_title("Total Seniority vacancies by date", fontsize=18)
        ax.set_xlabel ("Seniority Type", fontsize=16)
        ax.set_ylabel ("Count", fontsize=16)
        # calculate the percentages and annotate the sns barplot
        i = 0
        for rect in ax.patches:
            ax.text (rect.get_x() + rect.get_width() / 3, rect.get_height(),  f"#{seniority_count[i]}, {round(seniority_count_norm[i], 2)}%", weight='bold' )
            i+=1
      #  bar.savefig("Seaborn_Pie_Chart.png")
        plt.xticks(fontsize=13)
        plt.yticks(fontsize=13)
        if download:
            plt.savefig(path_to_download + f'/seniority_{date_1}_{date_2}.png')
        else:
            st.pyplot(bar)
    
    def make_plot_region_by_time_period(df, date_1, date_2, download, path_to_download):
        
        sns.set_style("whitegrid")
        
        region_count_norm  = df['Region'].value_counts(normalize=True) * 100
        region_count = df['Region'].value_counts()
        
        bar,ax = plt.subplots(figsize=(12,8))
        ax = sns.barplot(region_count.index, region_count.values, ci=None, palette="muted",orient='v', )
        ax.set_title("Total region vacancies by date", fontsize=18)
        ax.set_xlabel ("Region Type", fontsize=16)
        ax.set_ylabel ("Count", fontsize=16)
        plt.xticks(fontsize=13)
        plt.yticks(fontsize=13)
        # calculate the percentages and annotate the sns barplot
        i = 0
        for rect in ax.patches:
            ax.text (rect.get_x() + rect.get_width() / 3, rect.get_height(),  f"#{region_count[i]}, {round(region_count_norm[i], 2)}%", weight='bold' )
            i+=1
        if download:
            bar.savefig(path_to_download + f'/region_{date_1}_{date_2}.png')   
        else:
            st.pyplot(bar)
        
    
    new_df = df[(df['Decision made date'] >= date_1) & 
                                   (df['Decision made date'] < date_2)]
    if download:
        path_to_download = path_to_download + f"/position_list_{date_1}_{date_2}"
        if not os.path.exists(path_to_download):
            os.makedirs(path_to_download)
        
    make_plot_region_by_time_period(new_df, date_1, date_2, download, path_to_download)
    make_plot_recruitment_vacancies_by_time_period(new_df, date_1, date_2, download, path_to_download)
    make_plot_skills_by_time_period(new_df, date_1, date_2, download, path_to_download)
    make_plot_departments_by_time_period(new_df, date_1, date_2, download, path_to_download)
    make_plot_seniority_by_time_period(new_df, date_1, date_2, download, path_to_download)
    
    
def make_plots_by_interview_list(df, date_1, date_2, download=False, path_to_download=''):
    
    def make_plot_recruitment_interviews_by_time_period(df, date_1, date_2, download, path_to_download):
        
        sns.set_style("whitegrid")
        recruiter_count  = df['HRM interviewed'].value_counts() 
        recruiter_count_norm  = df['HRM interviewed'].value_counts(normalize=True)* 100
        
        bar,ax = plt.subplots(figsize=( 14, int(0.5 * len(recruiter_count))))
        ax = sns.barplot( recruiter_count.values, recruiter_count.index, alpha=0.8, orient="h")
        plt.title(f"Count of interwies by recruiterd from {date_1} to {date_2}", fontsize=18)
        plt.ylabel('Number of interwies', fontsize=16)
        plt.yticks(fontsize=14)
        plt.xticks(fontsize=14)
        plt.xlabel('Recruiter', fontsize=15)
        
        i = 0
        for rect in ax.patches:
            ax.text ( rect.get_width(), rect.get_y() + rect.get_height() / 2, "%.2f%%"% recruiter_count_norm[i], weight='bold', fontsize=11 )
            i+=1
        if download:
            bar.savefig(path_to_download + f'/recruitment_interviews_{date_1}_{date_2}.png')   
        else:
            plt.show()
            st.pyplot(bar)
        
        
    def make_plot_departments_by_time_period(df, date_1, date_2, download, path_to_download):
        
        sns.set_style("whitegrid")
        df['Department'] = df['Department'].fillna("Not determined")
        df.loc[:, 'Unit'] = df['Department'].map(lambda x: x.split('.')[0])
        department_count  = df['Unit'].value_counts()
        department_count_norm  = df['Unit'].value_counts(normalize=True) * 100
        bar,ax = plt.subplots(figsize=(16,12))
        ax = sns.barplot(department_count.index, department_count.values,  alpha=0.8)
        plt.title(f"Number of interviews by units from {date_1} to {date_2}", fontsize=18)
        plt.ylabel('Number of interviews', fontsize=15)
        plt.xlabel('Unit', fontsize=15)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        
        i = 0
        for rect in ax.patches:
            ax.text (rect.get_x() + rect.get_width() / 10, rect.get_height(),  f"#{department_count[i]}, {round(department_count_norm[i], 2)}%", weight='bold' )
            i+=1
        if download:
            bar.savefig(path_to_download + f'/departments_{date_1}_{date_2}.png') 
        else:
            plt.show()
            st.pyplot(bar)
        
    
    new_df = df[(df['Date of interview'] >= date_1) & 
                                   (df['Date of interview'] < date_2)]
    new_df = new_df[new_df['Interview result'] != 'cancelled']
    
    if download:
        path_to_download = path_to_download + f"/interview_list_{date_1}_{date_2}"
        if not os.path.exists(path_to_download):
            os.makedirs(path_to_download)
    
    make_plot_recruitment_interviews_by_time_period(new_df, date_1, date_2, download, path_to_download)
    make_plot_departments_by_time_period(new_df, date_1, date_2, download, path_to_download)

    
    
def make_plots_by_jo_hired_list(df, date_1, date_2, download=False, path_to_download=''):
    
    def make_plot_jo_by_skill_by_time_period(df, date_1, date_2, download, path_to_download):
        
        dataframe = pd.DataFrame(df.groupby(['Primary skill', 'JO result']).size(), columns=['Count'])
        flattened = pd.DataFrame(dataframe.to_records())
        flattened['total']= flattened['Primary skill'].map(dict(flattened.groupby(['Primary skill']).sum()['Count']))
        flattened = flattened.sort_values(by=['total', 'JO result'], ascending=(False, True))
        fig = px.bar(flattened, x="Count", y="Primary skill", color="JO result", title="JO by skill", height=1000)
        
        if download:
            fig.write_image(path_to_download + f'/skill_{date_1}_{date_2}.png') 
        else:
            st.plotly_chart(fig)
        
    
    def make_plot_seniority_by_time_period(df, date_1, date_2, download, path_to_download):
        
        sns.set_theme(style="whitegrid")

        # Draw a nested barplot by species and sex
        bar,ax = plt.subplots(figsize=( 12, 8))
        ax = sns.countplot(
            data=df, 
            x="Position in company",  hue="JO result",
            alpha=0.8, orient="h"
        )
        
        if download:
            bar.savefig(path_to_download + f'/seniority_{date_1}_{date_2}.png') 
        else:
            st.pyplot(bar)
        
        
        dataframe = pd.DataFrame(df.groupby(['Position in company', 'JO result']).size(), columns=['Count'])
        flattened = pd.DataFrame(dataframe.to_records())
        flattened['total']= flattened['Position in company'].map(dict(flattened.groupby(['Position in company']).sum()['Count']))
        flattened = flattened.sort_values(by=['total', 'JO result'], ascending=(False, True))
        fig = px.bar(flattened, x="Position in company", y="Count", color="JO result", title="JO by seniority")
        
        
        if download:
            fig.write_image(path_to_download + f'/seniority_2_{date_1}_{date_2}.png') 
        else:
            st.plotly_chart(fig)
        

    new_df = df[(df['JO date'] >= date_1) & 
                                   (df['JO date'] < date_2)]
    if download:
        path_to_download = path_to_download + f"/jo_hired_list_{date_1}_{date_2}"
        if not os.path.exists(path_to_download):
            os.makedirs(path_to_download)
            
    make_plot_jo_by_skill_by_time_period(new_df, date_1, date_2, download, path_to_download)
    make_plot_seniority_by_time_period(new_df, date_1, date_2, download, path_to_download)
    