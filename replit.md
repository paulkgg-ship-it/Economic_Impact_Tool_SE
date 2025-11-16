# Economic Impact Analysis Tool

## Overview
A professional Streamlit web application designed for the Homestead CRA (Community Redevelopment Agency) to analyze economic impacts of development projects. The tool helps calculate and visualize the economic benefits of CRA-funded projects.

## Project Details
- **Name**: Economic Impact Analysis Tool
- **Edition**: Street Economics - Homestead CRA Edition
- **Technology Stack**: Python 3.11, Streamlit 1.29.0
- **Port**: 5000

## Current State (Updated: November 16, 2025)
The application currently has:
- Professional landing page with custom branding
- Clean, modern interface with custom CSS styling
- Form structure with 5 expandable sections (all expanded by default):
  1. 📋 Project Description ✅ COMPLETED
  2. 🏢 Project Type & Use ✅ COMPLETED
  3. 💰 Project Costs ✅ COMPLETED
  4. 👥 Operations ✅ COMPLETED
  5. 💵 Funding Request (fields pending)
- Full-width "Generate Report" button with primary color styling
- Session state framework for form data storage
- Form validation with error messages
- Intelligent cost validation and tracking
- Key Metrics Summary dashboard with calculated values
- Captured data display functionality

### 📋 Project Description Section (Completed)
**Layout**: 2-column layout using st.columns(2), with full-width field at bottom

**Left Column Fields**:
- Project Name * (required) - Text input with placeholder
- Property Address * (required) - Text area (2 rows) with placeholder
- Building Size (sf) * (required) - Number input
- Current Taxable Value ($) (optional) - Number input

**Right Column Fields**:
- Parcel (Lot) Size (sf) (optional) - Number input
- Building/Bay/Space Size (sf) * (required) - Number input with auto-fill from Building Size
- Current SF * (required) - Number input with auto-fill from Building Size

**Full-Width Field** (positioned after columns):
- Additional Notes/Description (optional) - Multi-line text area (3 rows), placeholder: "Add any additional details about the project...", help text for context/background/special circumstances

**Features**:
- Required fields marked with red asterisk (*)
- Auto-fill functionality for dependent fields
- Form validation with error messages
- Help text for all fields
- Full-width text area for extended notes and descriptions
- Session state storage of all values
- Data display after successful submission

### 🏢 Project Type & Use Section (Completed)
**Layout**: 2-column layout using st.columns(2)

**Left Column Fields**:
- Proposed Use * (required) - Text input with placeholder "e.g., Restaurant, Retail Store, Office"
- Proposed Use SF * (required) - Number input for square footage

**Right Column Fields**:
- Rent or Own Property * (required) - Selectbox with options ["Rent", "Own"], defaults to "Rent"
- Purchase Price if Own ($) * (conditional) - Number input, only appears when "Own" is selected

**Features**:
- Dynamic conditional rendering: Purchase Price field shows/hides based on Rent/Own selection
- Form validation for all required fields
- Conditional validation: Purchase Price required only when "Own" is selected
- Help text for all fields
- Session state storage with proper handling of conditional fields
- All values captured and displayed after successful submission

### 💰 Project Costs Section (Completed)
**Layout**: 2-column layout using st.columns(2)

**Pre-Form Control** (appears BEFORE the form):
- "Will this project include an expansion?" - Radio buttons ["no", "yes"], horizontal layout, defaults to "no"
- This control is OUTSIDE the form to enable real-time conditional rendering
- Selection is stored in st.session_state['expansion_selection'] for immediate access

**Left Column Fields**:
- Renovation * (required) - Radio buttons ["yes", "no"], horizontal layout, defaults to "yes"
- Expansion SF * (conditional) - Number input, appears IMMEDIATELY when expansion selector = "yes"
- Total Development Costs ($) * (required) - Number input with help text
- Hard Costs ($) * (required) - Number input with help text

**Right Column Fields**:
- Soft Costs ($) (optional) - Number input with help text
- Financing Costs ($) (optional) - Number input
- FF&E Costs ($) (optional) - Number input with help text
- Construction Duration (months) (optional) - Number input, max 60 months

