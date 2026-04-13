import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PyPDF2 import PdfReader
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="Sustainability Report Analyzer Pro",
    page_icon="🌱",
    layout="wide"
)

# -----------------------
# CUSTOM CSS
# -----------------------
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 25px;
        text-align: center;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 32px;
    }
    .main-header p {
        color: #E8F5E9;
        margin: 10px 0 0 0;
    }
    .topic-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 5px solid;
    }
    .topic-number {
        font-size: 24px;
        font-weight: bold;
        color: #2E7D32;
    }
    .kpi-highlight {
        background: #E8F5E9;
        padding: 8px;
        border-radius: 8px;
        font-family: monospace;
    }
    .risk-high {
        color: #D32F2F;
        font-weight: bold;
    }
    .risk-medium {
        color: #F57C00;
        font-weight: bold;
    }
    .risk-low {
        color: #388E3C;
        font-weight: bold;
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
            <h1>🌱 Sustainability Report Analysis with AI Agent</h1>
            <p>GRI Standards | ESG Integration | AI-Powered Insights</p>
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
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="background-color: #E8F5E9;">
                    <th style="padding: 8px; text-align: left; font-size: 14px;">Role</th>
                    <th style="padding: 8px; text-align: left; font-size: 14px;">Name</th>
                </tr>
                <tr><td style="padding: 8px; font-size: 14px;"><b>Team Leader</b></td>
                    <td style="padding: 8px; color: #00008B; font-weight: bold; font-size: 14px;">Ismail Kamal</td>
                </tr>
                <tr><td style="padding: 8px; font-size: 14px;">Team Member</td>
                    <td style="padding: 8px; color: #00008B; font-size: 14px;">Adel ElSayed</td>
                </tr>
                <tr><td style="padding: 8px; font-size: 14px;">Team Member</td>
                    <td style="padding: 8px; color: #00008B; font-size: 14px;">Mohamed Gaber</td>
                </tr>
                <tr><td style="padding: 8px; font-size: 14px;">Team Member</td>
                    <td style="padding: 8px; color: #00008B; font-size: 14px;">Ahmed Omar</td>
                </tr>
                <tr><td style="padding: 8px; font-size: 14px;">Team Member</td>
                    <td style="padding: 8px; color: #00008B; font-size: 14px;">Sherouk Ashraf</td>
                </tr>
                <tr><td style="padding: 8px; font-size: 14px;">Team Member</td>
                    <td style="padding: 8px; color: #00008B; font-size: 14px;">Mohamed ElHammadi</td>
                </tr>
                <tr><td style="padding: 8px; font-size: 14px;">Team Member</td>
                    <td style="padding: 8px; color: #00008B; font-size: 14px;">Farouk Sameh</td>
                </tr>
            </table>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%); 
                        padding: 25px; border-radius: 15px; text-align: center; 
                        border: 3px solid #FF0000; box-shadow: 0 4px 15px rgba(255,0,0,0.2);'>
                <h3 style='color: #2E7D32; margin: 0;'>🎓 Under Supervision of</h3>
                <h1 style='color: #FF0000; font-weight: bold; font-size: 34px; margin: 10px 0; 
                           text-shadow: 2px 2px 4px rgba(0,0,0,0.1);'>
                    Dr. Mohamed Tash
                </h1>
                <p style='font-size: 16px; color: #333; font-weight: bold;'>Professor of Sustainability & ESG</p>
                <p style='font-size: 14px; color: #666;'>PhD in Environmental Engineering | GRI Certified</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("© 2025 Sustainability Report Analysis System | GRI Standards Compliant")
    st.stop()

