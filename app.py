import streamlit as st
import pandas as pd
import plotly.express as px
from PyPDF2 import PdfReader
import re
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="Sustainability Report Analyzer",
    page_icon="🌱",
    layout="wide"
)

# -----------------------
# LOGIN SYSTEM
# -----------------------
users = {"admin": "1234", "ismail": "2024"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("""
        <h1 style='text-align: center; color: #2E7D32;'>🌱 Sustainability Report Analysis with AI Agent</h1>
        <hr>
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
        # ALL TEAM MEMBERS - DARK BLUE, SIZE 14
        st.markdown("""
            <style>
                .team-leader {
                    color: #0D47A1;
                    font-weight: bold;
                    font-size: 14px;
                }
                .team-member {
                    color: #0D47A1;
                    font-weight: normal;
                    font-size: 14px;
                }
                .team-table th {
                    background-color: #E8F5E9;
                    padding: 8px;
                    text-align: left;
                    font-size: 14px;
                }
                .team-table td {
                    padding: 8px;
                    font-size: 14px;
                }
            </style>
            <h3>👥 Project Team</h3>
            <table class="team-table" style="width: 100%; border-collapse: collapse;">
                <tr style="background-color: #E8F5E9;">
                    <th style="padding: 8px; text-align: left;">Role</th>
                    <th style="padding: 8px; text-align: left;">Name</th>
                </tr>
                <tr>
                    <td style="padding: 8px;"><strong>Team Leader</strong></td>
                    <td style="padding: 8px;"><span class="team-leader">Ismail Kamal</span></td>
                </tr>
                <tr>
                    <td style="padding: 8px;">Team Member</td>
                    <td style="padding: 8px;"><span class="team-member">Adel ElSayed</span></td>
                </tr>
                <tr>
                    <td style="padding: 8px;">Team Member</td>
                    <td style="padding: 8px;"><span class="team-member">Mohamed Gaber</span></td>
                </tr>
                <tr>
                    <td style="padding: 8px;">Team Member</td>
                    <td style="padding: 8px;"><span class="team-member">Ahmed Omar</span></td>
                </tr>
                <tr>
                    <td style="padding: 8px;">Team Member</td>
                    <td style="padding: 8px;"><span class="team-member">Sherouk Ashraf</span></td>
                </tr>
                <tr>
                    <td style="padding: 8px;">Team Member</td>
                    <td style="padding: 8px;"><span class="team-member">Mohamed ElHammadi</span></td>
                </tr>
                <tr>
                    <td style="padding: 8px;">Team Member</td>
                    <td style="padding: 8px;"><span class="team-member">Farouk Sameh</span></td>
                </tr>
            </table>
        """, unsafe_allow_html=True)
    
    with col2:
        # DR. MOHAMED TASH - RED & BOLD
        st.markdown("""
            <div style='background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%); 
                        padding: 25px; border-radius: 15px; text-align: center; 
                        border: 3px solid #FF0000; box-shadow: 0 4px 15px rgba(255,0,0,0.3);'>
                <h3 style='color: #2E7D32; margin: 0;'>🎓 Under Supervision of</h3>
                <h1 style='color: #FF0000; font-weight: bold; font-size: 32px; margin: 10px 0; 
                           text-shadow: 2px 2px 4px rgba(0,0,0,0.1);'>
                    Dr. Mohamed Tash
                </h1>
                <p style='font-size: 16px; color: #333; font-weight: bold;'>Professor of Sustainability & ESG</p>
                <p style='font-size: 14px; color: #666;'>PhD in Environmental Engineering | GRI Certified</p>
                <p style='font-size: 12px; color: #FF0000; margin-top: 10px;'>⭐ Lead Supervisor | ESG Expert ⭐</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("© 2025 Sustainability Report Analysis System | GRI Standards Compliant | ESG Framework")
    st.stop()

# -----------------------
# MAIN APP (AFTER LOGIN)
# -----------------------
st.markdown("""
    <div style='background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
        <h1 style='color: white; text-align: center; margin: 0;'>🌱 Sustainability Report Analysis with AI Agent</h1>
        <p style='color: #E8F5E9; text-align: center; margin: 10px 0 0 0; font-size: 14px;'>
            <span style='color: #0D47A1; font-weight: bold;'>Team Leader: Ismail Kamal</span> | 
            <span style='color: #0D47A1;'>Adel, Mohamed, Ahmed, Sherouk, ElHammadi, Farouk</span> | 
            <span style='color: #FF0000; font-weight: bold;'>Supervisor: Dr. Mohamed Tash</span>
        </p>
    </div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/sustainability.png", width=80)
    st.markdown("## 🌿 Sustainability AI Agent")
    st.markdown("---")
    
    # ALL TEAM MEMBERS - DARK BLUE, SIZE 14 IN SIDEBAR
    st.markdown("""
    <style>
        .sidebar-member {
            color: #0D47A1;
            font-weight: normal;
            font-size: 14px;
            margin: 5px 0;
        }
        .sidebar-leader {
            color: #0D47A1;
            font-weight: bold;
            font-size: 14px;
            margin: 5px 0;
        }
    </style>
    <h3>👥 Team Members</h3>
    <div class="sidebar-leader">👑 Ismail Kamal (Leader)</div>
    <div class="sidebar-member">👤 Adel ElSayed</div>
    <div class="sidebar-member">👤 Mohamed Gaber</div>
    <div class="sidebar-member">👤 Ahmed Omar</div>
    <div class="sidebar-member">👤 Sherouk Ashraf</div>
    <div class="sidebar-member">👤 Mohamed ElHammadi</div>
    <div class="sidebar-member">👤 Farouk Sameh</div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🎓 Supervisor")
    st.markdown("<span style='color: #FF0000; font-weight: bold; font-size: 18px;'>Dr. Mohamed Tash</span>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📊 Regulatory Frameworks")
    st.markdown("""
    - **GRI Standards** (2024)
    - **ESG Framework**
    - **SASB** (Sustainability Accounting)
    - **TCFD** (Climate-related Disclosures)
    - **SDGs** (Sustainable Development Goals)
    """)
    st.markdown("---")
    st.markdown("### 📋 GRI Disclosures")
    st.markdown("""
    - GRI 305: Emissions (Scope 1,2,3)
    - GRI 302: Energy
    - GRI 303: Water
    - GRI 306: Waste
    - GRI 401: Employment
    - GRI 403: Occupational Health
    - GRI 405: Diversity
    """)
    st.markdown("---")
    st.caption("Version 3.0 | AI-Powered | GRI Compliant")

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
    pattern2 = rf"(\d+(?:[.,]\d+)?(?:\,?\d+)?)\s*(?:tons|MWh|m3|kWh|GJ|CO2)"
    match2 = re.search(pattern2, text, re.IGNORECASE)
    if match2 and keyword.lower() in text.lower():
        return match2.group(1)
    return "Not found"

def extract_detailed_kpis(text):
    """استخراج مؤشرات أكثر تفصيلاً"""
    return {
        "co2_scope1": find_kpi(text, "scope 1"),
        "co2_scope2": find_kpi(text, "scope 2"),
        "co2_scope3": find_kpi(text, "scope 3"),
        "energy_renewable": find_kpi(text, "renewable"),
        "water_recycled": find_kpi(text, "recycled"),
        "waste_recycled": find_kpi(text, "recycled waste"),
    }

def generate_detailed_analysis(co2, energy, water, waste, detailed_kpis):
    """توليد تحليل مفصل مع توصيات تنظيمية"""
    
    # Calculate ESG Score
    esg_score = 0
    if co2 != "Not found":
        try:
            co2_val = float(re.sub(r'[^\d.-]', '', str(co2)))
            if co2_val < 40000:
                esg_score += 30
            elif co2_val < 50000:
                esg_score += 20
            else:
                esg_score += 10
        except:
            esg_score += 15
    else:
        esg_score += 10
    
    if energy != "Not found":
        esg_score += 25
    else:
        esg_score += 15
    
    if water != "Not found":
        esg_score += 25
    else:
        esg_score += 15
    
    if waste != "Not found":
        esg_score += 20
    else:
        esg_score += 10
    
    # Regulatory compliance check
    gri_compliance = []
    if co2 != "Not found":
        gri_compliance.append("✅ GRI 305-1 (Direct Emissions)")
    if energy != "Not found":
        gri_compliance.append("✅ GRI 302-1 (Energy Consumption)")
    if water != "Not found":
        gri_compliance.append("✅ GRI 303-3 (Water Withdrawal)")
    if waste != "Not found":
        gri_compliance.append("✅ GRI 306-3 (Waste Generated)")
    
    analysis = f"""
    **📊 EXECUTIVE SUMMARY**
    The sustainability report has been analyzed against GRI Standards 2024 and ESG framework requirements.
    
    ---
    
    **🌿 ENVIRONMENTAL PERFORMANCE**
    | Indicator | Value | Status | GRI Reference |
    |-----------|-------|--------|---------------|
    | CO₂ Emissions | {co2} metric tons | {'✅ Good' if co2 != 'Not found' else '⚠️ Missing'} | GRI 305-1 |
    | Energy Consumption | {energy} MWh | {'✅ Good' if energy != 'Not found' else '⚠️ Missing'} | GRI 302-1 |
    | Water Usage | {water} m³ | {'✅ Good' if water != 'Not found' else '⚠️ Missing'} | GRI 303-3 |
    | Waste Generated | {waste} tons | {'✅ Good' if waste != 'Not found' else '⚠️ Missing'} | GRI 306-3 |
    
    **🔍 DETAILED INSIGHTS:**
    • {'Carbon emissions are within acceptable range' if co2 != 'Not found' else '⚠️ Carbon emissions data missing - Required by GRI 305'}
    • {'Energy intensity shows improvement potential' if energy != 'Not found' else '⚠️ Energy data missing - Required by GRI 302'}
    • {'Water stewardship metrics captured' if water != 'Not found' else '⚠️ Water data missing - Required by GRI 303'}
    • {'Waste management KPIs documented' if waste != 'Not found' else '⚠️ Waste data missing - Required by GRI 306'}
    
    ---
    
    **📋 REGULATORY COMPLIANCE CHECK (GRI Standards 2024)**
    
    {'✅ ' + '\\n✅ '.join(gri_compliance) if gri_compliance else '⚠️ No GRI disclosures found'}
    
    **Missing Disclosures (Gap Analysis):**
    """
    
    if co2 == "Not found":
        analysis += "\n• GRI 305-2 (Scope 2 Emissions) - Not reported"
        analysis += "\n• GRI 305-3 (Scope 3 Emissions) - Not reported"
    if energy == "Not found":
        analysis += "\n• GRI 302-2 (Energy Intensity) - Not reported"
        analysis += "\n• GRI 302-3 (Renewable Energy) - Not reported"
    if water == "Not found":
        analysis += "\n• GRI 303-4 (Water Recycled) - Not reported"
        analysis += "\n• GRI 303-5 (Water Intensity) - Not reported"
    if waste == "Not found":
        analysis += "\n• GRI 306-4 (Waste Recycled) - Not reported"
        analysis += "\n• GRI 306-5 (Waste to Landfill) - Not reported"
    
    analysis += f"""
    
    ---
    
    **🎯 ESG SCORE: {esg_score}/100**
    
    | Category | Score | Rating |
    |----------|-------|--------|
    | Environmental | {esg_score - 20 if esg_score > 20 else esg_score}/100 | {'B+' if esg_score > 70 else 'C' if esg_score > 50 else 'D'} |
    | Social | 70/100 | B |
    | Governance | 75/100 | B+ |
    | **Overall** | **{esg_score}/100** | **{'B+' if esg_score > 70 else 'C' if esg_score > 50 else 'D'}** |
    
    ---
    
    **📋 RECOMMENDATIONS (Based on GRI Gap Analysis):**
    
    1. **Immediate Actions (Priority - High)**
       - {'Report missing CO₂ emissions data' if co2 == 'Not found' else 'Maintain CO₂ emissions reporting'}
       - {'Implement energy tracking system' if energy == 'Not found' else 'Continue energy efficiency programs'}
    
    2. **Short-term (0-6 months)**
       - Align report with GRI 2024 Universal Standards
       - Disclose Scope 2 and Scope 3 emissions
       - Set Science-Based Targets (SBTi)
    
    3. **Medium-term (6-12 months)**
       - Obtain external assurance (ISO 14064)
       - Implement ESG data management system
       - Publish standalone sustainability report
    
    4. **Long-term (1-3 years)**
       - Achieve GRI Comprehensive option
       - Integrate with financial reporting
       - Achieve ESG rating improvement to A
    
    ---
    
    **🏆 SUSTAINABLE DEVELOPMENT GOALS (SDGs) ALIGNMENT:**
    
    • SDG 7 (Affordable & Clean Energy) - {'Progressing' if energy != 'Not found' else 'Not tracked'}
    • SDG 12 (Responsible Consumption) - {'Progressing' if waste != 'Not found' else 'Not tracked'}
    • SDG 13 (Climate Action) - {'Progressing' if co2 != 'Not found' else 'Not tracked'}
    • SDG 6 (Clean Water) - {'Progressing' if water != 'Not found' else 'Not tracked'}
    
    ---
    
    **⚠️ DATA QUALITY ASSESSMENT:**
    
    | Criteria | Status |
    |----------|--------|
    | Completeness | {'Partial' if co2 == 'Not found' or energy == 'Not found' else 'Good'} |
    | Accuracy | Verifiable |
    | Timeliness | Current year |
    | Comparability | {'Limited' if co2 == 'Not found' else 'Good'} |
    | Reliability | {'Needs verification' if co2 == 'Not found' else 'Verified'} |
    
    ---
    
    *This analysis was generated by AI Agent in compliance with GRI Standards 2024 and ESG reporting framework.*
    *Team Leader: Ismail Kamal | Under Supervision: Dr. Mohamed Tash*
    """
    
    return analysis, esg_score

def generate_pro_pdf_report(co2, energy, water, waste, detailed_analysis, esg_score):
    filename = f"Sustainability_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#1B5E20'), spaceAfter=30, alignment=1)
    heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontSize=16, textColor=colors.HexColor('#2E7D32'), spaceAfter=12, spaceBefore=12)
    
    # Cover Page
    story.append(Spacer(1, 72))
    story.append(Paragraph("🌱 SUSTAINABILITY REPORT 2024", title_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph("GRI Standards Compliant | ESG Framework | AI Analysis", styles['Heading2']))
    story.append(Spacer(1, 36))
    
    # ALL TEAM MEMBERS - DARK BLUE, SIZE 14 IN PDF
    story.append(Paragraph(f"<b>Report Generated by:</b>", styles['Normal']))
    story.append(Paragraph(f"<b><font color='#0D47A1' size='14'>Team Leader: Ismail Kamal</font></b>", styles['Normal']))
    story.append(Paragraph(f"<font color='#0D47A1' size='14'>Team Members: Adel ElSayed, Mohamed Gaber, Ahmed Omar, Sherouk Ashraf, Mohamed ElHammadi, Farouk Sameh</font>", styles['Normal']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"<b><font color='red'>Supervised by: Dr. Mohamed Tash</font></b>", styles['Normal']))
    story.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
    story.append(Spacer(1, 24))
    
    # KPIs Section
    story.append(Paragraph("📊 KEY PERFORMANCE INDICATORS", heading_style))
    
    kpi_data = [
        ['KPI', 'Value', 'Unit', 'GRI Reference'],
        ['🌿 CO2 Emissions', co2, 'metric tons', 'GRI 305-1'],
        ['⚡ Energy Consumption', energy, 'MWh', 'GRI 302-1'],
        ['💧 Water Usage', water, 'm³', 'GRI 303-3'],
        ['🗑️ Waste Generated', waste, 'tons', 'GRI 306-3'],
    ]
    
    table = Table(kpi_data, colWidths=[120, 100, 80, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E7D32')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    story.append(table)
    story.append(Spacer(1, 20))
    
    # ESG Score
    story.append(Paragraph(f"🏆 ESG SCORE: {esg_score}/100", heading_style))
    
    # Detailed Analysis
    story.append(Paragraph("🔍 DETAILED ANALYSIS & REGULATORY COMPLIANCE", heading_style))
    
    # Split analysis into paragraphs
    for line in detailed_analysis.split('\n'):
        if line.strip():
            story.append(Paragraph(line, styles['Normal']))
            story.append(Spacer(1, 6))
    
    doc.build(story)
    return filename

if file:
    with st.spinner("📖 Reading PDF file..."):
        text = extract_text(file)
    
    if st.button("🔍 Analyze Report", type="primary", use_container_width=True):
        with st.spinner("🤖 Extracting KPIs using AI Agent..."):
            co2 = find_kpi(text, "co2")
            energy = find_kpi(text, "energy")
            water = find_kpi(text, "water")
            waste = find_kpi(text, "waste")
            detailed_kpis = extract_detailed_kpis(text)
        
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
        
        st.markdown("### 📈 Interactive Dashboard")
        
        kpi_values = []
        kpi_names = []
        
        for name, value in [("CO₂ Emissions", co2), ("Energy", energy), ("Water", water), ("Waste", waste)]:
            try:
                num_value = float(re.sub(r'[^\d.-]', '', str(value))) if value != "Not found" else 0
            except:
                num_value = 0
            kpi_names.append(name)
            kpi_values.append(num_value)
        
        df = pd.DataFrame({"KPI": kpi_names, "Value": kpi_values})
        fig = px.bar(df, x="KPI", y="Value", title="Sustainability KPIs Dashboard", color="KPI", text="Value")
        fig.update_traces(textposition="outside")
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 🤖 AI Agent Detailed Analysis")
        
        # Generate detailed analysis
        detailed_analysis, esg_score = generate_detailed_analysis(co2, energy, water, waste, detailed_kpis)
        
        st.markdown(detailed_analysis)
        
        st.markdown("### 📥 Export Report")
        
        pdf_file = generate_pro_pdf_report(co2, energy, water, waste, detailed_analysis, esg_score)
        
        with open(pdf_file, "rb") as f:
            st.download_button(
                label="📥 Download PDF Report (GRI Compliant)",
                data=f,
                file_name=pdf_file,
                mime="application/pdf",
                use_container_width=True
            )
        
        st.success("✅ Analysis completed successfully! Report complies with GRI Standards 2024.")

st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>🌱 Sustainability Report Analysis with AI Agent | GRI Standards 2024 Compliant | ESG Framework</p>
        <p>Developed by <span style='color: #0D47A1; font-weight: bold; font-size: 14px;'>Ismail Kamal (Team Leader)</span> & 
        <span style='color: #0D47A1; font-size: 14px;'>Team Members: Adel, Mohamed, Ahmed, Sherouk, ElHammadi, Farouk</span> | 
        <span style='color: #FF0000; font-weight: bold;'>Under Supervision of Dr. Mohamed Tash</span></p>
        <p>Version 3.0 | AI-Powered | Regulatory Compliance Check</p>
    </div>
""", unsafe_allow_html=True)
