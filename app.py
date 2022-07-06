import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
#import base64
#import laspy
#import open3d as o3d
from PIL import Image

#this one is for using the whole layout in the page
st.set_page_config(layout='wide')
#page = st.sidebar.selectbox("Explore Or Predict", ("Predict", "Explore"))


####################### FUNCTIONS ####################### 
#To save info in cache. Its not gonna run this function again everytime we open it
@st.cache(persist=False)
def load_data(url):
    df=pd.read_csv(url)
    return df

#@st.cache(persist=True)
#def load_las(url):
#    las = laspy.read(url)
#    return las

@st.cache(persist=True)
def clean_data(df):
    df=df.sample(1000)
    df = df.drop(columns="MDS")
    df = df.drop(columns='Categories')
    return df

logISA=Image.open('images/logC.png')
log117=Image.open('images/logo117.png')


#Creating columns that separates the layout in 3
d1,d2,d3=st.columns((1,8,1))


d1.image(logISA, caption=None, width=300)
#h1 is for a bigger text
#unsafe_allow_html permite usar html
d2.markdown("<h1 style='text-align: center; color: #FE5000;'>LIDAR data analysis for ISA</h1>", unsafe_allow_html=True)

d3.image(log117, caption=None, width=100)

##############Categories#####################
#Creating columns that separates the layout in 2
st.markdown("<h2 style='text-align: center; color: #003087;'> LIDAR Categories in the TOLEDO-SAMORE 230KV transmission line </h2>", unsafe_allow_html=True)
#This file is for the entire line file 2
l2S=load_data('data/open/com2.csv')
#For columns
a1,a2=st.columns((5,5))
#Generating graph
fig1 = px.histogram(l2S, x='Categories', color='Categories')
#Editing graph
fig1.update_layout(
        title_x=0.5,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        template = 'simple_white',
        xaxis_title="<b>Categories<b>",
        yaxis_title='<b>Categories count<b>',
        legend_title_text='')
#Sending graph to streamlit
a1.plotly_chart(fig1)

# Hacer un checkbox
if a1.checkbox('Check here for this count graph explanation.', False):
    a1.write('The following graph allow us to see the most abundant categories along the line.')
    a1.write('For this case, "Árboles mayores a 1 m de de altura" is the category with the highest count, followed by "Terreno natural".')
    a1.write('These categories help us understand what we need to look for when facing our data. For example, we can notice that that the values for risk categories are pretty low compared to the rest.')
    a1.write("This can indicate us that lines with this categories' count could be less in risk that others with a higher risk count.")

ll=l2S.sample(1000)

fig2 = px.scatter_3d(ll, x="X", y="Y", z="Z", color="Categories",size_max=25)

a2.plotly_chart(fig2,use_container_width=True)

# Hacer un checkbox
if a2.checkbox('Check for this 3D graph explanation.', False):
    a2.write('This graph is a representation of the Toledo-Samoré line and is another way to check the categories along it. In this case, each colored point belongs to a different category and we can see the X, Y and Z axes. The Z axis represent the meters above sea level.')
    a2.write('Each of those points end up joining to form the image of the different objects that the LIDAR has detected for this line.')
    a2.write('You can zoom in and out of it to look for the points.')

#LINES
condRisk=load_data('data/open/condRisk.csv')
cRS=condRisk.sample(10000)
st.markdown("<h2 style='text-align: center; color: #0099FF;'> Different risk areas versus 230kV line </h2>", unsafe_allow_html=True)
#Generating graph
fig3=px.scatter(cRS, x='X', y='Z', height=600, width=1500, color="Categories", orientation='h')
fig2.update_layout(
        title_x=0.5,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        template = 'simple_white',
        xaxis_title="<b>X<b>",
        yaxis_title='<b>Z<b>',
        legend_title_text='')
#Sending graph to streamlit
st.plotly_chart(fig3)