# -----------------------
# MAIN APP HEADER
# -----------------------
st.markdown("""
    <div class='main-header'>
        <h1>🌱 Sustainability Report Analysis with AI Agent</h1>
        <p style='color: #E8F5E9; text-align: center; margin: 10px 0 0 0;'>
            <span style='color: #00008B; font-weight: bold; font-size: 14px;'>Team Leader: Ismail Kamal</span> | 
            <span style='color: #00008B; font-size: 14px;'>Adel ElSayed, Mohamed Gaber, Ahmed Omar, Sherouk Ashraf, Mohamed ElHammadi, Farouk Sameh</span> | 
            <span style='color: #FF0000; font-weight: bold;'>Under Supervision: Dr. Mohamed Tash</span>
        </p>
    </div>
""", unsafe_allow_html=True)

# -----------------------
# SIDEBAR
# -----------------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/sustainability.png", width=80)
    st.markdown("## 🌿 Sustainability AI Agent")
    st.markdown("---")
    
    # Comparison Mode Toggle
    comparison_mode = st.checkbox("📊 Enable Company Comparison Mode", value=st.session_state.comparison_mode)
    st.session_state.comparison_mode = comparison_mode
    
    if st.session_state.comparison_mode:
        st.markdown("### 🏢 Companies to Compare")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Add Company"):
                st.session_state.company_reports.append(None)
        with col2:
            if st.button("🗑️ Clear All") and st.session_state.company_reports:
                st.session_state.company_reports = []
        
        for i in range(len(st.session_state.company_reports)):
            st.file_uploader(f"Company {i+1} Report", type="pdf", key=f"company_{i}")
    
    st.markdown("---")
    st.markdown("### 👥 Team Members")
    st.markdown("""
    <div style='color: #00008B; font-size: 14px;'>
        <b style='color: #00008B;'>• Ismail Kamal</b> (Leader)<br>
        <span style='color: #00008B;'>• Adel ElSayed</span><br>
        <span style='color: #00008B;'>• Mohamed Gaber</span><br>
        <span style='color: #00008B;'>• Ahmed Omar</span><br>
        <span style='color: #00008B;'>• Sherouk Ashraf</span><br>
        <span style='color: #00008B;'>• Mohamed ElHammadi</span><br>
        <span style='color: #00008B;'>• Farouk Sameh</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 🎓 Supervisor")
    st.markdown("<span style='color: #FF0000; font-weight: bold; font-size: 16px;'>Dr. Mohamed Tash</span>", unsafe_allow_html=True)
    st.markdown("---")
    st.caption("Version 4.0 | Top 10 Sustainability Topics")

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

def extract_company_info(text):
    """استخراج معلومات عامة عن الشركة"""
    activity_types = {
        "Petrochemical": ["petrochemical", "chemical", "polymer"],
        "Oil & Gas": ["oil", "gas", "petroleum", "refinery"],
        "Manufacturing": ["manufacturing", "factory", "industrial"],
        "Waste Management": ["waste", "recycling", "landfill"]
    }
    
    company_type = "Not specified"
    for act_type, keywords in activity_types.items():
        for kw in keywords:
            if kw.lower() in text.lower():
                company_type = act_type
                break
    
    # Company size detection
    size = "Local"
    if "global" in text.lower() or "international" in text.lower():
        size = "Global"
    elif "regional" in text.lower():
        size = "Regional"
    
    # Number of sites
    sites_match = re.search(r"(\d+)\s*(?:sites|facilities|locations|plants)", text, re.IGNORECASE)
    num_sites = sites_match.group(1) if sites_match else "N/A"
    
    return {
        "activity_type": company_type,
        "size": size,
        "num_sites": num_sites
    }

def generate_top10_topics(text, company_info):
    """توليد أهم 10 مواضيع للاستدامة"""
    
    # Extract KPIs
    co2 = find_kpi(text, "co2")
    energy = find_kpi(text, "energy")
    water = find_kpi(text, "water")
    waste = find_kpi(text, "waste")
    renewable = find_kpi(text, "renewable")
    employees = find_kpi(text, "employees")
    safety = find_kpi(text, "safety|ltifr")
    training = find_kpi(text, "training")
    board = find_kpi(text, "board")
    ethics = find_kpi(text, "ethics")
    
    topics = [
        {
            "number": 1,
            "topic": "🏭 Company Overview",
            "kpi": f"Type: {company_info['activity_type']} | Size: {company_info['size']} | Sites: {company_info['num_sites']}",
            "risk": "Business continuity, Market reputation",
            "impact": "Economic",
            "color": "#1B5E20"
        },
        {
            "number": 2,
            "topic": "🌿 CO₂ / GHG Emissions",
            "kpi": f"{co2} metric tons CO₂e",
            "risk": "Climate regulations, Carbon tax, Reputation damage" if co2 != "N/A" else "Data gap - unable to assess climate risk",
            "impact": "Environmental / Regulatory",
            "color": "#2E7D32"
        },
        {
            "number": 3,
            "topic": "⚡ Energy Consumption",
            "kpi": f"{energy} MWh",
            "risk": "Energy price volatility, Supply disruption",
            "impact": "Economic / Environmental",
            "color": "#F57C00"
        },
        {
            "number": 4,
            "topic": "💧 Water Stewardship",
            "kpi": f"{water} m³",
            "risk": "Water scarcity, Regulatory compliance, Community relations",
            "impact": "Environmental / Social",
            "color": "#1565C0"
        },
        {
            "number": 5,
            "topic": "🗑️ Waste Management",
            "kpi": f"{waste} tons generated",
            "risk": "Landfill costs, Regulatory fines, Reputation",
            "impact": "Environmental / Economic",
            "color": "#6A1B9A"
        },
        {
            "number": 6,
            "topic": "🛡️ Occupational Health & Safety",
            "kpi": f"LTIFR: {safety if safety != 'N/A' else 'N/A'}",
            "risk": "Workplace accidents, Legal liability, Employee morale",
            "impact": "Social / Legal",
            "color": "#C62828"
        },
        {
            "number": 7,
            "topic": "👥 Workforce & Human Rights",
            "kpi": f"{employees} employees | Training: {training if training != 'N/A' else 'N/A'} hrs",
            "risk": "Labor disputes, Skill shortage, Diversity compliance",
            "impact": "Social / Economic",
            "color": "#4527A0"
        },
        {
            "number": 8,
            "topic": "🏛️ Governance & Ethics",
            "kpi": f"Board Independence: {board if board != 'N/A' else 'N/A'}% | Ethics: {ethics if ethics != 'N/A' else 'N/A'}%",
            "risk": "Corruption, Non-compliance, Shareholder activism",
            "impact": "Governance / Legal",
            "color": "#4A148C"
        },
        {
            "number": 9,
            "topic": "🎯 Renewable Energy & Net Zero",
            "kpi": f"Renewable share: {renewable if renewable != 'N/A' else 'N/A'}%",
            "risk": "Transition risk, Stranded assets, Investor pressure",
            "impact": "Environmental / Economic",
            "color": "#FF8F00"
        },
        {
            "number": 10,
            "topic": "⚠️ Risk & Compliance Summary",
            "kpi": "GRI Standards assessment",
            "risk": "Regulatory non-compliance, Fines, Legal action",
            "impact": "Legal / Financial / Reputational",
            "color": "#D32F2F"
        }
    ]
    
    return topics

def display_top10_topics(topics):
    """عرض أهم 10 مواضيع بشكل منظم"""
    
    st.markdown("## 🏆 Top 10 Sustainability Topics")
    st.markdown("---")
    
    for topic in topics:
        color = topic["color"]
        
        # Risk level styling
        risk_text = topic["risk"]
        if "high" in risk_text.lower() or "severe" in risk_text.lower():
            risk_style = "risk-high"
        elif "medium" in risk_text.lower():
            risk_style = "risk-medium"
        else:
            risk_style = "risk-low"
        
        st.markdown(f"""
            <div class='topic-card' style='border-left-color: {color};'>
                <table style="width: 100%;">
                    <tr>
                        <td style="width: 60px; vertical-align: top;">
                            <span class='topic-number' style='color: {color};'>#{topic['number']}</span>
                        </td>
                        <td style="vertical-align: top;">
                            <h3 style='color: {color}; margin: 0 0 10px 0;'>{topic['topic']}</h3>
                            <div class='kpi-highlight' style='background: {color}20;'>
                                <b>📊 KPI:</b> {topic['kpi']}
                            </div>
                            <div style='margin-top: 8px;'>
                                <b>⚠️ Risk:</b> <span class='{risk_style}'>{topic['risk']}</span>
                            </div>
                            <div style='margin-top: 8px;'>
                                <b>🎯 Impact:</b> {topic['impact']}
                            </div>
                        </td>
                    </tr>
                </table>
            </div>
        """, unsafe_allow_html=True)

def create_risk_matrix(topics):
    """إنشاء مصفوفة المخاطر"""
    risks = []
    impacts = []
    
    for topic in topics:
        risks.append(topic['topic'].split()[1] if len(topic['topic'].split()) > 1 else topic['topic'])
        if "Environmental" in topic['impact']:
            impacts.append(3)
        elif "Social" in topic['impact']:
            impacts.append(2)
        else:
            impacts.append(1)
    
    fig = go.Figure(data=[go.Bar(x=risks[:5], y=impacts[:5], marker_color=['#2E7D32', '#F57C00', '#1565C0', '#6A1B9A', '#C62828'])])
    fig.update_layout(title="Top 5 Risks by Impact Level", xaxis_title="Risk Category", yaxis_title="Impact Score (1-3)", height=400)
    return fig

def generate_pdf_report(topics, company_info):
    """توليد تقرير PDF"""
    filename = f"Sustainability_Top10_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, 
                                  textColor=colors.HexColor('#1B5E20'), spaceAfter=30, alignment=1)
    
    # Cover
    story.append(Paragraph("🌱 TOP 10 SUSTAINABILITY TOPICS", title_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph("GRI Standards Compliant | ESG Analysis", styles['Heading2']))
    story.append(Spacer(1, 36))
    story.append(Paragraph("<b>Prepared by:</b> Ismail Kamal & Team", styles['Normal']))
    story.append(Paragraph("<b><font color='red'>Supervised by: Dr. Mohamed Tash</font></b>", styles['Normal']))
    story.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
    story.append(Spacer(1, 24))
    
    # Company Info
    story.append(Paragraph("🏭 COMPANY INFORMATION", styles['Heading2']))
    story.append(Paragraph(f"Activity Type: {company_info['activity_type']}", styles['Normal']))
    story.append(Paragraph(f"Company Size: {company_info['size']}", styles['Normal']))
    story.append(Paragraph(f"Number of Sites: {company_info['num_sites']}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Top 10 Topics Table
    story.append(Paragraph("📊 TOP 10 SUSTAINABILITY TOPICS", styles['Heading2']))
    
    table_data = [['#', 'Topic', 'KPI', 'Risk', 'Impact']]
    for topic in topics:
        table_data.append([
            str(topic['number']),
            topic['topic'],
            topic['kpi'][:50] + "..." if len(topic['kpi']) > 50 else topic['kpi'],
            topic['risk'][:50] + "..." if len(topic['risk']) > 50 else topic['risk'],
            topic['impact']
        ])
    
    table = Table(table_data, colWidths=[30, 100, 120, 120, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E7D32')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))
    story.append(table)
    
    doc.build(story)
    return filename

# -----------------------
# MAIN UPLOAD & ANALYSIS
# -----------------------
if not st.session_state.comparison_mode:
    file = st.file_uploader("📄 Upload Sustainability Report (PDF)", type="pdf")
    
    if file:
        with st.spinner("📖 Reading PDF..."):
            text = extract_text(file)
            company_info = extract_company_info(text)
        
        if st.button("🔍 Analyze Report", type="primary", use_container_width=True):
            with st.spinner("🤖 Generating Top 10 Sustainability Topics..."):
                topics = generate_top10_topics(text, company_info)
            
            # Display Company Info
            st.markdown("## 🏭 Company Overview")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Activity Type", company_info['activity_type'])
            with col2:
                st.metric("Company Size", company_info['size'])
            with col3:
                st.metric("Number of Sites", company_info['num_sites'])
            
            st.markdown("---")
            
            # Display Top 10 Topics
            display_top10_topics(topics)
            
            # Risk Matrix
            st.markdown("---")
            st.markdown("## 📊 Risk Matrix")
            st.plotly_chart(create_risk_matrix(topics), use_container_width=True)
            
            # Summary Stats
            st.markdown("---")
            st.markdown("## 📈 Summary Statistics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            # Count risks by impact type
            env_risks = sum(1 for t in topics if "Environmental" in t['impact'])
            social_risks = sum(1 for t in topics if "Social" in t['impact'])
            econ_risks = sum(1 for t in topics if "Economic" in t['impact'])
            
            with col1:
                st.metric("🌿 Environmental Risks", env_risks)
            with col2:
                st.metric("👥 Social Risks", social_risks)
            with col3:
                st.metric("💰 Economic Risks", econ_risks)
            with col4:
                st.metric("📋 Total Topics", len(topics))
            
            # PDF Download
            st.markdown("---")
            st.markdown("## 📥 Export Report")
            
            pdf_file = generate_pdf_report(topics, company_info)
            with open(pdf_file, "rb") as f:
                st.download_button(
                    label="📥 Download Top 10 Report (PDF)",
                    data=f,
                    file_name=pdf_file,
                    mime="application/pdf",
                    use_container_width=True
                )
            
            st.success("✅ Analysis completed successfully! Top 10 Sustainability Topics identified.")

else:
    # Comparison Mode
    st.markdown("## 🏢 Multi-Company Comparison Mode")
    st.info("📌 Upload reports for multiple companies to compare Top 10 Sustainability Topics")
    
    companies_data = []
    for i in range(len(st.session_state.company_reports)):
        company_file = st.session_state.get(f"company_{i}")
        if company_file:
            with st.spinner(f"Analyzing Company {i+1}..."):
                text = extract_text(company_file)
                company_info = extract_company_info(text)
                topics = generate_top10_topics(text, company_info)
                
                companies_data.append({
                    "Company": f"Company {i+1}",
                    "Type": company_info['activity_type'],
                    "Size": company_info['size'],
                    "CO2": find_kpi(text, "co2"),
                    "Energy": find_kpi(text, "energy"),
                    "Water": find_kpi(text, "water")
                })
    
    if companies_data and st.button("📊 Compare Companies", type="primary"):
        df_comparison = pd.DataFrame(companies_data)
        
        st.subheader("📊 Companies Overview")
        st.dataframe(df_comparison, use_container_width=True)
        
        st.subheader("📈 KPI Comparison")
        fig_kpi = px.bar(df_comparison, x="Company", y=["CO2", "Energy", "Water"],
                         title="Sustainability KPIs Comparison", barmode="group")
        st.plotly_chart(fig_kpi, use_container_width=True)
        
        st.success("✅ Comparison complete!")

# -----------------------
# FOOTER
# -----------------------
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>🌱 Sustainability Report Analysis with AI Agent | Top 10 Sustainability Topics | GRI Standards Compliant</p>
        <p>Developed by <span style='color: #00008B; font-weight: bold;'>Ismail Kamal</span> & Team | 
        <span style='color: #FF0000; font-weight: bold;'>Under Supervision of Dr. Mohamed Tash</span></p>
        <p>Version 4.0 | Top 10 Topics | Risk Matrix | ESG Analytics</p>
    </div>
""", unsafe_allow_html=True)
