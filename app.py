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
# PROFESSIONAL CUSTOM CSS
# -----------------------
st.markdown("""
    <style>
    /* Main Header - Professional Sustainability Design */
    .main-header {
        background: linear-gradient(135deg, #0D47A1 0%, #1B5E20 100%);
        padding: 35px 25px;
        border-radius: 20px;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    }
    .main-header::before {
        content: "🌿";
        position: absolute;
        font-size: 120px;
        opacity: 0.1;
        bottom: -20px;
        right: -20px;
        transform: rotate(-15deg);
    }
    .main-header::after {
        content: "🌍";
        position: absolute;
        font-size: 100px;
        opacity: 0.1;
        top: -30px;
        left: -20px;
        transform: rotate(15deg);
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 36px;
        font-weight: 700;
        letter-spacing: -0.5px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    .main-header p {
        color: #E8F5E9;
        margin: 15px 0 0 0;
        font-size: 16px;
        opacity: 0.95;
    }
    .main-header .team-line {
        margin-top: 20px;
        padding-top: 15px;
        border-top: 1px solid rgba(255,255,255,0.2);
    }
    
    /* Topic Cards - Professional Design */
    .topic-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 20px;
        border-radius: 16px;
        margin-bottom: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 6px solid;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .topic-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    .topic-number {
        font-size: 28px;
        font-weight: 800;
        display: inline-block;
        width: 50px;
        height: 50px;
        line-height: 50px;
        text-align: center;
        border-radius: 12px;
        margin-right: 15px;
    }
    .kpi-highlight {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        padding: 10px 15px;
        border-radius: 12px;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        margin: 10px 0;
    }
    .risk-high {
        color: #D32F2F;
        font-weight: bold;
        background: #FFEBEE;
        padding: 3px 8px;
        border-radius: 20px;
        display: inline-block;
    }
    .risk-medium {
        color: #F57C00;
        font-weight: bold;
        background: #FFF3E0;
        padding: 3px 8px;
        border-radius: 20px;
        display: inline-block;
    }
    .risk-low {
        color: #388E3C;
        font-weight: bold;
        background: #E8F5E9;
        padding: 3px 8px;
        border-radius: 20px;
        display: inline-block;
    }
    
    /* Stat Cards */
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
    .stat-card p {
        margin: 8px 0 0 0;
        opacity: 0.9;
        font-size: 14px;
    }
    
    /* Sidebar styling */
    .css-1d391kg, .css-12oz5g7 {
        background: linear-gradient(180deg, #0A2E0F 0%, #1B5E20 100%);
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
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
            <div class='team-line'>
                <p style='font-weight: bold;'>Team Leader: Ismail Kamal | Under Supervision: Dr. Mohamed Tash</p>
                <p style='font-size: 12px; opacity: 0.8;'>QHSE Master at Alexandria University</p>
            </div>
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
                    <th style="padding: 8px; text-align: left;">Role</th>
                    <th style="padding: 8px; text-align: left;">Name</th>
                </tr>
                <tr><td style="padding: 8px;"><b>Team Leader</b></td>
                    <td style="padding: 8px; color: #00008B; font-weight: bold;">Ismail Kamal</td></tr>
                <tr><td style="padding: 8px;">Team Member</td>
                    <td style="padding: 8px; color: #00008B;">Adel ElSayed</td></tr>
                <tr><td style="padding: 8px;">Team Member</td>
                    <td style="padding: 8px; color: #00008B;">Mohamed Gaber</td></tr>
                <tr><td style="padding: 8px;">Team Member</td>
                    <td style="padding: 8px; color: #00008B;">Ahmed Omar</td></tr>
                <tr><td style="padding: 8px;">Team Member</td>
                    <td style="padding: 8px; color: #00008B;">Sherouk Ashraf</td></tr>
                <tr><td style="padding: 8px;">Team Member</td>
                    <td style="padding: 8px; color: #00008B;">Mohamed ElHammadi</td></tr>
                <tr><td style="padding: 8px;">Team Member</td>
                    <td style="padding: 8px; color: #00008B;">Farouk Sameh</td></tr>
            </table>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #0D47A1 0%, #1B5E20 100%); 
                        padding: 30px; border-radius: 20px; text-align: center; 
                        box-shadow: 0 10px 30px rgba(0,0,0,0.2);'>
                <h3 style='color: #FFD54F; margin: 0;'>🎓 Under Supervision of</h3>
                <h1 style='color: #FF0000; font-weight: bold; font-size: 32px; margin: 15px 0; 
                           text-shadow: 2px 2px 4px rgba(0,0,0,0.2);'>
                    Dr. Mohamed Tash
                </h1>
                <p style='font-size: 18px; color: white; font-weight: bold;'>QHSE Master at Alexandria University</p>
                <p style='font-size: 14px; color: #E8F5E9;'>Professor of Sustainability & ESG</p>
                <p style='font-size: 12px; color: #FFD54F; margin-top: 15px;'>⭐ Lead Supervisor | ESG Expert ⭐</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("© 2025 Sustainability Report Analysis System | GRI Standards Compliant")
    st.stop()

# -----------------------
# MAIN APP HEADER - PROFESSIONAL DESIGN
# -----------------------
st.markdown("""
    <div class='main-header'>
        <h1>🌱 Sustainability Report Analysis</h1>
        <p>with AI Agent | GRI Standards 2024 | ESG Framework</p>
        <div class='team-line'>
            <p style='font-weight: bold; color: white; font-size: 16px;'>
                Team Leader: Ismail Kamal | Under Supervision: Dr. Mohamed Tash
            </p>
            <p style='font-size: 13px; color: #FFD54F; margin-top: 8px;'>
                QHSE Master at Alexandria University
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)

