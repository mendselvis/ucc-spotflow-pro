import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="SpotFlow Pro | UCC", page_icon="🚀", layout="wide")

# --- THE ENGINE (MODEL) ---
class SpotFlowEngine:
    def __init__(self):
        self.locations = pd.DataFrame([
            {"name": "Main Library", "base": 0.45, "cap": 1200},
            {"name": "Science Block C2", "base": 0.55, "cap": 250},
            {"name": "FELT Theatre", "base": 0.20, "cap": 800},
            {"name": "Old Exam Centre", "base": 0.15, "cap": 450},
            {"name": "Cafeteria Hub", "base": 0.40, "cap": 150}
        ])

    def get_forecast(self, hour, is_exam):
        time_weight = np.sin((hour - 8) * (np.pi / 12)) * 0.4 + 0.6
        multiplier = 1.85 if is_exam else 1.0
        results = self.locations.copy()
        results['predicted_load'] = results['base'].apply(
            lambda x: min(round((x * time_weight * multiplier) * 100, 1), 98.0)
        )
        return results

# --- THE INTERFACE (VIEW) ---
engine = SpotFlowEngine()

st.title("🚀 UCC SpotFlow Pro")
st.markdown("### *Predictive Campus Resource Optimization*")

col_ctrl, col_main = st.columns([1, 3])

with col_ctrl:
    st.header("Parameters")
    hr = st.slider("Forecast Hour (24h)", 0, 23, datetime.now().hour)
    exams = st.checkbox("Exam Window Active", value=True)
    st.divider()
    st.info("**Algorithm:** Weighted Temporal Inference v2.1")

forecast_data = engine.get_forecast(hr, exams)

with col_main:
    k1, k2, k3 = st.columns(3)
    avg_load = forecast_data['predicted_load'].mean()
    k1.metric("Avg Campus Density", f"{round(avg_load)}%")
    k2.metric("Most Available", forecast_data.loc[forecast_data['predicted_load'].idxmin()]['name'])
    k3.metric("System Status", "Live / Predictive")

    fig = go.Figure(go.Bar(
        x=forecast_data['predicted_load'],
        y=forecast_data['name'],
        orientation='h',
        marker=dict(color=forecast_data['predicted_load'], colorscale='RdYlGn_r')
    ))
    fig.update_layout(xaxis_range=[0, 100], height=400, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(forecast_data[['name', 'predicted_load', 'cap']], 
                 column_config={"name": "Location", "predicted_load": st.column_config.ProgressColumn("Load Status", format="%f%%", min_value=0, max_value=100)},
                 use_container_width=True)
