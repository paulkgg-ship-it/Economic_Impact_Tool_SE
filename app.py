import streamlit as st
from dotenv import load_dotenv
from economic_calculator import calculate_economic_impact
import plotly.graph_objects as go
import plotly.express as px
import os
import sys

load_dotenv()

st.set_page_config(
    page_title="Economic Impact Analysis Tool",
    page_icon="📊",
    layout="wide"
)

# ===== DIAGNOSTIC MODE FOR STREAMLIT CLOUD =====
# Check if we're on Streamlit Cloud (no Replit env vars)
is_streamlit_cloud = 'REPL_ID' not in os.environ

if is_streamlit_cloud:
    try:
        # Check secrets - Streamlit Cloud uses st.secrets
        api_key = st.secrets.get("STACK_AI_API_KEY") if hasattr(st, 'secrets') else os.environ.get("STACK_AI_API_KEY")
        flow_id = st.secrets.get("STACK_AI_FLOW_ID") if hasattr(st, 'secrets') else os.environ.get("STACK_AI_FLOW_ID")
        
        if not api_key:
            st.error("❌ Missing STACK_AI_API_KEY in secrets")
            st.info("Add secrets in Streamlit Cloud: Settings → Secrets")
            st.stop()
        
        if not flow_id:
            st.error("❌ Missing STACK_AI_FLOW_ID in secrets")
            st.info("Add secrets in Streamlit Cloud: Settings → Secrets")
            st.stop()
        
        # Set environment variables from secrets for compatibility
        os.environ["STACK_AI_API_KEY"] = api_key
        os.environ["STACK_AI_FLOW_ID"] = flow_id
        
        st.write("✓ Secrets loaded")
        
        from data_processor import data_processor
        st.write("✓ data_processor imported")
        
        from stack_client import StackAIClient
        st.write("✓ stack_client imported")
        
        from PIL import Image
        try:
            logo = Image.open("SE Logo.png")
            st.write("✓ Logo loaded")
        except FileNotFoundError:
            st.warning("⚠️ SE Logo.png not found - continuing without logo")
        
        st.success("✅ All checks passed - app should work")
        
    except Exception as e:
        st.error(f"❌ Startup error: {str(e)}")
        st.code(f"Error type: {type(e).__name__}")
        import traceback
        st.code(traceback.format_exc())
        st.stop()

