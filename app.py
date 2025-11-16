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
    
    label:has(+ div input[required]),
    label:has(+ div textarea[required]) {
        background-color: #f8f9fa;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
    }
    
    div[data-testid="stTextInput"] label:contains("*"),
    div[data-testid="stTextArea"] label:contains("*"),
    div[data-testid="stNumberInput"] label:contains("*") {
        font-weight: 600;
    }
    
    div[data-testid="stTextInput"] label:contains("*")::after,
    div[data-testid="stTextArea"] label:contains("*")::after,
    div[data-testid="stNumberInput"] label:contains("*")::after {
        color: #c41e3a;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Economic Impact Analysis Tool")

st.markdown('<p class="subtitle">Street Economics - Homestead CRA Edition</p>', unsafe_allow_html=True)

st.info("Complete the form below to generate your economic impact report")

if 'form_data' not in st.session_state:
    st.session_state['form_data'] = {}
if 'report_generated' not in st.session_state:
    st.session_state['report_generated'] = False
if 'form_key' not in st.session_state:
    st.session_state['form_key'] = 0
if 'uploaded_documents' not in st.session_state:
    st.session_state['uploaded_documents'] = []

st.markdown("### 📤 Import Previous Analysis")
uploaded_json = st.file_uploader("Upload a previously saved JSON file to restore your analysis", type=['json'], key="json_uploader")

if uploaded_json is not None:
    import json
    try:
        loaded_data = json.load(uploaded_json)
        
        st.session_state['form_data'] = loaded_data
        st.session_state['report_generated'] = True
        st.session_state['form_complete'] = True
        
        for key, value in loaded_data.items():
            st.session_state[key] = value
        
        st.success("✅ Data loaded successfully! Form fields have been populated.")
        st.info("Scroll down to review the data or click 'Start New Analysis' to begin fresh.")
    except (json.JSONDecodeError, ValueError) as e:
        st.error("❌ Error: Invalid JSON file. Please upload a valid JSON file exported from this application.")
    except Exception as e:
        st.error(f"❌ Error loading file: {str(e)}")

st.markdown("---")

with st.form(f"economic_impact_form_{st.session_state['form_key']}"):
    
    st.markdown("### 📎 Upload Project Documents (Optional)")
    st.caption("Upload any supporting documents about your project (images, PDFs, plans, etc.)")
    uploaded_files = st.file_uploader(
        "Choose files",
        type=['pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx', 'xlsx'],
        accept_multiple_files=True,
        help="Optional - add photos, site plans, or other project materials",
        key="project_documents",
        label_visibility="collapsed"
    )
    
    if uploaded_files:
        st.session_state['uploaded_documents'] = uploaded_files
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded")
    
    st.markdown("---")
    
    with st.expander("📋 Project Description", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            project_name = st.text_input(
                "Project Name *",
                placeholder="e.g., Downtown Cafe",
                help="Enter the business or project name",
                key="project_name"
            )
            
            property_address = st.text_area(
                "Property Address *",
                placeholder="e.g., 123 Main St, Homestead, FL",
                help="Full street address",
                height=60,
                key="property_address"
            )
            
            building_size = st.number_input(
                "Building Size (sf) *",
                min_value=0,
                step=100,
                help="Total building square footage",
                key="building_size"
            )
            
            current_taxable_value = st.number_input(
                "Current Taxable Value ($)",
                min_value=0,
                step=1000,
                help="Optional - current assessed value",
                key="current_taxable_value"
            )
        
        with col2:
            parcel_size = st.number_input(
                "Parcel (Lot) Size (sf)",
                min_value=0,
                step=100,
                help="Optional - total lot size",
                key="parcel_size"
            )
            
            building_bay_size = st.number_input(
                "Building/Bay/Space Size (sf) *",
                min_value=0,
                value=int(building_size) if building_size > 0 else 0,
                step=100,
                help="Specific space being used",
                key="building_bay_size"
            )
            
            current_sf = st.number_input(
                "Current SF *",
                min_value=0,
                value=int(building_size) if building_size > 0 else 0,
                step=100,
                help="Current square footage in use",
                key="current_sf"
            )
        
        additional_notes = st.text_area(
            "Additional Notes/Description",
            placeholder="Add any additional details about the project...",
            help="Optional - provide context, background, or special circumstances",
            height=90,
            key="additional_notes"
        )
    
    with st.expander("🏢 Project Type & Use", expanded=True):
        col3, col4 = st.columns(2)
        
        with col3:
            proposed_use = st.text_input(
                "Proposed Use *",
                placeholder="e.g., Restaurant, Retail Store, Office",
                help="Type of business or use",
                key="proposed_use"
            )
            
            proposed_use_sf = st.number_input(
                "Proposed Use SF *",
                min_value=0,
                step=100,
                help="Square footage for proposed use",
                key="proposed_use_sf"
            )
        
        with col4:
            rent_or_own = st.selectbox(
                "Rent or Own Property *",
                options=["Rent", "Own"],
                index=0,
                key="rent_or_own"
            )
            
            purchase_price = st.number_input(
                "Purchase Price (if Own) ($)",
                min_value=0,
                step=10000,
                help="Leave at 0 if renting",
                key="purchase_price"
            )
    
    with st.expander("💰 Project Costs", expanded=True):
        col5, col6 = st.columns(2)
        
        with col5:
            renovation = st.radio(
                "Renovation *",
                options=["yes", "no"],
                index=0,
                horizontal=True,
                key="renovation"
            )
            
            expansion = st.radio(
                "Expansion *",
                options=["yes", "no"],
                index=1,
                horizontal=True,
                key="expansion"
            )
            
            expansion_sf = st.number_input(
                "Expansion SF (if applicable)",
                min_value=0,
                step=100,
                key="expansion_sf"
            )
            
            total_development_costs = st.number_input(
                "Total Development Costs ($) *",
                min_value=0,
                step=1000,
                help="Total project investment",
                key="total_development_costs"
            )
            
            hard_costs = st.number_input(
                "Hard Costs ($) *",
                min_value=0,
                step=1000,
                help="Construction and renovation costs",
                key="hard_costs"
            )
        
        with col6:
            soft_costs = st.number_input(
                "Soft Costs ($)",
                min_value=0,
                step=1000,
                help="Design, permits, professional fees",
                key="soft_costs"
            )
            
            financing_costs = st.number_input(
                "Financing Costs ($)",
                min_value=0,
                step=1000,
                key="financing_costs"
            )
            
            ffe_costs = st.number_input(
                "FF&E Costs ($)",
                min_value=0,
                step=1000,
                help="Furniture, fixtures, and equipment",
                key="ffe_costs"
            )
            
            construction_duration = st.number_input(
                "Construction Duration (months)",
                min_value=0,
                max_value=60,
                step=1,
                key="construction_duration"
            )
        
        costs_sum = hard_costs + soft_costs + financing_costs + ffe_costs
        
        st.info(f"💡 **Cost Breakdown:** Soft Costs + Hard Costs + Financing + FF&E = ${costs_sum:,.0f}")
        
        if total_development_costs > 0:
            if costs_sum == total_development_costs:
                st.success(f"✅ Cost breakdown matches Total Development Costs (${total_development_costs:,.0f})")
            else:
                difference = total_development_costs - costs_sum
                if difference > 0:
                    st.warning(f"⚠️ Cost breakdown is ${abs(difference):,.0f} less than Total Development Costs")
                else:
                    st.warning(f"⚠️ Cost breakdown is ${abs(difference):,.0f} more than Total Development Costs")
        
        if hard_costs > total_development_costs and total_development_costs > 0:
            st.warning(f"⚠️ Hard Costs (${hard_costs:,.0f}) exceed Total Development Costs (${total_development_costs:,.0f})")
    
    with st.expander("👥 Operations", expanded=True):
        col7, col8 = st.columns(2)
        
        with col7:
            full_time_jobs = st.number_input(
                "Full Time Jobs *",
                min_value=0,
                step=1,
                help="Number of full-time positions",
                key="full_time_jobs"
            )
            
            part_time_jobs = st.number_input(
                "Part Time Jobs",
                min_value=0,
                step=1,
                help="Number of part-time positions",
                key="part_time_jobs"
            )
            
            average_wage = st.number_input(
                "Average Wage ($)",
                min_value=0,
                step=1000,
                help="Average annual wage per employee",
                key="average_wage"
            )
            
            occupancy = st.number_input(
                "Occupancy (# of people) *",
                min_value=1,
                value=20,
                step=1,
                help="Maximum occupancy capacity",
                key="occupancy"
            )
        
        with col8:
            num_tables = st.number_input(
                "# of tables (for restaurants)",
                min_value=0,
                step=1,
                help="Leave blank if not a restaurant",
                key="num_tables"
            )
            
            annual_operating_revenue = st.number_input(
                "Annual Operating Revenue (stabilized) ($)",
                min_value=0,
                step=10000,
                help="Projected annual revenue at stabilization",
                key="annual_operating_revenue"
            )
            
            annual_expenses = st.number_input(
                "Annual Expenses (stabilized) ($)",
                min_value=0,
                step=10000,
                help="Projected annual operating expenses",
                key="annual_expenses"
            )
            
            annual_rent = st.number_input(
                "Annual Rent ($)",
                min_value=0,
                step=1000,
                help="Annual rent payment (if applicable)",
                key="annual_rent"
            )
            
            rent_per_sf = st.number_input(
                "Rent per SF ($)",
                min_value=0.0,
                step=0.1,
                format="%.2f",
                help="Annual rent per square foot",
                key="rent_per_sf"
            )
    
    with st.expander("💵 Funding Request", expanded=True):
        funding_request = st.number_input(
            "Funding Request ($) *",
            min_value=0,
            step=1000,
            help="Amount of CRA funding requested for this project",
            key="funding_request"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    submitted = st.form_submit_button("Generate Report", use_container_width=True)
    
    if submitted:
        required_fields = {
            'project_name': ('Project Name', project_name),
            'property_address': ('Property Address', property_address),
            'building_size': ('Building Size', building_size),
            'building_bay_size': ('Building/Bay/Space Size', building_bay_size),
            'current_sf': ('Current SF', current_sf),
            'proposed_use': ('Proposed Use', proposed_use),
            'proposed_use_sf': ('Proposed Use SF', proposed_use_sf),
            'total_development_costs': ('Total Development Costs', total_development_costs),
            'hard_costs': ('Hard Costs', hard_costs),
            'occupancy': ('Occupancy', occupancy),
            'funding_request': ('Funding Request', funding_request)
        }
        
        missing_fields = []
        for field_key, (field_name, value) in required_fields.items():
            if value is None or value == '' or (isinstance(value, (int, float)) and value <= 0):
                missing_fields.append(field_name)
        
        if full_time_jobs < 0:
            missing_fields.append("Full Time Jobs (must be 0 or greater)")
        
        if missing_fields:
            st.error("⚠️ Please fill in all required fields:")
            for field in missing_fields:
                st.write(f"  • {field}")
        else:
            st.session_state['form_data'].update({
                'project_name': project_name,
                'property_address': property_address,
                'building_size': building_size,
                'current_taxable_value': current_taxable_value,
                'parcel_size': parcel_size,
                'building_bay_size': building_bay_size,
                'current_sf': current_sf,
                'additional_notes': additional_notes,
                'proposed_use': proposed_use,
                'proposed_use_sf': proposed_use_sf,
                'rent_or_own': rent_or_own,
                'purchase_price': purchase_price,
                'renovation': renovation,
                'expansion': expansion,
                'expansion_sf': expansion_sf,
                'total_development_costs': total_development_costs,
                'hard_costs': hard_costs,
                'soft_costs': soft_costs,
                'financing_costs': financing_costs,
                'ffe_costs': ffe_costs,
                'construction_duration': construction_duration,
                'full_time_jobs': full_time_jobs,
                'part_time_jobs': part_time_jobs,
                'average_wage': average_wage,
                'occupancy': occupancy,
                'num_tables': num_tables,
                'annual_operating_revenue': annual_operating_revenue,
                'annual_expenses': annual_expenses,
                'annual_rent': annual_rent,
                'rent_per_sf': rent_per_sf,
                'funding_request': funding_request
            })
            st.session_state['report_generated'] = True
            st.session_state['form_complete'] = True
            
            st.success("✅ Form validated successfully!")
            
            with st.spinner('🔄 Preparing your data for analysis...'):
                import time
                time.sleep(2)
            
            progress_bar = st.progress(0)
            st.write("Connecting to analysis engine...")
            for percent_complete in range(100):
                time.sleep(0.01)
                progress_bar.progress(percent_complete + 1)
            
            st.info("✅ Form submitted successfully! Generating your economic impact report...")

if st.session_state.get('form_complete', False):
    
    st.success("✅ Phase 1 Complete - Data Collection & Validation")
    
    if st.session_state['form_data']:
        data = st.session_state['form_data']
        
        st.markdown("---")
        st.subheader("Key Metrics Summary")
        
        total_jobs = data.get('full_time_jobs', 0) + data.get('part_time_jobs', 0)
        funding_ratio = (data.get('funding_request', 0) / data.get('total_development_costs', 1) * 100) if data.get('total_development_costs', 0) > 0 else 0
        cost_per_sf = (data.get('total_development_costs', 0) / data.get('building_size', 1)) if data.get('building_size', 0) > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Investment", 
                f"${data.get('total_development_costs', 0):,.0f}",
                help="Total Development Costs for the project"
            )
        
        with col2:
            st.metric(
                "Hard Costs", 
                f"${data.get('hard_costs', 0):,.0f}",
                help="Construction and renovation costs"
            )
        
        with col3:
            st.metric(
                "Total Jobs", 
                f"{total_jobs:,}",
                delta=f"FT: {data.get('full_time_jobs', 0):,}, PT: {data.get('part_time_jobs', 0):,}",
                help="Full-time and part-time jobs created"
            )
        
        with col4:
            st.metric(
                "Occupancy", 
                f"{data.get('occupancy', 0):,}",
                help="Maximum number of people"
            )
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Building Size", 
                f"{data.get('building_size', 0):,} sf",
                help="Total building square footage"
            )
        
        with col2:
            st.metric(
                "Cost per SF", 
                f"${cost_per_sf:,.0f}",
                help="Total development costs divided by building size"
            )
        
        with col3:
            st.metric(
                "Renovation", 
                data.get('renovation', 'N/A'),
                help="Whether project includes renovation"
            )
        
        with col4:
            st.metric(
                "Funding Request", 
                f"${data.get('funding_request', 0):,.0f}",
                delta=f"{funding_ratio:.1f}% of Total",
                help="CRA funding requested"
            )
        
        if data.get('annual_rent', 0) > 0 and data.get('proposed_use_sf', 0) > 0:
            calculated_rent_per_sf = data['annual_rent'] / data['proposed_use_sf']
            st.info(f"💡 **Rent Calculation:** Annual Rent ${data['annual_rent']:,.0f} ÷ Proposed Use SF {data['proposed_use_sf']:,.0f} = **${calculated_rent_per_sf:.2f} per SF**")
        elif data.get('rent_per_sf', 0) > 0 and data.get('proposed_use_sf', 0) > 0:
            calculated_annual_rent = data['rent_per_sf'] * data['proposed_use_sf']
            st.info(f"💡 **Rent Calculation:** Rent per SF ${data['rent_per_sf']:.2f} × Proposed Use SF {data['proposed_use_sf']:,.0f} = **${calculated_annual_rent:,.0f} Annual Rent**")
        
        st.markdown("---")
        st.subheader("Captured Data")
        
        with st.expander("📋 View All Form Data", expanded=False):
            st.markdown("**Project Description**")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Project Name:** {data.get('project_name', 'N/A')}")
                st.write(f"**Building Size:** {data.get('building_size', 0):,} sf")
                st.write(f"**Current SF:** {data.get('current_sf', 0):,} sf")
                if data.get('current_taxable_value', 0) > 0:
                    st.write(f"**Current Taxable Value:** ${data.get('current_taxable_value', 0):,}")
            with col2:
                st.write(f"**Property Address:** {data.get('property_address', 'N/A')}")
                if data.get('parcel_size', 0) > 0:
                    st.write(f"**Parcel Size:** {data.get('parcel_size', 0):,} sf")
                st.write(f"**Building/Bay/Space Size:** {data.get('building_bay_size', 0):,} sf")
            
            if data.get('additional_notes'):
                st.markdown("**Additional Notes:**")
                st.write(data.get('additional_notes'))
            
            st.markdown("")
            st.markdown("**Project Type & Use**")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Proposed Use:** {data.get('proposed_use', 'N/A')}")
                st.write(f"**Proposed Use SF:** {data.get('proposed_use_sf', 0):,} sf")
            with col2:
                st.write(f"**Rent or Own:** {data.get('rent_or_own', 'N/A')}")
                if data.get('purchase_price', 0) > 0:
                    st.write(f"**Purchase Price:** ${data.get('purchase_price', 0):,}")
            
            st.markdown("")
            st.markdown("**Project Costs**")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Total Development Costs:** ${data.get('total_development_costs', 0):,}")
                st.write(f"**Hard Costs:** ${data.get('hard_costs', 0):,}")
                if data.get('soft_costs', 0) > 0:
                    st.write(f"**Soft Costs:** ${data.get('soft_costs', 0):,}")
                if data.get('financing_costs', 0) > 0:
                    st.write(f"**Financing Costs:** ${data.get('financing_costs', 0):,}")
            with col2:
                st.write(f"**Renovation:** {data.get('renovation', 'N/A')}")
                st.write(f"**Expansion:** {data.get('expansion', 'N/A')}")
                if data.get('expansion_sf', 0) > 0:
                    st.write(f"**Expansion SF:** {data.get('expansion_sf', 0):,} sf")
                if data.get('ffe_costs', 0) > 0:
                    st.write(f"**FF&E Costs:** ${data.get('ffe_costs', 0):,}")
                if data.get('construction_duration', 0) > 0:
                    st.write(f"**Construction Duration:** {data.get('construction_duration', 0):,} months")
            
            st.markdown("")
            st.markdown("**Operations**")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Full Time Jobs:** {data.get('full_time_jobs', 0):,}")
                st.write(f"**Part Time Jobs:** {data.get('part_time_jobs', 0):,}")
                st.write(f"**Occupancy:** {data.get('occupancy', 0):,} people")
                if data.get('average_wage', 0) > 0:
                    st.write(f"**Average Wage:** ${data.get('average_wage', 0):,}")
            with col2:
                if data.get('num_tables', 0) > 0:
                    st.write(f"**# of Tables:** {data.get('num_tables', 0):,}")
                if data.get('annual_operating_revenue', 0) > 0:
                    st.write(f"**Annual Revenue:** ${data.get('annual_operating_revenue', 0):,}")
                if data.get('annual_expenses', 0) > 0:
                    st.write(f"**Annual Expenses:** ${data.get('annual_expenses', 0):,}")
                if data.get('annual_rent', 0) > 0:
                    st.write(f"**Annual Rent:** ${data.get('annual_rent', 0):,}")
                if data.get('rent_per_sf', 0) > 0:
                    st.write(f"**Rent per SF:** ${data.get('rent_per_sf', 0):.2f}")
            
            st.markdown("")
            st.markdown("**Funding Request**")
            st.write(f"**Funding Request:** ${data.get('funding_request', 0):,}")
            st.write(f"**Funding Ratio:** {funding_ratio:.1f}% of Total Development Costs")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            import json
            import re
            json_data = json.dumps(st.session_state['form_data'], indent=2)
            project_name_raw = data.get('project_name', 'project')
            project_name_clean = re.sub(r'[^a-zA-Z0-9_-]', '_', project_name_raw)
            project_name_clean = re.sub(r'_+', '_', project_name_clean)
            
            st.download_button(
                label="Download Form Data (JSON)",
                data=json_data,
                file_name=f"impact_analysis_{project_name_clean}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col2:
            if st.button("🔄 Start New Analysis", type="secondary", use_container_width=True, key="reset_button"):
                form_key_backup = st.session_state.get('form_key', 0)
                st.session_state.clear()
                st.session_state['form_key'] = form_key_backup + 1
                st.session_state['form_data'] = {}
                st.session_state['report_generated'] = False
                st.session_state['form_complete'] = False
                st.rerun()
        
        st.markdown("---")
        st.info("🎯 **Ready to generate your report?** Phase 2 coming next!")
        st.caption("Phase 1 Complete ✅ - Your data has been validated and is ready for economic impact analysis.")
