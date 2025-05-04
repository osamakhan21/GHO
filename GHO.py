import streamlit as st
import pandas as pd
import plotly.express as px
import base64

st.markdown("""
    <style>
    body, .stApp {
        background-color: #0e1117;
        color: white;
    }
    .block-container {
        padding: 1rem 1rem;
    }
    .card {
        background-color: #1c1f26;
        padding: 1rem;
        border-radius: 12px;
        border-top: 4px solid #003cff;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        margin-bottom: 12px;
        text-align: center;
    }
    .metric {
        font-size: 26px;
        font-weight: 700;
        color: #00f9ff;
    }
    .subtext {
        font-size: 15px;
        font-weight: 500;
        color: #ccc;
        margin-bottom: 6px;
    }
    [data-testid="stSidebar"] {
        background-color: #1c1f26;
        color: white;
    }
    .stButton > button {
        background-color: #ff3c3c !important;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        margin: 0.5rem 0;
        font-weight: bold;
    }
    .stSlider > div > div {
        background-color: #2c2f3a;
        padding: 8px;
        border-radius: 10px;
    }
    .card {
        background-color: #1c1f26;
        padding: 1rem;
        border-radius: 12px;
        border-top: 4px solid #003cff;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        margin-bottom: 12px;
        text-align: center;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .fixed-card {
        min-height: 10px;
        height: 130px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .card-second{
        min-height: 10px;
        height: 130px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    </style>
""", unsafe_allow_html=True)


# Load data
df = pd.read_csv("data/GHO.csv")

# Sidebar
st.sidebar.image("Blue_Flat_Illustrative_Human_Artificial_Intelligence_Technology_Logo-removebg-preview.png", width=150)

st.sidebar.markdown("## Please filter")
countries = st.sidebar.multiselect("Select Countries", df['country'].unique(), default=["India", "Pakistan"])
year_range = st.sidebar.slider("Select Year Range", int(df['year'].min()), int(df['year'].max()), (2000, 2015))

st.sidebar.button("Home")
st.sidebar.button("Prognosis")

# Filter data
df_filtered = df[(df['country'].isin(countries)) & (df['year'].between(year_range[0], year_range[1]))]
latest_year = year_range[1]
df_latest = df_filtered[df_filtered['year'] == latest_year]

import base64

# Header
with open("Blue_Flat_Illustrative_Human_Artificial_Intelligence_Technology_Logo-removebg-preview.png", "rb") as f:
    img_data = base64.b64encode(f.read()).decode()

st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: space-between; padding: 10px 0;">
        <div style="display: flex; align-items: center;">
            <img src="data:image/png;base64,{img_data}" width="55" style="border-radius: 8px;"/>
            <div style="margin-left: 15px;">
                <h1 style="margin: 0; font-size: 2.5rem;">HealthVision Dashboard</h1>
                <p style="margin: 0; font-size: 0.9rem; color: #ccc;">Empowering insights in global health</p>
            </div>
        </div>
        <div><h6 style="color: gold;">My Excel Workbook</h6></div>
    </div>
""", unsafe_allow_html=True)

# Metric Cards
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown(f"<div style='height:100%;'><div class='card'><div class='subtext'>Total Investment</div><div class='metric'>{int(df_filtered['health_exp'].sum()):,}</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
            <div class="card card-second">
            <div class='subtext'>Most Frequent</div>
            <div class='metric'>{int(df_filtered['life_expect'].mode().values[0]):,}</div>
            </div>
         """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
        <div class="card fixed-card">
            <div class='subtext'>Average</div>
            <div class='metric'>{int(df_filtered['life_expect'].mean()):,}</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"<div style='height:100%;'><div class='card'><div class='subtext'>Central Earnings</div><div class='metric'>{int(df_filtered['maternal_mortality'].median()):,}</div></div>", unsafe_allow_html=True)
with col5:
    st.markdown("""
        <div class="card fixed-card">
            <div class='subtext'>Ratings</div>
            <div class='metric'>3.51k</div>
        </div>
    """, unsafe_allow_html=True)


# Row of 3 Charts
colA, colB, colC = st.columns(3)

# Uniform 3-column layout with equal size charts
colA, colB, colC = st.columns([1, 1, 1])

# Row of 3 Charts
colA, colB, colC = st.columns([1, 1, 1])  # Keep only one columns() call

with colA:
    st.subheader("Investment by Stats")
    fig1 = px.line(df_filtered, x="year", y="health_exp", color="country", markers=True,
                   color_discrete_sequence=px.colors.sequential.Blues)
    fig1.update_layout(
        paper_bgcolor='#0e1117',
        plot_bgcolor='#0e1117',
        font_color='white',
        height=500  
    )
    st.plotly_chart(fig1, use_container_width=True)

with colB:
    st.subheader("Investment by Country")
    business = df_filtered.groupby("country")["health_exp"].sum().reset_index().sort_values(by="health_exp", ascending=False)
    fig2 = px.bar(business, x="health_exp", y="country", orientation='h', color_discrete_sequence=["#00f9ff"])
    fig2.update_layout(
        paper_bgcolor='#0e1117',
        plot_bgcolor='#0e1117',
        font_color='white',
        height=500  
    )
    st.plotly_chart(fig2, use_container_width=True)

with colC:
    st.subheader("Regions by Ratings")
    fig3 = px.pie(df_filtered, names='country', values='life_expect', hole=0.4)
    fig3.update_traces(textposition='inside', textinfo='percent+label',
                       marker=dict(line=dict(color='#000000', width=1)))
    fig3.update_layout(
        paper_bgcolor='#0e1117',
        font_color='white',
        height=500  
    )
    st.plotly_chart(fig3, use_container_width=True)


# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<center><small style='color:gray'>Developed and Maintained by Team © 2025</small></center>", unsafe_allow_html=True)