# -----------------------
# SIDEBAR - PROFESSIONAL DESIGN
# -----------------------
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 10px;'>
            <div style='font-size: 60px;'>🌿</div>
            <h3 style='color: white; margin: 10px 0;'>Sustainability AI Agent</h3>
        </div>
    """, unsafe_allow_html=True)
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
    <div style='color: #E8F5E9; font-size: 13px;'>
        <b style='color: #FFD54F;'>• Ismail Kamal</b> (Leader)<br>
        <span>• Adel ElSayed</span><br>
        <span>• Mohamed Gaber</span><br>
        <span>• Ahmed Omar</span><br>
        <span>• Sherouk Ashraf</span><br>
        <span>• Mohamed ElHammadi</span><br>
        <span>• Farouk Sameh</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 🎓 Supervisor")
    st.markdown("""
    <div style='text-align: center;'>
        <span style='color: #FF0000; font-weight: bold; font-size: 18px;'>Dr. Mohamed Tash</span><br>
        <span style='color: #FFD54F; font-size: 12px;'>QHSE Master at Alexandria University</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.caption("Version 4.0 | Top 10 Topics | Professional Edition")

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
    """Extract general company information"""
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
    
    size = "Local"
    if "global" in text.lower() or "international" in text.lower():
        size = "Global"
    elif "regional" in text.lower():
        size = "Regional"
    
    sites_match = re.search(r"(\d+)\s*(?:sites|facilities|locations|plants)", text, re.IGNORECASE)
    num_sites = sites_match.group(1) if sites_match else "N/A"
    
    return {
        "activity_type": company_type,
        "size": size,
        "num_sites": num_sites
    }

