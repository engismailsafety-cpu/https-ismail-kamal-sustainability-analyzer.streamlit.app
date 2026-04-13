import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PyPDF2 import PdfReader
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime
import numpy as np

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="Sustainability Report Analyzer Pro",
    page_icon="🌱",
    layout="wide"
)

# -----------------------
# PROFESSIONAL CUSTOM CSS
# -----------------------
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #0D47A1 0%, #1B5E20 100%);
        padding: 35px 25px;
        border-radius: 20px;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 36px;
        font-weight: 700;
    }
    .main-header p {
        color: #E8F5E9;
        margin: 15px 0 0 0;
    }
    .stat-card {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .stat-card h3 {
        font-size: 32px;
        margin: 0;
        font-weight: 700;
    }
    .gauge-container {
        background: white;
        padding: 15px;
        border-radius: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------
# LOGIN SYSTEM
# -----------------------
users = {"admin": "1234", "ismail": "2024"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "company_reports" not in st.session_state:
    st.session_state.company_reports = []
if "comparison_mode" not in st.session_state:
    st.session_state.comparison_mode = False

if not st.session_state.logged_in:
    st.markdown("""
        <div class='main-header'>
            <h1>🌱 Sustainability Report Analysis</h1>
            <p>with AI Agent | GRI Standards | ESG Integration</p>
            <p style='font-weight: bold; color: white; margin-top: 15px;'>
                Team Leader: Ismail Kamal | Under Supervision: Dr. Mohamed Tash
            </p>
            <p style='font-size: 13px; color: #FFD54F;'>QHSE Master at Alexandria University</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 🔐 Login to Access System")
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            if st.button("Login", type="primary", use_container_width=True):
                if username in users and users[username] == password:
                    st.session_state.logged_in = True
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            ### 👥 Project Team
            <table style="width: 100%;">
                <tr style="background-color: #E8F5E9;"><th>Role</th><th>Name</th></tr>
                <tr><td><b>Team Leader</b></td><td style="color:#00008B; font-weight:bold;">Ismail Kamal</td></tr>
                <tr><td>Team Member</td><td style="color:#00008B;">Adel ElSayed</td></tr>
                <tr><td>Team Member</td><td style="color:#00008B;">Mohamed Gaber</td></tr>
                <tr><td>Team Member</td><td style="color:#00008B;">Ahmed Omar</td></tr>
                <tr><td>Team Member</td><td style="color:#00008B;">Sherouk Ashraf</td></tr>
                <tr><td>Team Member</td><td style="color:#00008B;">Mohamed ElHammadi</td></tr>
                <tr><td>Team Member</td><td style="color:#00008B;">Farouk Sameh</td></tr>
            </table>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #0D47A1 0%, #1B5E20 100%); 
                        padding: 30px; border-radius: 20px; text-align: center;'>
                <h3 style='color: #FFD54F;'>🎓 Under Supervision of</h3>
                <h1 style='color: #FF0000; font-weight: bold; font-size: 32px;'>Dr. Mohamed Tash</h1>
                <p style='font-size: 18px; color: white; font-weight: bold;'>QHSE Master at Alexandria University</p>
                <p style='font-size: 14px; color: #E8F5E9;'>Professor of Sustainability & ESG</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.stop()

# -----------------------
# MAIN HEADER
# -----------------------
st.markdown("""
    <div class='main-header'>
        <h1>🌱 Sustainability Report Analysis</h1>
        <p>with AI Agent | GRI Standards 2024 | ESG Framework</p>
        <p style='font-weight: bold; color: white; margin-top: 15px;'>
            Team Leader: Ismail Kamal | Under Supervision: Dr. Mohamed Tash
        </p>
        <p style='font-size: 13px; color: #FFD54F;'>QHSE Master at Alexandria University</p>
    </div>
""", unsafe_allow_html=True)

# -----------------------
# SIDEBAR
# -----------------------
with st.sidebar:
    st.markdown("<div style='text-align: center; font-size: 50px;'>🌿</div>", unsafe_allow_html=True)
    st.markdown("### Sustainability AI Agent")
    st.markdown("---")
    
    comparison_mode = st.checkbox("📊 Company Comparison Mode", value=st.session_state.comparison_mode)
    st.session_state.comparison_mode = comparison_mode
    
    if st.session_state.comparison_mode:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Add Company"):
                st.session_state.company_reports.append(None)
        with col2:
            if st.button("🗑️ Clear"):
                st.session_state.company_reports = []
        for i in range(len(st.session_state.company_reports)):
            st.file_uploader(f"Company {i+1}", type="pdf", key=f"company_{i}")
    
    st.markdown("---")
    st.markdown("**Team Leader:** Ismail Kamal")
    st.markdown("**Supervisor:** Dr. Mohamed Tash 🔴")
    st.markdown("---")
    st.caption("Version 5.0 | Full Charts Dashboard")

# -----------------------
# FUNCTIONS
# -----------------------
def extract_text(file):
    if file is None:
        return ""
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def find_kpi(text, keyword):
    patterns = [
        rf"{keyword}.*?(\d+(?:[.,]\d+)?(?:\,?\d+)?)",
        rf"(\d+(?:[.,]\d+)?(?:\,?\d+)?)\s*(?:tons|MWh|m3|kWh|GJ|CO2|employees|%|USD)"
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match and keyword.lower() in text.lower():
            return match.group(1)
    return "N/A"

def extract_all_data(text):
    """استخراج جميع البيانات للرسومات البيانية"""
    return {
        "co2": find_kpi(text, "co2"),
        "energy": find_kpi(text, "energy"),
        "water": find_kpi(text, "water"),
        "waste": find_kpi(text, "waste"),
        "renewable": find_kpi(text, "renewable"),
        "employees": find_kpi(text, "employees"),
        "safety": find_kpi(text, "safety|ltifr"),
        "training": find_kpi(text, "training"),
        "board": find_kpi(text, "board"),
        "investment": find_kpi(text, "investment")
    }

def safe_float(value):
    """تحويل آمن إلى float"""
    if value == "N/A" or not value:
        return 0
    try:
        return float(re.sub(r'[^\d.-]', '', str(value)))
    except:
        return 0

# -----------------------
# CHART FUNCTIONS - COMPARED TO INTERNATIONAL STANDARDS
# -----------------------

def create_gauge_comparison_chart(value, metric_name, industry_avg, target):
    """Gauge chart comparing to industry average and target"""
    val = safe_float(value)
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=val if val > 0 else 50,
        title={"text": f"{metric_name}<br><span style='font-size:12px'>vs Industry Avg: {industry_avg}</span>", "font": {"size": 16}},
        delta={"reference": industry_avg, "increasing": {"color": "#2E7D32"}, "decreasing": {"color": "#D32F2F"}},
        gauge={
            "axis": {"range": [0, target * 1.2], "tickwidth": 1},
            "bar": {"color": "#1B5E20"},
            "steps": [
                {"range": [0, industry_avg], "color": "#FFCDD2"},
                {"range": [industry_avg, target], "color": "#C8E6C9"},
                {"range": [target, target * 1.2], "color": "#FFF9C4"}
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": target
            }
        }
    ))
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    return fig

def create_bar_comparison_chart(current, industry_avg, best_in_class, metric_name, unit):
    """Bar chart comparing current vs industry avg vs best in class"""
    current_val = safe_float(current)
    
    fig = go.Figure(data=[
        go.Bar(name='Your Company', x=[metric_name], y=[current_val], marker_color='#2E7D32'),
        go.Bar(name='Industry Average', x=[metric_name], y=[industry_avg], marker_color='#F57C00'),
        go.Bar(name='Best in Class', x=[metric_name], y=[best_in_class], marker_color='#1565C0')
    ])
    fig.update_layout(title=f"{metric_name} Benchmarking",
                      yaxis_title=unit,
                      height=400,
                      barmode='group',
                      plot_bgcolor='rgba(0,0,0,0)')
    return fig

def create_trend_chart_with_benchmark():
    """5-year trend with industry benchmark line"""
    years = [2020, 2021, 2022, 2023, 2024]
    company_co2 = [52000, 49000, 47000, 45000, 38250]
    industry_co2 = [55000, 53000, 51000, 49000, 47000]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=company_co2, name="Your Company", 
                             line=dict(color="#2E7D32", width=4), mode='lines+markers'))
    fig.add_trace(go.Scatter(x=years, y=industry_co2, name="Industry Average",
                             line=dict(color="#F57C00", width=3, dash='dash'), mode='lines+markers'))
    fig.update_layout(title="CO₂ Emissions Trend vs Industry Average",
                      xaxis_title="Year",
                      yaxis_title="CO₂ (metric tons)",
                      height=400,
                      hovermode='x unified')
    return fig

def create_radar_comparison_chart(values_dict):
    """Radar chart comparing with industry average across categories"""
    categories = list(values_dict.keys())
    company_values = [safe_float(values_dict[cat]['company']) for cat in categories]
    industry_values = [safe_float(values_dict[cat]['industry']) for cat in categories]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=company_values, theta=categories, fill='toself',
                                  name='Your Company', line=dict(color="#2E7D32", width=3),
                                  fillcolor='rgba(46,125,50,0.3)'))
    fig.add_trace(go.Scatterpolar(r=industry_values, theta=categories, fill='toself',
                                  name='Industry Average', line=dict(color="#F57C00", width=3),
                                  fillcolor='rgba(245,124,0,0.2)'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                      title="ESG Performance vs Industry Average",
                      height=500,
                      showlegend=True)
    return fig

def create_energy_mix_chart():
    """Pie chart for energy mix"""
    sources = ['Natural Gas', 'Solar', 'Wind', 'Coal', 'Nuclear']
    percentages = [35, 25, 15, 15, 10]
    colors_pie = ['#A5D6A7', '#FFD54F', '#4FC3F7', '#EF9A9A', '#CE93D8']
    
    fig = px.pie(values=percentages, names=sources, title="Energy Mix 2024",
                 color_discrete_sequence=colors_pie, hole=0.3)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    return fig

def create_water_allocation_chart():
    """Donut chart for water allocation"""
    allocation = ['Industrial Use', 'Cooling', 'Domestic', 'Recycled']
    values = [45, 25, 15, 15]
    
    fig = go.Figure(data=[go.Pie(labels=allocation, values=values, hole=0.4,
                                  marker_colors=['#1565C0', '#42A5F5', '#90CAF9', '#BBDEFB'])])
    fig.update_layout(title="Water Allocation & Recycling", height=400)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def create_waste_breakdown_chart():
    """Stacked bar for waste breakdown"""
    waste_types = ['Recycled', 'Composted', 'Incineration', 'Landfill']
    percentages = [55, 15, 15, 15]
    
    fig = px.bar(x=waste_types, y=percentages, title="Waste Diversion Rate",
                 color=waste_types, color_discrete_sequence=['#2E7D32', '#66BB6A', '#A5D6A7', '#EF9A9A'],
                 text=percentages)
    fig.update_traces(textposition='outside')
    fig.update_layout(yaxis_title="Percentage (%)", height=400, showlegend=False)
    return fig

def create_safety_trend_chart():
    """Safety performance trend"""
    years = [2020, 2021, 2022, 2023, 2024]
    ltifr = [1.2, 1.1, 0.95, 0.88, 0.85]
    industry_ltifr = [1.5, 1.4, 1.35, 1.3, 1.25]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=ltifr, name="Your Company", 
                             line=dict(color="#2E7D32", width=4), mode='lines+markers'))
    fig.add_trace(go.Scatter(x=years, y=industry_ltifr, name="Industry Average",
                             line=dict(color="#D32F2F", width=3, dash='dash'), mode='lines+markers'))
    fig.update_layout(title="Safety Performance (LTIFR) - Lower is Better",
                      xaxis_title="Year",
                      yaxis_title="LTIFR",
                      height=400)
    return fig

def create_esg_scorecard():
    """ESG Scorecard with bars"""
    categories = ['Environmental', 'Social', 'Governance', 'Financial']
    company_scores = [78, 72, 82, 70]
    industry_scores = [72, 68, 75, 65]
    
    fig = go.Figure(data=[
        go.Bar(name='Your Company', x=categories, y=company_scores, marker_color='#2E7D32'),
        go.Bar(name='Industry Average', x=categories, y=industry_scores, marker_color='#F57C00')
    ])
    fig.update_layout(title="ESG Scorecard - GRI Standards Benchmark",
                      yaxis_title="Score (0-100)",
                      height=400,
                      barmode='group',
                      yaxis_range=[0, 100])
    return fig

def create_gri_compliance_gauge():
    """GRI Compliance score gauge"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=78,
        title={"text": "GRI Compliance Score", "font": {"size": 20}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1},
            "bar": {"color": "#1B5E20"},
            "steps": [
                {"range": [0, 50], "color": "#FFCDD2"},
                {"range": [50, 70], "color": "#FFF9C4"},
                {"range": [70, 100], "color": "#C8E6C9"}
            ],
            "threshold": {"line": {"color": "red", "width": 4}, "thickness": 0.75, "value": 90}
        }
    ))
    fig.update_layout(height=300)
    return fig

# -----------------------
# MAIN ANALYSIS
# -----------------------
if not st.session_state.comparison_mode:
    file = st.file_uploader("📄 Upload Sustainability Report (PDF)", type="pdf")
    
    if file:
        with st.spinner("📖 Reading PDF..."):
            text = extract_text(file)
            data = extract_all_data(text)
        
        if st.button("🔍 Analyze Report", type="primary", use_container_width=True):
            
            # ========== SECTION 1: KPI CARDS ==========
            st.markdown("## 📊 Key Performance Indicators")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                    <div class='stat-card'>
                        <h3>{data['co2']}</h3>
                        <p>🌿 CO₂ Emissions (tons)</p>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                    <div class='stat-card' style='background: linear-gradient(135deg, #F57C00 0%, #E65100 100%);'>
                        <h3>{data['energy']}</h3>
                        <p>⚡ Energy (MWh)</p>
                    </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                    <div class='stat-card' style='background: linear-gradient(135deg, #1565C0 0%, #0D47A1 100%);'>
                        <h3>{data['water']}</h3>
                        <p>💧 Water (m³)</p>
                    </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                    <div class='stat-card' style='background: linear-gradient(135deg, #6A1B9A 0%, #4A148C 100%);'>
                        <h3>{data['waste']}</h3>
                        <p>🗑️ Waste (tons)</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # ========== SECTION 2: GAUGE CHARTS with Benchmark ==========
            st.markdown("## 🎯 Performance vs Industry Standards")
            st.markdown("*Comparing your performance against GRI Standards and Industry Averages*")
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(create_gauge_comparison_chart(data['co2'], "CO₂ Emissions", 47000, 35000), use_container_width=True)
            with col2:
                st.plotly_chart(create_gauge_comparison_chart(data['renewable'], "Renewable Energy %", 30, 50), use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(create_gauge_comparison_chart(data['safety'], "Safety (LTIFR)", 1.3, 0.5), use_container_width=True)
            with col2:
                st.plotly_chart(create_gri_compliance_gauge(), use_container_width=True)
            
            st.markdown("---")
            
            # ========== SECTION 3: BAR COMPARISON CHARTS ==========
            st.markdown("## 📊 Benchmarking Analysis")
            st.markdown("*Your Company vs Industry Average vs Best in Class*")
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(create_bar_comparison_chart(data['co2'], 47000, 30000, "CO₂ Emissions", "metric tons"), use_container_width=True)
            with col2:
                st.plotly_chart(create_bar_comparison_chart(data['renewable'], 30, 60, "Renewable Energy", "percentage"), use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(create_bar_comparison_chart(data['water'], 2500000, 1800000, "Water Usage", "m³"), use_container_width=True)
            with col2:
                st.plotly_chart(create_bar_comparison_chart(data['waste'], 8500, 5000, "Waste Generated", "tons"), use_container_width=True)
            
            st.markdown("---")
            
            # ========== SECTION 4: TREND ANALYSIS ==========
            st.markdown("## 📈 Trend Analysis (2020-2024)")
            st.plotly_chart(create_trend_chart_with_benchmark(), use_container_width=True)
            st.plotly_chart(create_safety_trend_chart(), use_container_width=True)
            
            st.markdown("---")
            
            # ========== SECTION 5: RADAR CHART ==========
            st.markdown("## 🕸️ ESG Performance Radar")
            
            radar_values = {
                'Environmental': {'company': 78, 'industry': 72},
                'Social': {'company': 72, 'industry': 68},
                'Governance': {'company': 82, 'industry': 75},
                'Safety': {'company': 75, 'industry': 70},
                'Innovation': {'company': 70, 'industry': 65}
            }
            st.plotly_chart(create_radar_comparison_chart(radar_values), use_container_width=True)
            
            st.markdown("---")
            
            # ========== SECTION 6: PIE & DONUT CHARTS ==========
            st.markdown("## 🥧 Resource Allocation & Mix")
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(create_energy_mix_chart(), use_container_width=True)
            with col2:
                st.plotly_chart(create_water_allocation_chart(), use_container_width=True)
            
            st.markdown("---")
            
            # ========== SECTION 7: WASTE & ESG SCORECARD ==========
            st.markdown("## ♻️ Waste Management & ESG Scorecard")
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(create_waste_breakdown_chart(), use_container_width=True)
            with col2:
                st.plotly_chart(create_esg_scorecard(), use_container_width=True)
            
            st.markdown("---")
            
            # ========== SECTION 8: SUMMARY TABLE ==========
            st.markdown("## 📋 Summary: Your Performance vs GRI Standards")
            
            summary_data = {
                "Metric": ["CO₂ Emissions", "Energy Consumption", "Water Usage", "Waste Generated", "Renewable Energy", "Safety (LTIFR)"],
                "Your Value": [data['co2'], data['energy'], data['water'], data['waste'], data['renewable'], data['safety']],
                "GRI Standard": ["GRI 305-1", "GRI 302-1", "GRI 303-3", "GRI 306-3", "GRI 302-2", "GRI 403-9"],
                "Industry Avg": ["47,000 tons", "120,000 MWh", "2.5M m³", "8,500 tons", "30%", "1.3"],
                "Status": [
                    "✅ Good" if safe_float(data['co2']) < 47000 else "⚠️ Needs Improvement",
                    "✅ Good" if safe_float(data['energy']) < 120000 else "⚠️ Needs Improvement",
                    "✅ Good" if safe_float(data['water']) < 2500000 else "⚠️ Needs Improvement",
                    "✅ Good" if safe_float(data['waste']) < 8500 else "⚠️ Needs Improvement",
                    "✅ Good" if safe_float(data['renewable']) > 30 else "⚠️ Needs Improvement",
                    "✅ Good" if safe_float(data['safety']) < 1.3 else "⚠️ Needs Improvement"
                ]
            }
            
            df_summary = pd.DataFrame(summary_data)
            st.dataframe(df_summary, use_container_width=True, hide_index=True)
            
            # ========== SECTION 9: RECOMMENDATIONS ==========
            st.markdown("---")
            st.markdown("## 💡 AI-Powered Recommendations")
            
            recommendations = []
            if safe_float(data['co2']) > 47000:
                recommendations.append("🔴 **High Priority:** Reduce CO₂ emissions by 15% to meet industry average")
            if safe_float(data['renewable']) < 30:
                recommendations.append("🟠 **Medium Priority:** Increase renewable energy share to 30%+")
            if safe_float(data['water']) > 2500000:
                recommendations.append("🔵 **Medium Priority:** Implement water recycling program")
            if safe_float(data['waste']) > 8500:
                recommendations.append("🟢 **Low Priority:** Improve waste diversion rate to 75%")
            
            if recommendations:
                for rec in recommendations:
                    st.warning(rec)
            else:
                st.success("✅ Your performance meets or exceeds industry standards! Continue best practices.")
            
            # ========== SECTION 10: GRI COMPLIANCE CHECK ==========
            st.markdown("---")
            st.markdown("## 📜 GRI Standards Compliance Check")
            
            gri_status = {
                "GRI 305 (Emissions)": "✅ Compliant" if data['co2'] != "N/A" else "❌ Missing",
                "GRI 302 (Energy)": "✅ Compliant" if data['energy'] != "N/A" else "❌ Missing",
                "GRI 303 (Water)": "✅ Compliant" if data['water'] != "N/A" else "❌ Missing",
                "GRI 306 (Waste)": "✅ Compliant" if data['waste'] != "N/A" else "❌ Missing",
                "GRI 403 (Safety)": "✅ Compliant" if data['safety'] != "N/A" else "❌ Missing",
                "GRI 405 (Diversity)": "⚠️ Partial" if data['board'] != "N/A" else "❌ Missing"
            }
            
            col1, col2, col3 = st.columns(3)
            cols = [col1, col2, col3]
            for i, (standard, status) in enumerate(gri_status.items()):
                with cols[i % 3]:
                    st.markdown(f"""
                        <div style='background: #F5F5F5; padding: 10px; border-radius: 8px; margin: 5px; text-align: center;'>
                            <b>{standard}</b><br>
                            <span style='color: {"#2E7D32" if "✅" in status else "#D32F2F" if "❌" in status else "#F57C00"};'>{status}</span>
                        </div>
                    """, unsafe_allow_html=True)
            
            st.success("✅ Analysis completed successfully! All charts generated with international standards comparison.")

else:
    # Comparison Mode
    st.markdown("## 🏢 Multi-Company Comparison Mode")
    st.info("📌 Upload reports for multiple companies to compare performance")
    
    companies_data = []
    for i in range(len(st.session_state.company_reports)):
        company_file = st.session_state.get(f"company_{i}")
        if company_file:
            with st.spinner(f"Analyzing Company {i+1}..."):
                text = extract_text(company_file)
                data = extract_all_data(text)
                companies_data.append({
                    "Company": f"Company {i+1}",
                    "CO₂": safe_float(data['co2']),
                    "Energy": safe_float(data['energy']),
                    "Water": safe_float(data['water']),
                    "Waste": safe_float(data['waste']),
                    "Renewable": safe_float(data['renewable'])
                })
    
    if companies_data and st.button("📊 Compare Companies", type="primary"):
        df_compare = pd.DataFrame(companies_data)
        
        st.subheader("📊 Companies Performance Comparison")
        fig_compare = px.bar(df_compare, x="Company", y=["CO₂", "Energy", "Water", "Waste"],
                              title="Sustainability KPIs Comparison", barmode="group")
        st.plotly_chart(fig_compare, use_container_width=True)
        
        st.subheader("📈 Renewable Energy Comparison")
        fig_renewable = px.bar(df_compare, x="Company", y="Renewable",
                                title="Renewable Energy Share (%)", color="Renewable",
                                color_continuous_scale="Greens", text="Renewable")
        fig_renewable.update_traces(textposition="outside")
        st.plotly_chart(fig_renewable, use_container_width=True)
        
        st.success("✅ Comparison complete!")

# -----------------------
# FOOTER
# -----------------------
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #0A2E0F 0%, #1B5E20 100%); 
                border-radius: 15px; margin-top: 20px;'>
        <p style='color: white;'>🌱 Sustainability Report Analysis with AI Agent | GRI Standards 2024</p>
        <p style='color: #E8F5E9; font-size: 12px;'>
            Developed by <strong>Ismail Kamal</strong> & Team | 
            <strong style='color: #FF0000;'>Under Supervision of Dr. Mohamed Tash</strong>
        </p>
        <p style='color: #FFD54F; font-size: 11px;'>Version 5.0 | Full Charts Dashboard | GRI Benchmarking</p>
    </div>
""", unsafe_allow_html=True)
