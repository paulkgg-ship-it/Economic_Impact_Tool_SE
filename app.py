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
            
            if rent_or_own == "Own":
                purchase_price = st.number_input(
                    "Purchase Price if Own ($) *",
                    min_value=0,
                    step=10000,
                    help="Purchase price of property",
                    key="purchase_price"
                )
            else:
                purchase_price = 0
    
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
            
            if expansion == "yes":
                expansion_sf = st.number_input(
                    "Expansion SF *",
                    min_value=0,
                    step=100,
                    key="expansion_sf"
                )
            else:
                expansion_sf = 0
            
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
        st.write("Fields coming soon")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    submitted = st.form_submit_button("Generate Report", use_container_width=True)
    
    if submitted:
        errors = []
        
        if not project_name:
            errors.append("Project Name is required")
        if not property_address:
            errors.append("Property Address is required")
        if building_size <= 0:
            errors.append("Building Size must be greater than 0")
        if building_bay_size <= 0:
            errors.append("Building/Bay/Space Size must be greater than 0")
        if current_sf <= 0:
            errors.append("Current SF must be greater than 0")
        
        if not proposed_use:
            errors.append("Proposed Use is required")
        if proposed_use_sf <= 0:
            errors.append("Proposed Use SF must be greater than 0")
        if rent_or_own == "Own" and purchase_price <= 0:
            errors.append("Purchase Price is required when owning property")
        
        if total_development_costs <= 0:
            errors.append("Total Development Costs must be greater than 0")
        if hard_costs <= 0:
            errors.append("Hard Costs must be greater than 0")
        if expansion == "yes" and expansion_sf <= 0:
            errors.append("Expansion SF is required when Expansion is 'yes'")
        
        if full_time_jobs < 0:
            errors.append("Full Time Jobs must be 0 or greater")
        if occupancy < 1:
            errors.append("Occupancy must be at least 1")
        
        if errors:
            for error in errors:
                st.error(f"❌ {error}")
        else:
            st.session_state['form_data'].update({
                'project_name': project_name,
                'property_address': property_address,
                'building_size': building_size,
                'current_taxable_value': current_taxable_value,
                'parcel_size': parcel_size,
                'building_bay_size': building_bay_size,
                'current_sf': current_sf,
                'proposed_use': proposed_use,
                'proposed_use_sf': proposed_use_sf,
                'rent_or_own': rent_or_own,
                'purchase_price': purchase_price if rent_or_own == "Own" else 0,
                'renovation': renovation,
                'expansion': expansion,
                'expansion_sf': expansion_sf if expansion == "yes" else 0,
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
                'rent_per_sf': rent_per_sf
            })
            st.session_state['report_generated'] = True
            st.success("✅ Report generation initiated!")

if st.session_state.get('report_generated', False):
    st.info("Report results will be displayed here once all form sections are completed.")
    
    if st.session_state['form_data']:
        data = st.session_state['form_data']
        
        st.markdown("---")
        st.subheader("📊 Key Metrics Summary")
        
        col_metric1, col_metric2, col_metric3 = st.columns(3)
        
        with col_metric1:
            total_jobs = data.get('full_time_jobs', 0) + data.get('part_time_jobs', 0)
            st.metric("Total Jobs", total_jobs, delta=f"FT: {data.get('full_time_jobs', 0)}, PT: {data.get('part_time_jobs', 0)}")
        
        with col_metric2:
            st.metric("Total Development Costs", f"${data.get('total_development_costs', 0):,.0f}")
        
        with col_metric3:
            st.metric("Occupancy Capacity", data.get('occupancy', 0))
        
        if data.get('annual_rent', 0) > 0 and data.get('proposed_use_sf', 0) > 0:
            calculated_rent_per_sf = data['annual_rent'] / data['proposed_use_sf']
            st.info(f"💡 **Rent Calculation:** Annual Rent ${data['annual_rent']:,.0f} ÷ Proposed Use SF {data['proposed_use_sf']:,.0f} = **${calculated_rent_per_sf:.2f} per SF**")
        elif data.get('rent_per_sf', 0) > 0 and data.get('proposed_use_sf', 0) > 0:
            calculated_annual_rent = data['rent_per_sf'] * data['proposed_use_sf']
            st.info(f"💡 **Rent Calculation:** Rent per SF ${data['rent_per_sf']:.2f} × Proposed Use SF {data['proposed_use_sf']:,.0f} = **${calculated_annual_rent:,.0f} Annual Rent**")
        
        st.markdown("---")
        st.subheader("📋 Captured Data")
        with st.expander("View All Form Data", expanded=False):
            for key, value in st.session_state['form_data'].items():
                st.write(f"**{key.replace('_', ' ').title()}:** {value}")
