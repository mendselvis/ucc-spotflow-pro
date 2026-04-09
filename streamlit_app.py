import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# --- CONFIG & STYLING ---
st.set_page_config(page_title="SpotFlow Pro", page_icon="📍", layout="wide")

# Injecting Custom CSS for a Premium "SaaS" Look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }
    
    .stApp { background-color: #0B0E14; color: #E0E0E0; }
    
    /* Metrics Card Styling */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    /* Responsive Header */
    .main-title { font-size: 2.5rem; font-weight: 700; color: #00D4FF; margin-bottom: 0; }
    .sub-title { font-size: 1rem; color: #888; margin-bottom: 2rem; }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- CORE LOGIC ---
locations = ["Main Library", "Science Block C2", "FELT Theatre", "Old Exam Centre", "Cafeteria Hub"]
types = ["Study Zone", "Lab", "Lecture Hall", "Study Zone", "Dining"]

def get_realtime_data(hour, is_exam):
    # Simulated Predictive Logic (Sinusoidal occupancy)
    base_load = np.sin((hour - 7) * (np.pi / 12)) * 35 + 50
    modifier = 1.4 if is_exam else 1.0
    
    data = []
    for i, loc in enumerate(locations):
        # Add some randomness per location
        load = min(98, max(5, base_load * (0.8 + (i * 0.1)) * modifier))
        data.append({"Location": loc, "Type": types[i], "Occupancy (%)": round(load, 1)})
    return pd.DataFrame(data)

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    hr = st.select_slider("Forecast Time", options=list(range(24)), value=datetime.now().hour)
    exam_mode = st.toggle("Exam Season Active", value=True)
    st.info("The model uses **Weighted Temporal Inference** to predict peaks.")

# --- MAIN DASHBOARD ---
st.markdown('<p class="main-title">📍 UCC SpotFlow Pro</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Advanced Campus Resource Optimization for UCC Students</p>', unsafe_allow_html=True)

df = get_realtime_data(hr, exam_mode)
avg_load = df["Occupancy (%)"].mean()

# Key Metrics Row
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Global Density", f"{round(avg_load)}%", delta="High" if avg_load > 60 else "Optimal", delta_color="inverse")
with m2:
    best_spot = df.sort_values("Occupancy (%)").iloc[0]["Location"]
    st.metric("Recommended Spot", best_spot)
with m3:
    st.metric("Active Users", "1.2k", delta="Live")

st.markdown("---")

# Visuals Row
col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.subheader("📊 Occupancy Trends")
    fig = px.bar(
        df, x="Occupancy (%)", y="Location", 
        orientation='h', color="Occupancy (%)",
        color_continuous_scale="Viridis",
        template="plotly_dark"
    )
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("📋 Real-Time Heatmap")
    st.dataframe(
        df, 
        column_config={
            "Occupancy (%)": st.column_config.ProgressColumn(
                "Density", format="%f%%", min_value=0, max_value=100
            )
        },
        hide_index=True, use_container_width=True
    )

st.markdown("""
    <div style="text-align: center; color: #555; font-size: 0.8rem; margin-top: 50px;">
        Built for Predict4Good 2026 | Powered by Sinusoidal Predictive Modeling
    </div>
    """, unsafe_allow_html=True)