def generate_top10_topics(text, company_info):
    """Generate Top 10 Sustainability Topics"""
    
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
            "risk": "Climate regulations, Carbon tax, Reputation damage",
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
            "risk": "Water scarcity, Regulatory compliance",
            "impact": "Environmental / Social",
            "color": "#1565C0"
        },
        {
            "number": 5,
            "topic": "🗑️ Waste Management",
            "kpi": f"{waste} tons generated",
            "risk": "Landfill costs, Regulatory fines",
            "impact": "Environmental / Economic",
            "color": "#6A1B9A"
        },
        {
            "number": 6,
            "topic": "🛡️ Occupational Health & Safety",
            "kpi": f"LTIFR: {safety if safety != 'N/A' else 'N/A'}",
            "risk": "Workplace accidents, Legal liability",
            "impact": "Social / Legal",
            "color": "#C62828"
        },
        {
            "number": 7,
            "topic": "👥 Workforce & Human Rights",
            "kpi": f"{employees} employees | Training: {training if training != 'N/A' else 'N/A'} hrs",
            "risk": "Labor disputes, Skill shortage",
            "impact": "Social / Economic",
            "color": "#4527A0"
        },
        {
            "number": 8,
            "topic": "🏛️ Governance & Ethics",
            "kpi": f"Board Independence: {board if board != 'N/A' else 'N/A'}%",
            "risk": "Corruption, Non-compliance",
            "impact": "Governance / Legal",
            "color": "#4A148C"
        },
        {
            "number": 9,
            "topic": "🎯 Renewable Energy & Net Zero",
            "kpi": f"Renewable share: {renewable if renewable != 'N/A' else 'N/A'}%",
            "risk": "Transition risk, Investor pressure",
            "impact": "Environmental / Economic",
            "color": "#FF8F00"
        },
        {
            "number": 10,
            "topic": "⚠️ Risk & Compliance Summary",
            "kpi": "GRI Standards assessment",
            "risk": "Regulatory non-compliance",
            "impact": "Legal / Financial",
            "color": "#D32F2F"
        }
    ]
    
    return topics

def display_top10_topics(topics):
    """Display Top 10 Topics in professional format"""
    
    st.markdown("## 🏆 Top 10 Sustainability Topics")
    st.markdown("---")
    
    for topic in topics:
        color = topic["color"]
        
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
                        <td style="width: 70px; vertical-align: top;">
                            <div class='topic-number' style='background: {color}20; color: {color};'>#{topic['number']}</div>
                        </td>
                        <td style="vertical-align: top;">
                            <h3 style='color: {color}; margin: 0 0 10px 0;'>{topic['topic']}</h3>
                            <div class='kpi-highlight'>
                                <b>📊 KPI:</b> {topic['kpi']}
                            </div>
                            <div style='margin-top: 12px;'>
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
    """Create risk matrix chart"""
    risk_names = []
    impact_scores = []
    
    for topic in topics[:8]:
        name = topic['topic'].split()[1] if len(topic['topic'].split()) > 1 else topic['topic']
        risk_names.append(name)
        if "Environmental" in topic['impact']:
            impact_scores.append(3)
        elif "Social" in topic['impact']:
            impact_scores.append(2)
        elif "Legal" in topic['impact']:
            impact_scores.append(3)
        else:
            impact_scores.append(1)
    
    colors_risk = ['#2E7D32', '#F57C00', '#1565C0', '#6A1B9A', '#C62828', '#4527A0', '#FF8F00', '#D32F2F']
    
    fig = go.Figure(data=[go.Bar(x=risk_names, y=impact_scores, 
                                  marker_color=colors_risk[:len(risk_names)],
                                  text=impact_scores, textposition='outside')])
    fig.update_layout(title="Top Risks by Impact Level",
                      xaxis_title="Risk Category",
                      yaxis_title="Impact Score (1-3)",
                      height=450,
                      plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)')
    fig.update_xaxes(tickangle=45)
    return fig