# Hacer un checkbox
if st.checkbox('Check here read an explanation about the graph.', False):
    st.write('This line is a 2D representation of the XYZ graph above. In this case, however, we can see the distribution of the points that shape the high tension line along with points that have been determined as risky.')
    st.write('This way, we can know where in the line the different levels of risk are.')
    st.write("In this case, the major risk for this line is in lower values. However, it is important to not disregard the medium and high risk values, even if they are small.")
    st.write("You can interact with the graph by clicking over the different categories in the right or by zooming in.")

st.markdown("<h2 style='text-align: center; color: #FE5000'>Top 10 Smallest distances per risk zone vs the 230kV line</h2>", unsafe_allow_html=True)


#Creating columns that separates the layout in 3
c1,c2,c3=st.columns((5,1,5))
#This ones contains the distances for each category
HD=pd.read_csv("data/analysis/HD.csv")
MD=pd.read_csv("data/analysis/MD.csv")
LD=pd.read_csv("data/analysis/LD.csv")
#data transf
mH=HD.mean()
mM=MD.mean()
mL=LD.mean()

x_data = ['Smaller Distances for High Risk', 'Smaller Distances for Medium Risk',
          'Smaller Distances for Low Risk']

y_data = [mH, mM, mL]

colors = ['rgba(0, 153, 255, 0.5)', 'rgba(100, 48, 135, 0.5)', 'rgba(254, 80, 0, 0.5)']

fig4 = go.Figure()

for xd, yd, cls in zip(x_data, y_data, colors):
        fig4.add_trace(go.Box(
            y=yd,
            name=xd,
            boxpoints='all',
            jitter=0.5,
            whiskerwidth=0.2,
            #fillcolor=cls,
            marker_size=2,
            line_width=1)
        )

fig4.update_layout(
    autosize=False,
    #width=500,
    #height=1000,
    yaxis=dict(
        autorange=True,
        showgrid=True,
        zeroline=True,
        dtick=5,
        gridcolor='rgb(255, 255, 255)',
        gridwidth=1,
        zerolinecolor='rgb(255, 255, 255)',
        zerolinewidth=2,
    ),
     margin=dict(
         l=40,
         r=30,
         b=80,
         t=100,
     ),
    paper_bgcolor='rgb(243, 243, 243)',
    plot_bgcolor='rgb(243, 243, 243)',
    showlegend=False
)

c1.plotly_chart(fig4)

# Hacer un checkbox
if c1.checkbox('Check here for an explanation of the boxplot above.', False):
    c1.write('The following graph describes the distribution of the distances data.')
    c1.write('As we can see, the High Risk Trees category distances are the smallest, as expected, with values mostly distributed between ~9.6 m to ~17 m.')
    c1.write('On the other hand, for the Medium Risk Trees category distances, we can see a main distribution between the values of 13.4 m to 19.3 m.')
    c1.write('Finally, the Low Risk Trees category distances show a distribution of values mainly between 16 m to 20.9 m.')

#data transformation
a=pd.DataFrame(mH.describe(), columns=[''])
b=pd.DataFrame(mM.describe(), columns=[''])
c=pd.DataFrame(mL.describe(), columns=[''])

object=c3.selectbox('Statistics for Top 10 Smallest Distances',('Please Select One','High Risk Trees', 'Medium Risk Trees', 'Low Risk Trees'))

if object=='High Risk Trees':
    c3.write(a)
elif object=='Medium Risk Trees':
    c3.write(b)    
elif object=='Low Risk Trees':
    c3.write(c)

#w1,w2,w3=st.columns((5,1,5))
#Socials ISA

#lISA='https://www.linkedin.com/company/isa-intercolombia/'
#tISA='https://twitter.com/intercolombia'
#yISA='https://www.youtube.com/c/CanalISAINTERCOLOMBIA'
#fbISA='https://es-la.facebook.com/ISAIntercolombiaSA/'

#Socials Team
#lL='https://www.linkedin.com/in/l-giron/'
#lE='https://www.linkedin.com/in/elkinrestrepom/'
#tL='https://twitter.com/boalatil'
#tE='https://twitter.com/ElkinRestrepoM'

#link=Image.open('images/link.png')
#twit=Image.open('images/twit.png')
#you=Image.open('images/you.png')
#fac=Image.open('images/fac.png')

