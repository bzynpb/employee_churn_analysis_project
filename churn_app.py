import pickle
import pandas as pd
import numpy as np
import streamlit as st
import base64
# from PIL import Image


st.set_page_config(page_title='Employee Churn Analysis Project', page_icon="👩‍💻", layout="wide")

html_temp = """
<div style="background-color:#3A5874;padding:10px">
<h1 style="color:white;text-align:center;">Are you worried that your employees will leave your company?</h1>
</div><br>"""
st.markdown(html_temp,unsafe_allow_html=True)
st.write('\n')

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)


set_background('background.png')

st.image("work.png")

html_temp2 = """
<div style="background-color:#5A7D9F;padding:10px">
<h3 style="color:white;text-align:center;">Complete the levels below and  ease your worries with Employee Churn Analysis</h3>
</div><br>"""
st.markdown(html_temp2,unsafe_allow_html=True)


col1, col2 = st.columns((7,1)) # ekrani 2 kolona ayirdik


with col1:
    satisfaction_level=st.slider("Employee satisfaction point", 0.01, 1.00, 0.50, step=0.01)
    last_evaluation=st.slider("Evaluated performance by the employer", 0.01, 1.00, 0.50, step=0.01)
    number_project=st.slider("How many of projects assigned to an employee?", 2 ,7, 5, step=1)
    average_montly_hours=st.slider("How many hours in averega an employee worked in a month?", 96, 310, 200, step=1)

	
ColorMinMax = st.markdown(''' <style> div.stSlider > div[data-baseweb = "slider"] > div[data-testid="stTickBar"] > div {
	    background: rgb(1 1 1 / 0%); } </style>''', unsafe_allow_html = True)


Slider_Cursor = st.markdown(''' <style> div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"]{
	    background-color: rgb(0, 51, 102); box-shadow: rgb(14 38 74 / 20%) 0px 0px 0px 0.3rem;} </style>''', unsafe_allow_html = True)


Slider_Number = st.markdown(''' <style> div.stSlider > div[data-baseweb="slider"] > div > div > div > div
					{ color: rgb(14, 38, 74); } </style>''', unsafe_allow_html = True)


col = f''' <style> div.stSlider > div[data-baseweb = "slider"] > div > div {{
	    background: linear-gradient(to right, rgb(1, 183, 158) 0%, 
					rgb(14, 38, 74) {satisfaction_level}%, 
					rgba(14, 38, 74, 0.25) {satisfaction_level}%, 
					rgba(14, 38, 74, 0.25) 100%); }} </style>'''


ColorSlider = st.markdown(col, unsafe_allow_html = True)   



def satisfaction(satisfaction_level): 
    if satisfaction_level <= 0.01:
        output = "  🤬"
        
    elif satisfaction_level <= 0.2:
        output = "  😒"
    
    elif satisfaction_level <= 0.4:
        output = "  😔"
    
    elif satisfaction_level <= 0.6:
        output = "  🙂"
        
    elif satisfaction_level <= 0.8:
        output = "  😄"
        
    elif satisfaction_level < 1:
        output = "  🤗"
        
    else:
        output ="  🥰"
        
    return output 
    
with col2: 
    st.title(satisfaction(satisfaction_level))

    
time_spend_company=st.selectbox("The number of years spent by an employee in the company", (2, 3, 4, 5, 6, 7, 8, 9, 10))    

df = pd.read_csv("HR_Dataset.csv")
features = pickle.load(open("features2.pkl", "rb"))
model = pickle.load(open("XGBClassifier.pkl", "rb"))

coll_dict = {'satisfaction_level':satisfaction_level,
             'last_evaluation':last_evaluation,
             'number_project':number_project,
             'average_montly_hours': average_montly_hours,
	     'time_spend_company':time_spend_company
            }

columns = ['satisfaction_level',
           'last_evaluation', 
           'number_project',
           'average_montly_hours', 
           'time_spend_company'
          ]

df_coll = pd.DataFrame.from_dict([coll_dict])
user_inputs = pd.get_dummies(df_coll).reindex(columns=features.columns, fill_value=0)
prediction = model.predict(user_inputs)

st.write("")
st.write("")
st.write("")
html_temp = """
<div style="background-color:#6F8EA6;padding:10px">
<h2 style="color:white;text-align:center;">Will Your Employee Run Away?</h2>
</div><br>"""
st.markdown(html_temp,unsafe_allow_html=True)


button_style = """ 
<style> div.stButton > button:first-child { 
display: block;
width: 100%;
border: none;
background-color: #3A5874;
color: white;
padding: 14px 28px;
font-size: 24px;
cursor: pointer;
text-align: center; 
}

.button span {
  cursor: pointer;
  display: inline-block;
  position: relative;
  transition: 0.5s;
}

.button span:after {
  content: '\00bb';
  position: absolute;
  opacity: 0;
  top: 0;
  right: -20px;
  transition: 0.5s;
}

.button:hover span {
  padding-right: 25px;
}

.button:hover span:after {
  opacity: 1;
  right: 0;
  }
</style>
"""
st.markdown(button_style, unsafe_allow_html=True) 



c1, c2, c3,c4,c5= st.columns((1,3,4,3,1)) 
with c3:
    if c3.button("Predict Now!"):
        if prediction[0] ==1:
            st.error("Employee will LEAVE 👎")
        else:
            st.success("Employee will STAY 👍 ")    
	


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
