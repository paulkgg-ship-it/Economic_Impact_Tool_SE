# Economic Impact Analysis Tool

## Overview
A professional Streamlit web application designed for the Homestead CRA (Community Redevelopment Agency) to analyze economic impacts of development projects. The tool helps calculate and visualize the economic benefits of CRA-funded projects, integrating with Stack.ai for AI-powered report generation. The project aims to provide a comprehensive, user-friendly platform for economic impact assessment.

## User Preferences
Not specified. The agent should infer preferences from the provided `replit.md` and act accordingly, prioritizing clarity, maintainability, and functionality.

## System Architecture
The application is a Streamlit web application built with Python 3.11.

**UI/UX Decisions:**
- Professional landing page with custom branding.
- Clean, modern interface with custom CSS styling.
- **Color Scheme**: Primary color #1f4788 (Dark Blue), Secondary color #c41e3a (Red), Clean white background with subtle gray for content blocks.
- Custom button styling with hover effects, professional input field borders with focus states, responsive two-column layouts, clean visual hierarchy, rounded corners, and smooth transitions.
- All form fields are always visible (no dynamic show/hide behavior) with clear labeling for conditional fields.
- User-friendly error messages and professional progress indicators (spinner + progress bar).

**Technical Implementations:**
- **Form Structure**: 5 expandable sections (Project Description, Project Type & Use, Project Costs, Operations, Funding Request), all expanded by default.
- **Data Handling**: Session state framework for storing form data, streamlined form validation (only Proposed Use required + data quality checks), JSON import/export functionality for analysis data.
- **Validation Rules**: 
  - Required: Only "Proposed Use" field
  - Data Quality: At least one of Total Development Costs or Hard Costs must be > 0
  - Data Quality: Full Time Jobs cannot be negative (can be 0 for AI estimation)
  - Empty project names fallback to "Economic Impact Analysis" in reports
- **Cost Validation**: Intelligent cost validation and tracking, including real-time cost breakdown calculation and warnings for discrepancies.
- **Metrics**: Enhanced Key Metrics Summary dashboard with 8 calculated metrics (e.g., Total Jobs, Total Investment, Cost per SF, Funding Request ratio).
- **Reporting**: Professional report display with structured sections in logical order, download capabilities for reports (PDF with fallback to text) and analysis data (JSON).
- **Report Structure**: Reports display in this order for optimal readability:
  1. Executive Summary (overview of project impact)
  2. Key Metrics at a Glance (4 key metrics: Year 1 CRA Revenue, 10-Year CRA Total, Jobs Created, Annual Economic Output)
  3. Fiscal Impact: CRA Tax Increment (10-year taxable value and increment projection)
  4. Construction Phase (One-Time) (one-time economic impacts during development)
  5. Operations Phase (Recurring Annual) (ongoing annual economic effects)
  6. Ten-Year Operations Projection (long-term economic trajectory)
  7. Community and Qualitative Impacts (non-financial community benefits)
  8. Sources & Methodology (data sources, methodology, and assumptions)
- **Documents**: Project documents uploader supporting various file types (PDF, PNG, JPG, JPEG, DOC, DOCX, XLSX).

**Feature Specifications:**
- **Branding**: Street Economics logo displayed at top of page (centered, above main header)
- **Project Description**: Captures project name, address, current taxable value, current use, parcel size, building size, and current SF. All fields optional.
- **Project Type & Use**: Records proposed use* (REQUIRED - only required field in entire form), proposed use (bay/space size) SF, rent/own status, and purchase price. All fields except proposed use are optional.
- **Project Costs**: Details renovation, expansion, total development costs, hard costs, soft costs, financing costs, FF&E costs, and construction duration. All fields optional, but at least one of Total Development Costs OR Hard Costs must be > 0 for meaningful analysis.
- **Operations**: Collects full-time/part-time jobs (allows 0 with auto-estimation), average wage, occupancy (optional, can be 0), restaurant tables, annual operating revenue/expenses, and annual/per SF rent. All fields optional. Includes smart rent calculation in results.
- **Funding Request**: Captures the requested CRA funding amount (optional).

**System Design Choices:**
- **File Structure**: Organized into `app.py` (main application), `stack_client.py` (Stack.ai integration), `economic_calculator.py` (calculation engine), and `.streamlit/config.toml`.
- **Workflow**: `streamlit-app` running on port 5000.

## External Dependencies
- **Streamlit**: `streamlit==1.29.0` for the web application framework.
- **Python-dotenv**: `python-dotenv==1.0.0` for environment variable management.
- **Plotly**: `plotly==6.4.0` (installed for future visualization features).
- **Requests**: `requests==2.31.0` for making HTTP requests to external APIs.
- **Stack.ai**: Integrated for AI-powered economic impact report generation.
    - **Endpoint**: `https://api.stack-ai.com/inference/v0/run/{org_id}/{flow_id}`
    - **Authentication**: Bearer token via `STACK_AI_API_KEY` environment secret.
    - **Required Secrets**: `STACK_AI_API_KEY`, `STACK_AI_FLOW_ID`.
    - **Data Exchange**: Sends JSON string of form data, receives structured HTML report content in JSON format.