import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# --- PRO UI INJECTION (CSS) ---
st.set_page_config(page_title="SpotFlow Pro | UCC", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    /* Card-like containers */
    div[data-testid="stMetricValue"] {
        font-size: 2rem !important;
        color: #00d4ff !important;
    }
    .main-card {
        background: #161b22;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #30363d;
        margin-bottom: 20px;
    }
    /* Responsive adjustment */
    @media (max-width: 640px) {
        .stMetric {
            margin-bottom: 10px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# --- THE ENGINE ---
class SpotFlowEngine:
    def __init__(self):
        self.locations = pd.DataFrame([
            {"name": "Main Library", "base": 0.45, "cap": 1200, "type": "Study"},
            {"name": "Science Block C2", "base": 0.55, "cap": 250, "type": "Lab"},
            {"name": "FELT Theatre", "base": 0.20, "cap": 800, "type": "Lecture"},
            {"name": "Old Exam Centre", "base": 0.15, "cap": 450, "type": "Study"},
            {"name": "Cafeteria Hub", "base": 0.40, "cap": 150, "type": "Social"}
        ])

    def get_forecast(self, hour, is_exam):
        # Math: Sinusoidal wave + Exam Multiplier
        time_weight = np.sin((hour - 8) * (np.pi / 12)) * 0.4 + 0.6
        multiplier = 1.85 if is_exam else 1.0
        results = self.locations.copy()
        results['load'] = results['base'].apply(
            lambda x: min(round((x * time_weight * multiplier) * 100, 1), 98.0)
        )
        return results

engine = SpotFlowEngine()

# --- THE INTERFACE ---
st.title("🚀 UCC SpotFlow Pro")
st.caption("Predictive Analytics for Campus Congestion Management")

# Sidebar for Mobile-Friendly Controls
with st.sidebar:
    st.header("🎛️ Control Center")
    hr = st.select_slider("Select Time of Day", options=list(range(24)), value=datetime.now().hour)
    exams = st.toggle("Exam Window Active", value=True)
    st.divider()
    st.markdown("### Model Version\n`v2.5-Stable-Prod`")

# Calculations
data = engine.get_forecast(hr, exams)
avg_load = data['load'].mean()

# Responsive Metrics Row
k1, k2, k3 = st.columns(3)
with k1:
    st.metric("Avg Campus Density", f"{round(avg_load)}%", delta="-2%" if avg_load < 50 else "+5%", delta_color="inverse")
with k2:
    available = data.loc[data['load'].idxmin()]['name']
    st.metric("Best Study Spot", available)
with k3:
    st.metric("System Health", "Operational", delta="99.9% Uptime")

st.divider()

# Main Visuals
col_chart, col_table = st.columns([2, 1])

with col_chart:
    st.subheader("Live Congestion Forecast")
    # Custom Styled Plotly Chart
    fig = go.Figure(go.Bar(
        x=data['load'],
        y=data['name'],
        orientation='h',
        marker=dict(
            color=data['load'],
            colorscale='Viridis',
            line=dict(color='rgba(255, 255, 255, 0.5)', width=1)
        )
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),
        xaxis=dict(range=[0, 100], title="Occupancy %", gridcolor='#30363d'),
        yaxis=dict(autorange="reversed"),
        margin=dict(l=0, r=0, t=20, b=20),
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

with col_table:
    st.subheader("Location Details")
    st.dataframe(
        data[['name', 'type', 'load']],
        column_config={
            "name": "Location",
            "type": "Category",
            "load": st.column_config.ProgressColumn("Load", format="%f%%", min_value=0, max_value=100)
        },
        hide_index=True,
        use_container_width=True
    )

st.markdown("---")
st.markdown("Created for **Predict4Good Hackathon** | Data powered by UCC Facilities API (Simulated)")