**Intelligent Cost Tracking**:
- Real-time cost breakdown calculation: Soft + Hard + Financing + FF&E
- Info box displays total cost breakdown with formatted currency
- Success message when breakdown matches Total Development Costs
- Warning message when breakdown differs from Total Development Costs
- Warning message when Hard Costs exceed Total Development Costs
- All amounts displayed with comma formatting for readability

**Features**:
- **Real-time conditional rendering**: Expansion SF field appears/disappears IMMEDIATELY when user toggles expansion selector (no form submission needed)
- **Session state pattern**: Expansion selector placed outside form to enable instant UI updates while maintaining form data integrity
- Intelligent validation: warns but doesn't block when costs don't match
- Form validation for all required fields
- Conditional validation: Expansion SF required only when Expansion = "yes"
- Real-time cost comparison and validation
- Help text for key fields
- Session state storage with proper handling of conditional fields
- All values captured and displayed after successful submission

### 👥 Operations Section (Completed)
**Layout**: 2-column layout using st.columns(2)

**Left Column Fields**:
- Full Time Jobs * (required) - Number input, minimum 0
- Part Time Jobs (optional) - Number input, minimum 0
- Average Wage ($) (optional) - Number input with help text
- Occupancy (# of people) * (required) - Number input, minimum 1, default 20

**Right Column Fields**:
- # of tables (for restaurants) (optional) - Number input for restaurant-specific data
- Annual Operating Revenue (stabilized) ($) (optional) - Number input with help text
- Annual Expenses (stabilized) ($) (optional) - Number input with help text
- Annual Rent ($) (optional) - Number input with help text
- Rent per SF ($) (optional) - Number input with decimal precision (format: "%.2f")

**Key Metrics Summary (Post-Submission)**:
After form submission, displays a dashboard with:
- **Total Jobs Metric**: Automatically calculated (Full Time + Part Time) with breakdown
- **Total Development Costs Metric**: Displays total investment
- **Occupancy Capacity Metric**: Shows maximum occupancy
- **Rent Calculation Helper**: 
  - If Annual Rent entered: Shows calculated rent per SF (Annual Rent ÷ Proposed Use SF)
  - If Rent per SF entered: Shows calculated annual rent (Rent per SF × Proposed Use SF)

**Features**:
- Simple, intuitive form inputs without dynamic auto-calculation (Streamlit limitation)
- Smart rent calculation displayed in results section after submission
- Total jobs automatically calculated and displayed in Key Metrics Summary
- Form validation for required fields (Full Time Jobs, Occupancy)
- Help text for all key fields
- Session state storage of all values
- Professional metrics display using st.metric() components
- All values captured and displayed after successful submission

## Design Specifications

### Color Scheme
- **Primary Color**: #1f4788 (Dark Blue) - used for headers, buttons, and accents
- **Secondary Color**: #c41e3a (Red) - used for special highlights and accents
- **Background**: Clean white with subtle gray backgrounds for content blocks

### Styling Features
- Custom button styling with hover effects
- Professional input field borders with focus states
- Responsive two-column layouts
- Clean visual hierarchy with proper spacing and padding
- Rounded corners and smooth transitions

## File Structure
```
.
├── app.py                      # Main Streamlit application
├── economic_calculator.py      # Economic impact calculation engine (for future use)
├── .streamlit/
│   └── config.toml            # Streamlit server configuration
├── pyproject.toml             # Python project dependencies
└── replit.md                  # This documentation file
```

## Dependencies
- streamlit==1.29.0
- python-dotenv==1.0.0
- plotly==6.4.0 (installed for future visualization features)

## Workflow
- **Workflow Name**: streamlit-app
- **Command**: `streamlit run app.py --server.port 5000`
- **Output Type**: webview
- **Port**: 5000

## Next Steps
The form sections currently contain placeholder text ("Fields coming soon"). Future development will add:
- Actual form fields for data collection in each section
- Economic impact calculation logic
- Data visualization components
- Report generation and export functionality
- External API integrations for economic data

## Session State Management
The application uses Streamlit's session state to manage:
- `form_data`: Dictionary storing all form input data
- `report_generated`: Boolean flag indicating if report has been generated

## Testing
The application has been tested for:
- Visual appearance and styling
- Expandable section functionality
- Button interactions and state management
- Success message display
- Responsive layout