def generate_pdf_report(topics, company_info):
    """Generate professional PDF report"""
    filename = f"Sustainability_Top10_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=26, 
                                  textColor=colors.HexColor('#1B5E20'), spaceAfter=30, alignment=1)
    
    story.append(Paragraph("🌱 TOP 10 SUSTAINABILITY TOPICS", title_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph("GRI Standards Compliant | ESG Analysis | AI-Powered", styles['Heading2']))
    story.append(Spacer(1, 36))
    story.append(Paragraph("<b>Team Leader:</b> Ismail Kamal", styles['Normal']))
    story.append(Paragraph("<b><font color='red'>Under Supervision: Dr. Mohamed Tash</font></b>", styles['Normal']))
    story.append(Paragraph("<b>QHSE Master at Alexandria University</b>", styles['Normal']))
    story.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
    story.append(Spacer(1, 24))
    
    story.append(Paragraph("🏭 COMPANY INFORMATION", styles['Heading2']))
    story.append(Paragraph(f"Activity Type: {company_info['activity_type']}", styles['Normal']))
    story.append(Paragraph(f"Company Size: {company_info['size']}", styles['Normal']))
    story.append(Paragraph(f"Number of Sites: {company_info['num_sites']}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("📊 TOP 10 SUSTAINABILITY TOPICS", styles['Heading2']))
    
    table_data = [['#', 'Topic', 'KPI', 'Risk', 'Impact']]
    for topic in topics:
        table_data.append([
            str(topic['number']),
            topic['topic'],
            topic['kpi'][:45] + "..." if len(topic['kpi']) > 45 else topic['kpi'],
            topic['risk'][:45] + "..." if len(topic['risk']) > 45 else topic['risk'],
            topic['impact']
        ])
    
    table = Table(table_data, colWidths=[30, 100, 110, 120, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1B5E20')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
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
            
            # Company Info Cards
            st.markdown("## 🏭 Company Overview")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                    <div class='stat-card'>
                        <h3>{company_info['activity_type']}</h3>
                        <p>Activity Type</p>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                    <div class='stat-card'>
                        <h3>{company_info['size']}</h3>
                        <p>Company Size</p>
                    </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                    <div class='stat-card'>
                        <h3>{company_info['num_sites']}</h3>
                        <p>Number of Sites</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Display Top 10 Topics
            display_top10_topics(topics)
            
            # Risk Matrix
            st.markdown("---")
            st.markdown("## 📊 Risk Matrix")
            st.plotly_chart(create_risk_matrix(topics), use_container_width=True)
            
            # Summary Statistics
            st.markdown("---")
            st.markdown("## 📈 Summary Statistics")
            
            env_risks = sum(1 for t in topics if "Environmental" in t['impact'])
            social_risks = sum(1 for t in topics if "Social" in t['impact'])
            econ_risks = sum(1 for t in topics if "Economic" in t['impact'])
            legal_risks = sum(1 for t in topics if "Legal" in t['impact'])
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                    <div class='stat-card' style='background: linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%);'>
                        <h3>{env_risks}</h3>
                        <p>🌿 Environmental Risks</p>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                    <div class='stat-card' style='background: linear-gradient(135deg, #1565C0 0%, #0D47A1 100%);'>
                        <h3>{social_risks}</h3>
                        <p>👥 Social Risks</p>
                    </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                    <div class='stat-card' style='background: linear-gradient(135deg, #F57C00 0%, #E65100 100%);'>
                        <h3>{econ_risks}</h3>
                        <p>💰 Economic Risks</p>
                    </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                    <div class='stat-card' style='background: linear-gradient(135deg, #C62828 0%, #8B0000 100%);'>
                        <h3>{legal_risks}</h3>
                        <p>⚖️ Legal Risks</p>
                    </div>
                """, unsafe_allow_html=True)
            
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
# PROFESSIONAL FOOTER
# -----------------------
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #0A2E0F 0%, #1B5E20 100%); 
                border-radius: 15px; margin-top: 20px;'>
        <p style='color: white; margin: 0;'>
            🌱 Sustainability Report Analysis with AI Agent | GRI Standards 2024 Compliant
        </p>
        <p style='color: #E8F5E9; font-size: 12px; margin: 10px 0 0 0;'>
            Developed by <strong>Ismail Kamal</strong> & Team | 
            <strong style='color: #FF0000;'>Under Supervision of Dr. Mohamed Tash</strong> | 
            QHSE Master at Alexandria University
        </p>
        <p style='color: #FFD54F; font-size: 11px; margin: 8px 0 0 0;'>
            Version 4.0 | Top 10 Topics | Risk Matrix | Professional Edition
        </p>
    </div>
""", unsafe_allow_html=True)
