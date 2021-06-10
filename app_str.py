import streamlit as st
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageEnhance
import numpy as np
import cv2
import os
import pathlib
import pandas as pd
import datetime
import altair as alt
import base64
from pathlib import Path

import json
import pickle
import uuid
import re

import plots

# Setting custom Page Title and Icon with changed layout and sidebar state
st.set_page_config(page_title='Dashboard', layout='centered', initial_sidebar_state='expanded')


def local_css(file_name):
    """ Method for reading styles.css and applying necessary changes to HTML"""
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

@st.cache
def load_data():
    xls = pd.DataFrame()
    return xls



def set_date():
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    start_date = st.date_input('Start date', today)
    end_date = st.date_input('End date', tomorrow)
    if start_date < end_date:
        st.success('Start date: `%s`\n\nEnd date: `%s`' % (start_date, end_date))
        return start_date, end_date
    else:
        st.error('Error: End date must fall after start date.') 

        
def download_plots(sheet_to_df_map, start_date, end_date):

    downloads_path = str(Path.home() / "Downloads")
    dirName = downloads_path + f"/report_plots_{start_date}_{end_date}"
    if not os.path.exists(dirName):
        os.makedirs(dirName)
            
    df = sheet_to_df_map['Closed_position']
    plots.make_plots_by_closed_position_list(df, datetime.datetime(*start_date.timetuple()[:-4]), datetime.datetime(*end_date.timetuple()[:-4]), download=True, path_to_download=dirName)
                
    df = sheet_to_df_map['Interview']
    plots.make_plots_by_interview_list(df, datetime.datetime(*start_date.timetuple()[:-4]), datetime.datetime(*end_date.timetuple()[:-4]), download=True, path_to_download=dirName)
              
    df = sheet_to_df_map['JO_Hired']
    plots.make_plots_by_jo_hired_list(df, datetime.datetime(*start_date.timetuple()[:-4]), datetime.datetime(*end_date.timetuple()[:-4]), download=True, path_to_download=dirName)
                
    st.markdown(f'Successfully downloaded to {dirName}')
   
        
        
def make_graphs():
    local_css("css/styles.css")
    st.markdown('<h1 align="center"> Dashboards</h1>', unsafe_allow_html=True)
    activities = ["Closed positions", "Interview", 'JO']
    st.set_option('deprecation.showfileUploaderEncoding', False)
    st.sidebar.markdown("# Graphics on?")
    choice = st.sidebar.selectbox("Choose among the given options:", activities)
    st.markdown("### Upload your data ⬇")
    excel_file = st.file_uploader("", type=['xlsx'])  # upload image
    
    if excel_file is not None:
        xls = pd.ExcelFile(excel_file)
        sheet_to_df_map = {}
        for sheet_name in xls.sheet_names:
            sheet_to_df_map[sheet_name] = xls.parse(sheet_name)
        
        
        try:
            start_date, end_date = set_date()
        except:
            st.markdown('Change dates')

        
        if st.button('Download all plots'):
            try:
                download_plots(sheet_to_df_map, start_date, end_date)
            except:
                st.markdown('File does not contain data in this date interval')
          
                

        if choice == 'Closed positions':
            st.markdown('<h2 align="center">Closed positions analysis</h2>', unsafe_allow_html=True)
                    
            if st.button('Make plots'):
                df = sheet_to_df_map['Closed_position']
                try:
                    plots.make_plots_by_closed_position_list(df, datetime.datetime(*start_date.timetuple()[:-4]), datetime.datetime(*end_date.timetuple()[:-4]))
                except:
                    st.markdown('File does not contain data in this date interval')
            
        

        if choice == 'Interview':
            st.markdown('<h2 align="center">Interview analysis</h2>', unsafe_allow_html=True)
            if st.button('Make plots'): 
                df = sheet_to_df_map['Interview']
                try:
                    plots.make_plots_by_interview_list(df, datetime.datetime(*start_date.timetuple()[:-4]), datetime.datetime(*end_date.timetuple()[:-4]))  
                except:
                     st.markdown('File does not contain data in this date interval')

                        
        if choice == 'JO':
            st.markdown('<h2 align="center">JO analysis</h2>', unsafe_allow_html=True)
            if st.button('Make plots'): 
                df = sheet_to_df_map['JO_Hired']
                try:
                    plots.make_plots_by_jo_hired_list(df, datetime.datetime(*start_date.timetuple()[:-4]), datetime.datetime(*end_date.timetuple()[:-4])) 
                except:
                    st.markdown('File does not contain data in this date interval')
    else:
        st.markdown('Upload data')

    
   
make_graphs()