# ===== END DIAGNOSTIC MODE =====

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
    
    .main-header {
        color: #1f4788;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        color: #666;
        font-size: 1.3rem;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    </style>
""", unsafe_allow_html=True)

# Add logo and header aligned
logo_col, header_col = st.columns([1, 9])

with logo_col:
    try:
        from PIL import Image
        logo = Image.open("SE Logo.png")
        st.image(logo, width=80)
    except Exception as e:
        # If logo fails to load, skip it
        pass

with header_col:
    st.markdown('<div class="main-header">Economic Impact Analysis Tool</div>', unsafe_allow_html=True)

st.markdown('<div class="sub-header">Street Economics - Homestead CRA Edition</div>', unsafe_allow_html=True)

st.info("Complete the form below to generate your economic impact report")

if 'form_data' not in st.session_state:
    st.session_state['form_data'] = {}
if 'report_generated' not in st.session_state:
    st.session_state['report_generated'] = False
if 'form_key' not in st.session_state:
    st.session_state['form_key'] = 0
if 'uploaded_documents' not in st.session_state:
    st.session_state['uploaded_documents'] = []
if 'report_text' not in st.session_state:
    st.session_state['report_text'] = None
if 'api_error' not in st.session_state:
    st.session_state['api_error'] = None

with st.form(f"economic_impact_form_{st.session_state['form_key']}"):
    
    st.markdown("### Upload Project Documents (Optional)")
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
    
    with st.expander("Property Description", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            project_name = st.text_input(
                "Project Name",
                placeholder="e.g., Downtown Cafe",
                help="Enter the business or project name",
                key="project_name"
            )
            
            property_address = st.text_area(
                "Property Address",
                placeholder="e.g., 123 Main St, Homestead, FL",
                help="Full street address",
                height=60,
                key="property_address"
            )
            
            current_use = st.text_input(
                "Current Use",
                placeholder="e.g., Vacant, Office, Warehouse",
                help="What is the current use of the space? (Optional - helps with narrative)",
                key="current_use"
            )
        
        with col2:
            current_taxable_value = st.number_input(
                "Current Taxable Value ($)",
                min_value=0,
                step=1000,
                help="Optional - current assessed value",
                key="current_taxable_value"
            )
            
            parcel_size = st.number_input(
                "Parcel (Lot) Size (sf)",
                min_value=0,
                step=100,
                help="Optional - total lot size",
                key="parcel_size"
            )
            
            building_size = st.number_input(
                "Building Size (sf)",
                min_value=0,
                step=100,
                help="Optional - total building square footage",
                key="building_size"
            )
    
    with st.expander("Project Type & Use", expanded=True):
        col3, col4 = st.columns(2)
        
        with col3:
            proposed_use = st.text_input(
                "Proposed Use *",
                placeholder="e.g., Restaurant, Retail Store, Office",
                help="Type of business or use (REQUIRED)",
                key="proposed_use"
            )
            
            proposed_use_sf = st.number_input(
                "Proposed Use (Bay/Space Size) (sf)",
                min_value=0,
                step=100,
                help="Square footage dedicated to the proposed use",
                key="proposed_use_sf"
            )
        
        with col4:
            rent_or_own = st.selectbox(
                "Rent or Own Property",
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
        
        additional_notes = st.text_area(
            "Additional Notes/Description",
            placeholder="Add any additional details about the project...",
            help="Optional - provide context, background, or special circumstances",
            height=90,
            key="additional_notes"
        )
    
    with st.expander("Project Costs", expanded=True):
        col5, col6 = st.columns(2)
        
        with col5:
            renovation = st.radio(
                "Renovation",
                options=["yes", "no"],
                index=0,
                horizontal=True,
                key="renovation"
            )
            
            expansion = st.radio(
                "Expansion",
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
                "Total Development Costs ($)",
                min_value=0,
                step=1000,
                help="Total project investment (at least one of Total Development Costs or Hard Costs required)",
                key="total_development_costs"
            )
            
            hard_costs = st.number_input(
                "Hard Costs ($)",
                min_value=0,
                step=1000,
                help="Construction and renovation costs (at least one of Total Development Costs or Hard Costs required)",
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
    
    with st.expander("Operations", expanded=True):
        st.caption("If you don't know some items, enter 0 and we will estimate based on industry and local standards.")
        
        col7, col8 = st.columns(2)
        
        with col7:
            full_time_jobs = st.number_input(
                "Full Time Jobs",
                min_value=0,
                value=0,
                step=1,
                key="full_time_jobs"
            )
            
            part_time_jobs = st.number_input(
                "Part Time Jobs",
                min_value=0,
                value=0,
                step=1,
                key="part_time_jobs"
            )
            
            average_wage = st.number_input(
                "Average Wage ($)",
                min_value=0,
                value=0,
                step=1000,
                key="average_wage"
            )
            
            occupancy = st.number_input(
                "Occupancy (# of people)",
                min_value=0,
                value=0,
                step=1,
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
    
    with st.expander("Funding Request", expanded=True):
        funding_request = st.number_input(
            "Funding Request ($)",
            min_value=0,
            step=1000,
            help="Amount of CRA funding requested for this project",
            key="funding_request"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    submitted = st.form_submit_button("Generate Report", use_container_width=True)
    
    if submitted:
        # Validate required field and basic data quality
        validation_errors = []
        
        # Required: Proposed Use
        if not proposed_use or proposed_use.strip() == '':
            validation_errors.append("Proposed Use (required)")
        
        # Data quality checks (optional fields, but if filled, must be valid)
        # At least one cost field should be provided for meaningful analysis
        if total_development_costs <= 0 and hard_costs <= 0:
            validation_errors.append("At least one of Total Development Costs or Hard Costs must be greater than 0")
        
        # Jobs can be 0 (for estimation), but not negative
        if full_time_jobs < 0:
            validation_errors.append("Full Time Jobs cannot be negative")
        
        if validation_errors:
            st.error("⚠️ Please address the following issues:")
            for error in validation_errors:
                st.write(f"  • {error}")
        else:
            # Form is valid, proceed with generation
            st.success("✅ Form validated successfully!")
            st.session_state['form_data'].update({
                'project_name': project_name,
                'property_address': property_address,
                'building_size': building_size,
                'current_taxable_value': current_taxable_value,
                'current_use': current_use,
                'parcel_size': parcel_size,
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
            st.session_state['form_complete'] = True
            
            # Call Stack.ai to generate report with enhanced loading indicator
            progress_placeholder = st.empty()
            progress_placeholder.info("🔄 **Analyzing your project data...** Please wait while we generate your economic impact report.")
            
            with st.spinner('Generating report... This may take 30-60 seconds.'):
                from stack_client import get_stack_client
                import traceback
                
                try:
                    stack_client = get_stack_client()
                    
                    if stack_client is None:
                        # Stack.ai credentials not configured
                        st.session_state['api_error'] = "Stack.ai API credentials not configured. Please add STACK_AI_API_KEY and STACK_AI_FLOW_ID to your environment secrets."
                        st.session_state['report_generated'] = False
                        st.session_state['report_text'] = None
                    else:
                        result = stack_client.run_analysis(st.session_state['form_data'])
                        
                        if result['success']:
                            st.session_state['report_generated'] = True
                            st.session_state['report_text'] = result['report']
                            st.session_state['report_json'] = result.get('report_json')  # Store structured JSON
                            st.session_state['api_error'] = None
                            st.success("✅ Report generated successfully!")
                            st.rerun()
                        else:
                            st.session_state['api_error'] = f"API Error: {result['error']}"
                            st.session_state['report_generated'] = False
                            st.session_state['report_text'] = None
                            
                except Exception as e:
                    st.session_state['api_error'] = f"Unexpected error: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
                    st.session_state['report_generated'] = False
                    st.session_state['report_text'] = None

# Display report if generated
if st.session_state.get('report_generated', False):
    st.markdown("---")
    st.markdown("## Economic Impact Report")
    project_name_display = st.session_state.form_data.get('project_name', '').strip() or "Economic Impact Analysis"
    st.markdown(f"### {project_name_display}")
    
    # Check if we have JSON data
    if st.session_state.get('report_json'):
        report_data = st.session_state.report_json
        
        # ===== EXECUTIVE SUMMARY =====
        st.markdown("### Executive Summary")
        st.write(report_data.get('executive_summary', ''))
        
        st.markdown("---")
        
        # ===== KEY METRICS =====
        st.markdown("### Key Metrics at a Glance")
        
        col1, col2, col3, col4 = st.columns(4)
        
        fiscal = report_data.get('fiscal_highlights', {})
        construction = report_data.get('construction_impact', {})
        operations = report_data.get('operations_impact', {})
        
        # Get total values from construction table
        const_total = next((item for item in construction.get('table', []) if item['impact_type'] == 'Total'), {})
        ops_total = next((item for item in operations.get('table', []) if item['impact_type'] == 'Total'), {})
        
        with col1:
            st.metric(
                "Year 1 CRA Revenue",
                f"${fiscal.get('year_1_cra_revenue', 0):,.0f}"
            )
        
        with col2:
            st.metric(
                "10-Year CRA Total",
                f"${fiscal.get('ten_year_cumulative', 0):,.0f}"
            )
        
        with col3:
            st.metric(
                "Jobs Created (Annual)",
                f"{ops_total.get('jobs', 0):.1f}"
            )
        
        with col4:
            st.metric(
                "Annual Economic Output",
                f"${ops_total.get('economic_output', 0):,.0f}"
            )
        
        st.markdown("---")
        
        # ===== CRA INCREMENT PROJECTION =====
        st.markdown("### Fiscal Impact: CRA Tax Increment")
        
        if report_data.get('cra_increment_projection'):
            import pandas as pd
            
            cra_df = pd.DataFrame(report_data['cra_increment_projection'])
            
            # Format numbers
            cra_df['taxable_value'] = cra_df['taxable_value'].apply(lambda x: f"${x:,.0f}")
            cra_df['cra_increment'] = cra_df['cra_increment'].apply(lambda x: f"${x:,.0f}")
            cra_df['cumulative'] = cra_df['cumulative'].apply(lambda x: f"${x:,.0f}")
            
            # Rename columns
            cra_df.columns = ['Year', 'Taxable Value', 'CRA Increment', 'Cumulative']
            
            st.dataframe(cra_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # ===== CONSTRUCTION IMPACT =====
        st.markdown("### Construction Phase (One-Time)")
        
        st.write(construction.get('narrative', ''))
        
        if construction.get('table'):
            import pandas as pd
            
            const_df = pd.DataFrame(construction['table'])
            
            # Format numbers
            const_df['economic_output'] = const_df['economic_output'].apply(lambda x: f"${x:,.0f}")
            const_df['jobs'] = const_df['jobs'].apply(lambda x: f"{x:.1f}")
            const_df['earnings'] = const_df['earnings'].apply(lambda x: f"${x:,.0f}")
            
            # Rename columns
            const_df.columns = ['Impact Type', 'Economic Output', 'Jobs', 'Earnings']
            
            st.dataframe(const_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # ===== OPERATIONS IMPACT =====
        st.markdown("### Operations Phase (Recurring Annual)")
        
        st.write(operations.get('narrative', ''))
        
        if operations.get('table'):
            import pandas as pd
            
            ops_df = pd.DataFrame(operations['table'])
            
            # Format numbers
            ops_df['economic_output'] = ops_df['economic_output'].apply(lambda x: f"${x:,.0f}")
            ops_df['jobs'] = ops_df['jobs'].apply(lambda x: f"{x:.1f}")
            ops_df['earnings'] = ops_df['earnings'].apply(lambda x: f"${x:,.0f}")
            
            # Rename columns
            ops_df.columns = ['Impact Type', 'Economic Output', 'Jobs', 'Earnings']
            
            st.dataframe(ops_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # ===== 10-YEAR PROJECTION =====
        st.markdown("### Ten-Year Operations Projection")
        
        projection = report_data.get('ten_year_projection', {})
        st.write(projection.get('narrative', ''))
        
        if projection.get('table'):
            import pandas as pd
            
            proj_df = pd.DataFrame(projection['table'])
            
            # Format numbers
            proj_df['annual_output'] = proj_df['annual_output'].apply(lambda x: f"${x:,.0f}")
            proj_df['jobs'] = proj_df['jobs'].apply(lambda x: f"{x:.1f}")
            proj_df['labor_income'] = proj_df['labor_income'].apply(lambda x: f"${x:,.0f}")
            
            # Rename columns
            proj_df.columns = ['Year', 'Annual Output', 'Jobs', 'Labor Income']
            
            st.dataframe(proj_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # ===== COMMUNITY IMPACTS =====
        st.markdown("### Community and Qualitative Impacts")
        
        if report_data.get('community_impacts'):
            for impact in report_data['community_impacts']:
                st.markdown(f"**{impact.get('category', '')}**")
                st.write(impact.get('description', ''))
                st.write("")  # Add spacing
        
        st.markdown("---")
        
        # ===== SOURCES & METHODOLOGY =====
        st.markdown("### Sources & Methodology")
        
        # Always show CRA-specific methodology (ignore Stack.ai version)
        st.markdown("""
**Data Sources:**
- **Economic Multipliers:** Lightcast 2025 data for Homestead/South Dade region (NAICS-specific industry multipliers)
- **Demographics:** Esri 2025 demographic profiles for Homestead, FL
- **Real Estate Data:** CoStar 2025 market data for Homestead commercial properties
- **Fiscal Parameters:** City of Homestead and Miami-Dade County FY 2025 adopted millage rates

**Methodology:**

This analysis uses economic modeling based on the EMSI Type II methodology, which captures:
1. **Direct effects** - the immediate impact of project investment and operations
2. **Indirect effects** - supply chain impacts as businesses purchase goods and services
3. **Induced effects** - household spending impacts as workers spend their earnings in the local economy

**Fiscal Impact Calculations:**
- Incremental taxable value calculated as 60% of hard construction costs (standard capitalization rate for tenant improvements)
- Ad valorem taxes calculated using combined City and County millage rates
- CRA captures 95% of incremental tax revenue; 5% retained by each government
- 10-year projections assume 3% annual property value growth

**Economic Impact Calculations:**
- Construction impacts based on total development costs
- Direct construction jobs estimated at 1 job per $100,000 investment
- Operations impacts based on projected revenue or industry-standard sales per square foot
- Industry-specific multipliers applied to calculate indirect and induced effects
- Job-years represent the cumulative employment over the analysis period (e.g., 10 jobs × 10 years = 100 job-years)

**Conservative Assumptions:**
- Revenue estimates use lower end of industry averages when actual data not provided
- Employment multipliers are region-specific to avoid overstatement
- Growth rates (2.5% output, 1% employment) are conservative relative to historical trends
- All figures rounded to whole dollars

**Limitations:**
- Analysis assumes project is completed and operating as described
- Does not account for economic downturns, market disruptions, or competitive changes
- Multipliers are averages and may vary based on specific supply chain relationships
- Fiscal projections assume stable millage rates and capture percentages

This methodology is consistent with standard economic development impact analysis practices and is designed to provide conservative, defensible estimates for CRA investment decisions.
""")
        
        st.markdown("---")
        
        # ===== ACTION BUTTONS =====
        col1, col2 = st.columns(2)
        
        with col1:
            # Primary: PDF Download
            report_content = st.session_state.get('report_text', '')
            project_name = st.session_state.form_data.get('project_name', 'Economic_Impact_Analysis')
            
            try:
                from pdf_generator import generate_pdf_from_markdown
                
                pdf_bytes = generate_pdf_from_markdown(
                    report_content,
                    title=f"Economic Impact Report - {project_name}"
                )
                
                st.download_button(
                    label="Download Report (PDF)",
                    data=pdf_bytes,
                    file_name=f"economic_impact_{project_name.replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary"
                )
            except Exception as e:
                st.error(f"PDF generation failed: {str(e)}")
                # Fallback to markdown
                st.download_button(
                    label="Download Report (Markdown)",
                    data=report_content,
                    file_name=f"economic_impact_{project_name.replace(' ', '_')}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
        
        with col2:
            # Generate new report button
            if st.button("Generate New Report", use_container_width=True):
                st.session_state.report_generated = False
                st.session_state.report_text = None
                st.session_state.report_json = None
                st.rerun()
        
        # Advanced options (JSON download) - hidden in expander
        with st.expander("Advanced Options"):
            import json
            st.download_button(
                label="Download Raw Data (JSON)",
                data=json.dumps(report_data, indent=2),
                file_name=f"analysis_data_{st.session_state.form_data.get('project_name', 'report').replace(' ', '_')}.json",
                mime="application/json",
                use_container_width=True
            )
    
    else:
        # Fallback if no JSON (show raw text)
        st.markdown(st.session_state.get('report_text', 'No report generated'))
        
        # Simple download button
        st.download_button(
            label="Download Report",
            data=st.session_state.get('report_text', ''),
            file_name=f"economic_impact_{st.session_state.form_data.get('project_name', 'report').replace(' ', '_')}.txt",
            mime="text/plain"
        )

# Show data collection summary if form is complete but report not yet generated
elif st.session_state.get('form_complete', False):
    
    st.success("✅ Data Collection Complete")
    
    # Display API error if one occurred
    if st.session_state.get('api_error'):
        st.error(f"❌ Report Generation Failed")
        st.error(st.session_state['api_error'])
        st.info("Your form data has been saved below. You can try generating the report again or download your data.")
    
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

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9rem; margin-top: 2rem;'>
        Powered by Street Economics | BusinessFlare® Analytics
    </div>
""", unsafe_allow_html=True)
