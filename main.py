import streamlit as st
from shillelagh.backends.apsw.db import connect
import shillelagh
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Enactus HR Dashboard",
    page_icon="📊",
    layout = 'wide'  
)

st.title("Enactus-FUTO HR Dashboard")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)

# ------------ {connection} --------------------------
@st.cache(allow_output_mutation=True)
def get_database_connection():
    return connect(":memory:")

conn = get_database_connection()

@st.cache(ttl=5, hash_funcs={shillelagh.backends.apsw.db.Connection: hash},allow_output_mutation=True)
def run_query(query, connection):
    df = pd.read_sql(query,connection)
    return df


#st.markdown("<h2 style='text-align: center;'>Enactus HR Dashboard </h2>", unsafe_allow_html=True)

# --------------------------------------------------------------
sheet_url = st.secrets["public_gsheets_url"]
data = run_query(f"""select * from "{sheet_url}";""", conn)
#st.write(len(data))

data['member/volunteer'] = data['member/volunteer'].str.replace('A member', 'Member').replace('Recruit i.e Yet to be inducted','Recruit').replace('Recruit (yet to be Inducted)','Recruit')

kp1, kp2, kp3 = st.columns(3)

no_members = len(data)
perc_of_females = round(len(data[data['Gender'] == 'Female'])/len(data)*100,2)
perc_of_members = round(len(data[data['member/volunteer'] == 'Member'])/len(data)*100,2)

kp1.metric(label = 'Total counts of Students', value = no_members)
kp2.metric(label = 'Percentage of Female members', value = '{:0.2f}%'.format(perc_of_females))
kp3.metric(label = 'Percentage of Members', value = '{:0.2f}%'.format(perc_of_members))

st.header("")

kp4, kp5 = st.columns(2)

level_count = data['Level'].value_counts()
dept_count = data['Department'].value_counts()[:10].reset_index()
dept_count.columns = ['index', 'value']
with kp4:
    fig = px.bar(level_count, text='value',
       labels={'value':'', 'index':'Academic Level'})
    fig.update_traces(marker_color='darkblue',textposition='outside')
    fig.update_layout(width=800, height=500, bargap=0.05,plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',showlegend=False, title_text='Count of Students by Academic level', title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

with kp5:
    fig = px.pie(dept_count, values = 'value', names='index', hole=.3,color_discrete_sequence=px.colors.sequential.Blues_r)
    fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)', title_text='Distribution of top 10 departments', title_x=0.5)
    st.plotly_chart(fig)