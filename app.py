import streamlit as st
from dotenv import load_dotenv
from economic_calculator import calculate_economic_impact
import plotly.graph_objects as go
import plotly.express as px

load_dotenv()

st.set_page_config(
    page_title="Economic Impact Analysis Tool",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    
    h1 {
        color: #1f4788;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    h2, h3 {
        color: #1f4788;
    }
    
    .subtitle {
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    .welcome-message {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #1f4788;
        margin: 2rem 0;
        font-size: 1.1rem;
    }
    
    .stButton>button {
        background-color: #1f4788;
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #163761;
        box-shadow: 0 4px 8px rgba(31, 71, 136, 0.3);
    }
    
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select {
        border: 2px solid #e0e0e0;
        border-radius: 6px;
        padding: 0.5rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus {
        border-color: #1f4788;
        box-shadow: 0 0 0 2px rgba(31, 71, 136, 0.1);
    }
    
    .accent-red {
        color: #c41e3a;
        font-weight: 600;
    }
    
    hr {
        margin: 2rem 0;
        border: none;
        border-top: 2px solid #e0e0e0;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Economic Impact Analysis Tool")

st.markdown('<p class="subtitle">Street Economics - Homestead CRA Edition</p>', unsafe_allow_html=True)

st.markdown(
    '<div class="welcome-message">Complete the form below to generate your economic impact report</div>',
    unsafe_allow_html=True
)

if 'form_data' not in st.session_state:
    st.session_state['form_data'] = {}
if 'report_generated' not in st.session_state:
    st.session_state['report_generated'] = False

st.markdown("---")

with st.form("economic_impact_form"):
    
    with st.expander("📋 Project Description", expanded=True):
        st.write("Fields coming soon")
    
    with st.expander("🏢 Project Type & Use", expanded=True):
        st.write("Fields coming soon")
    
    with st.expander("💰 Project Costs", expanded=True):
        st.write("Fields coming soon")
    
    with st.expander("👥 Operations", expanded=True):
        st.write("Fields coming soon")
    
    with st.expander("💵 Funding Request", expanded=True):
        st.write("Fields coming soon")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    submitted = st.form_submit_button("Generate Report", use_container_width=True)
    
    if submitted:
        st.session_state['report_generated'] = True
        st.success("✅ Report generation initiated!")

if st.session_state.get('report_generated', False):
    st.info("Report results will be displayed here once form fields are implemented.")
