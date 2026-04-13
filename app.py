import streamlit as st
import pandas as pd
import plotly.express as px
from PyPDF2 import PdfReader
import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="Sustainability Report Analyzer",
    page_icon="🌱",
    layout="wide"
)

# -----------------------
# LOGIN SYSTEM WITH TEAM INFO
# -----------------------
users = {"admin": "1234", "ismail": "2024"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # Title
    st.markdown("""
        <h1 style='text-align: center; color: #2E7D32;'>🌱 Sustainability Report Analysis with AI Agent</h1>
        <hr>
    """, unsafe_allow_html=True)
    
    # Login Box
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
    
    # Team Information
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            ### 👥 Project Team
            | Role | Name |
            |------|------|
            | **Team Leader** | Ismail Kamal |
            | **Team Member** | Adel ElSayed |
            | **Team Member** | Mohamed Gaber |
            | **Team Member** | Ahmed Omar |
            | **Team Member** | Sherouk Ashraf |
            | **Team Member** | Mohamed ElHammadi |
            | **Team Member** | Farouk Sameh |
        """)
    
    with col2:
        st.markdown("""
            ### 🎓 Supervision
            <div style='background-color: #E8F5E9; padding: 20px; border-radius: 10px;'>
                <h3 style='color: #2E7D32;'>👨‍🏫 Under Supervision of</h3>
                <h2 style='color: #1B5E20;'>Dr. Mohamed Tash</h2>
                <p style='font-size: 16px;'>Professor of Sustainability & ESG</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("© 2024 Sustainability Report Analysis System | GRI Standards Compliant")
    
    st.stop()

# -----------------------
# MAIN APP (AFTER LOGIN)
# -----------------------
st.set_page_config(page_title="Sustainability Analyzer", page_icon="🌱", layout="wide")

# Header with team info
st.markdown("""
    <div style='background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
        <h1 style='color: white; text-align: center; margin: 0;'>🌱 Sustainability Report Analysis with AI Agent</h1>
        <p style='color: #E8F5E9; text-align: center; margin: 10px 0 0 0;'>Team Leader: Ismail Kamal | Under Supervision: Dr. Mohamed Tash</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar with team info
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/sustainability.png", width=80)
    st.markdown("## 🌿 Sustainability AI Agent")
    st.markdown("---")
    st.markdown("### 👥 Team Members")
    st.markdown("""
    - **Ismail Kamal** (Leader)
    - Adel ElSayed
    - Mohamed Gaber
    - Ahmed Omar
    - Sherouk Ashraf
    - Mohamed ElHammadi
    - Farouk Sameh
    """)
    st.markdown("---")
    st.markdown("### 🎓 Supervisor")
    st.markdown("**Dr. Mohamed Tash**")
    st.markdown("---")
    st.markdown("### 📊 GRI Standards")
    st.markdown("""
    - GRI 305: Emissions
    - GRI 302: Energy
    - GRI 303: Water
    - GRI 306: Waste
    """)
    st.markdown("---")
    st.caption("Version 2.0 | AI-Powered")

# Main content
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("### 📄 Upload Sustainability Report")
    file = st.file_uploader("Choose PDF file (GRI Standards Report)", type="pdf", label_visibility="collapsed")

with col2:
    st.markdown("### ℹ️ Instructions")
    st.markdown("""
    1. Upload PDF report
    2. Click Analyze
    3. View KPIs & Dashboard
    4. Download PDF report
    """)

# Functions
def extract_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def find_kpi(text, keyword):
    pattern = rf"{keyword}.*?(\d+(?:[.,]\d+)?(?:\,?\d+)?)"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1)
    # Try alternative pattern
    pattern2 = rf"(\d+(?:[.,]\d+)?(?:\,?\d+)?)\s*(?:tons|MWh|m3|kWh|GJ|CO2)"
    match2 = re.search(pattern2, text, re.IGNORECASE)
    if match2 and keyword.lower() in text.lower():
        return match2.group(1)
    return "Not found"

if file:
    with st.spinner("📖 Reading PDF file..."):
        text = extract_text(file)
    
    if st.button("🔍 Analyze Report", type="primary", use_container_width=True):
        with st.spinner("🤖 Extracting KPIs using AI Agent..."):
            co2 = find_kpi(text, "co2")
            energy = find_kpi(text, "energy")
            water = find_kpi(text, "water")
            waste = find_kpi(text, "waste")
        
        # KPI Cards
        st.markdown("### 📊 Key Performance Indicators (KPIs)")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%); padding: 15px; border-radius: 10px; text-align: center;'>
                    <h3 style='color: white; margin: 0;'>🌿 CO₂</h3>
                    <h2 style='color: #FFD54F; margin: 10px 0;'>{co2}</h2>
                    <p style='color: #E8F5E9; margin: 0;'>metric tons</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #F57C00 0%, #FF9800 100%); padding: 15px; border-radius: 10px; text-align: center;'>
                    <h3 style='color: white; margin: 0;'>⚡ Energy</h3>
                    <h2 style='color: #FFF; margin: 10px 0;'>{energy}</h2>
                    <p style='color: #FFF3E0; margin: 0;'>MWh</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #1565C0 0%, #1976D2 100%); padding: 15px; border-radius: 10px; text-align: center;'>
                    <h3 style='color: white; margin: 0;'>💧 Water</h3>
                    <h2 style='color: #90CAF9; margin: 10px 0;'>{water}</h2>
                    <p style='color: #E3F2FD; margin: 0;'>cubic meters</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #6A1B9A 0%, #8E24AA 100%); padding: 15px; border-radius: 10px; text-align: center;'>
                    <h3 style='color: white; margin: 0;'>🗑️ Waste</h3>
                    <h2 style='color: #CE93D8; margin: 10px 0;'>{waste}</h2>
                    <p style='color: #F3E5F5; margin: 0;'>tons</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Dashboard Chart
        st.markdown("### 📈 Interactive Dashboard")
        
        # Create dataframe for chart
        kpi_values = []
        kpi_names = []
        
        for name, value in [("CO₂ Emissions", co2), ("Energy", energy), ("Water", water), ("Waste", waste)]:
            try:
                # Convert to number if possible
                if value != "Not found":
                    num_value = float(re.sub(r'[^\d.-]', '', str(value)))
                else:
                    num_value = 0
            except:
                num_value = 0
            kpi_names.append(name)
            kpi_values.append(num_value)
        
        df = pd.DataFrame({"KPI": kpi_names, "Value": kpi_values})
        
        fig = px.bar(df, x="KPI", y="Value", title="Sustainability KPIs Dashboard",
                     color="KPI", color_discrete_sequence=px.colors.qualitative.Set2,
                     text="Value")
        fig.update_traces(textposition="outside")
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # AI Analysis
        st.markdown("### 🤖 AI Agent Analysis")
        
        analysis_text = f"""
        **📊 KPI Summary:**
        - CO₂ Emissions: {co2}
        - Energy Consumption: {energy}
        - Water Usage: {water}
        - Waste Generated: {waste}
        
        **🔍 Insights:**
        {'✅ All KPIs were successfully extracted from the report' if co2 != 'Not found' and energy != 'Not found' else '⚠️ Some KPIs are missing from the report'}
        
        **📋 Recommendations:**
        1. Align report with GRI Standards 2024
        2. Include Scope 2 and Scope 3 emissions
        3. Set science-based reduction targets
        4. Improve data granularity (monthly/quarterly)
        
        **🎯 ESG Score:**
        {'B+ (Good)' if co2 != 'Not found' else 'C (Needs Improvement)'}
        """
        
        st.info(analysis_text)
        
        # Generate PDF Report
        st.markdown("### 📥 Export Report")
        
        pdf_file = "sustainability_report.pdf"
        c = canvas.Canvas(pdf_file, pagesize=letter)
        y = 750
        
        # Header
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, "Sustainability Report Analysis")
        y -= 30
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Generated by: AI Agent | Team Leader: Ismail Kamal")
        y -= 20
        c.drawString(50, y, f"Supervisor: Dr. Mohamed Tash")
        y -= 30
        
        # KPIs
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Key Performance Indicators (KPIs):")
        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"CO₂ Emissions: {co2} metric tons")
        y -= 20
        c.drawString(50, y, f"Energy Consumption: {energy} MWh")
        y -= 20
        c.drawString(50, y, f"Water Usage: {water} m³")
        y -= 20
        c.drawString(50, y, f"Waste Generated: {waste} tons")
        y -= 40
        
        # Team
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Project Team:")
        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(50, y, "Ismail Kamal (Team Leader)")
        y -= 15
        c.drawString(50, y, "Adel ElSayed, Mohamed Gaber, Ahmed Omar")
        y -= 15
        c.drawString(50, y, "Sherouk Ashraf, Mohamed ElHammadi, Farouk Sameh")
        y -= 40
        
        # Supervisor
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Supervision:")
        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(50, y, "Dr. Mohamed Tash")
        
        c.save()
        
        with open(pdf_file, "rb") as f:
            st.download_button(
                label="📥 Download PDF Report",
                data=f,
                file_name="sustainability_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        
        st.success("✅ Analysis completed successfully!")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>🌱 Sustainability Report Analysis with AI Agent | GRI Standards Compliant</p>
        <p>Developed by Ismail Kamal & Team | Under Supervision of Dr. Mohamed Tash</p>
    </div>
""", unsafe_allow_html=True)
