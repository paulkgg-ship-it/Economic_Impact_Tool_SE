from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration


def generate_pdf_from_json(report_data: dict, project_name: str) -> bytes:
    """
    Generate PDF from report JSON data
    
    Args:
        report_data: Full report JSON with all sections
        project_name: Name of the project
    
    Returns:
        PDF file as bytes
    """
    
    # Build HTML sections from JSON
    html_sections = []
    
    # Executive Summary
    html_sections.append("<h2>Executive Summary</h2>")
    html_sections.append(f"<p>{report_data.get('executive_summary', '')}</p>")
    
    # Key Metrics
    fiscal = report_data.get('fiscal_highlights', {})
    html_sections.append("<h2>Key Metrics at a Glance</h2>")
    html_sections.append("<div class='metrics-grid'>")
    html_sections.append(f"<div class='metric'><span class='metric-label'>Year 1 CRA Revenue</span><span class='metric-value'>${fiscal.get('year_1_cra_revenue', 0):,.0f}</span></div>")
    html_sections.append(f"<div class='metric'><span class='metric-label'>10-Year Cumulative</span><span class='metric-value'>${fiscal.get('ten_year_cumulative', 0):,.0f}</span></div>")
    
    # Get job totals from operations
    operations = report_data.get('operations_impact', {})
    ops_total = next((item for item in operations.get('table', []) if item.get('impact_type') == 'Total'), {})
    html_sections.append(f"<div class='metric'><span class='metric-label'>Jobs Created (Annual)</span><span class='metric-value'>{ops_total.get('jobs', 0):.1f}</span></div>")
    html_sections.append(f"<div class='metric'><span class='metric-label'>Annual Economic Output</span><span class='metric-value'>${ops_total.get('output', 0):,.0f}</span></div>")
    html_sections.append("</div>")
    
    # CRA Increment Table
    cra_projection = report_data.get('cra_increment_projection', [])
    if cra_projection:
        html_sections.append("<h2>Fiscal Impact: CRA Tax Increment</h2>")
        html_sections.append("<table>")
        html_sections.append("<tr><th>Year</th><th>Taxable Value</th><th>CRA Increment</th><th>Cumulative</th></tr>")
        for row in cra_projection:
            html_sections.append("<tr>")
            html_sections.append(f"<td>{row.get('year', '')}</td>")
            html_sections.append(f"<td>${row.get('taxable_value', 0):,.0f}</td>")
            html_sections.append(f"<td>${row.get('cra_increment', 0):,.0f}</td>")
            html_sections.append(f"<td>${row.get('cumulative', 0):,.0f}</td>")
            html_sections.append("</tr>")
        html_sections.append("</table>")
    
    # Construction Impact
    construction = report_data.get('construction_impact', {})
    html_sections.append("<h2>Construction Phase (One-Time)</h2>")
    if construction.get('narrative'):
        html_sections.append(f"<p>{construction.get('narrative', '')}</p>")
    if construction.get('table'):
        html_sections.append("<table>")
        html_sections.append("<tr><th>Impact Type</th><th>Output</th><th>Jobs</th><th>Labor Income</th></tr>")
        for row in construction.get('table', []):
            html_sections.append("<tr>")
            html_sections.append(f"<td>{row.get('impact_type', '')}</td>")
            html_sections.append(f"<td>${row.get('output', row.get('economic_output', 0)):,.0f}</td>")
            html_sections.append(f"<td>{row.get('jobs', 0):.1f}</td>")
            html_sections.append(f"<td>${row.get('labor_income', row.get('earnings', 0)):,.0f}</td>")
            html_sections.append("</tr>")
        html_sections.append("</table>")
    
    # Operations Impact
    html_sections.append("<h2>Operations Phase (Recurring Annual)</h2>")
    if operations.get('narrative'):
        html_sections.append(f"<p>{operations.get('narrative', '')}</p>")
    if operations.get('table'):
        html_sections.append("<table>")
        html_sections.append("<tr><th>Impact Type</th><th>Output</th><th>Jobs</th><th>Labor Income</th></tr>")
        for row in operations.get('table', []):
            html_sections.append("<tr>")
            html_sections.append(f"<td>{row.get('impact_type', '')}</td>")
            html_sections.append(f"<td>${row.get('output', row.get('economic_output', 0)):,.0f}</td>")
            html_sections.append(f"<td>{row.get('jobs', 0):.1f}</td>")
            html_sections.append(f"<td>${row.get('labor_income', row.get('earnings', 0)):,.0f}</td>")
            html_sections.append("</tr>")
        html_sections.append("</table>")
    
    # Ten-Year Operations Projection
    ten_year = report_data.get('ten_year_operations_projection', {})
    if ten_year.get('table'):
        html_sections.append("<h2>Ten-Year Operations Projection</h2>")
        html_sections.append("<table>")
        html_sections.append("<tr><th>Year</th><th>Annual Output</th><th>Jobs</th><th>Labor Income</th></tr>")
        for row in ten_year.get('table', []):
            html_sections.append("<tr>")
            html_sections.append(f"<td>{row.get('year', '')}</td>")
            html_sections.append(f"<td>${row.get('annual_output', 0):,.0f}</td>")
            html_sections.append(f"<td>{row.get('jobs', 0):.1f}</td>")
            html_sections.append(f"<td>${row.get('labor_income', 0):,.0f}</td>")
            html_sections.append("</tr>")
        html_sections.append("</table>")
    
    # Community Impacts
    community = report_data.get('community_impacts', [])
    if community:
        html_sections.append("<h2>Community and Qualitative Impacts</h2>")
        for impact in community:
            html_sections.append(f"<h3>{impact.get('category', '')}</h3>")
            html_sections.append(f"<p>{impact.get('description', '')}</p>")
    
    # Sources & Methodology
    html_sections.append("<h2>Sources & Methodology</h2>")
    html_sections.append("""
    <p><strong>Data Sources:</strong></p>
    <ul>
        <li><strong>Economic Multipliers:</strong> Lightcast 2025 data for Homestead/South Dade region</li>
        <li><strong>Demographics:</strong> Esri 2025 demographic profiles for Homestead, FL</li>
        <li><strong>Real Estate Data:</strong> CoStar 2025 market data for Homestead commercial properties</li>
        <li><strong>Fiscal Parameters:</strong> City of Homestead and Miami-Dade County FY 2025 millage rates</li>
    </ul>
    <p><strong>Methodology:</strong> This analysis uses economic modeling based on the EMSI Type II methodology, 
    capturing direct effects, indirect effects (supply chain), and induced effects (household spending).</p>
    """)
    
    # Join all sections
    content_html = "\n".join(html_sections)
    
    # Wrap in template with CSS
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Economic Impact Report - {project_name}</title>
        <style>
            @page {{
                size: Letter;
                margin: 0.75in;
                @bottom-right {{
                    content: "Page " counter(page) " of " counter(pages);
                    font-size: 9pt;
                    color: #666;
                }}
            }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                font-size: 10pt;
                line-height: 1.5;
                color: #333;
            }}
            
            h1 {{
                color: #1f4788;
                font-size: 22pt;
                margin-top: 0;
                border-bottom: 3px solid #1f4788;
                padding-bottom: 10px;
            }}
            
            h2 {{
                color: #1f4788;
                font-size: 14pt;
                margin-top: 25px;
                margin-bottom: 10px;
                border-bottom: 2px solid #ddd;
                padding-bottom: 5px;
            }}
            
            h3 {{
                color: #2c5aa0;
                font-size: 11pt;
                margin-top: 15px;
                margin-bottom: 8px;
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 15px 0;
                font-size: 9pt;
            }}
            
            th {{
                background-color: #1f4788;
                color: white;
                padding: 8px;
                text-align: left;
                font-weight: 600;
            }}
            
            td {{
                padding: 6px 8px;
                border-bottom: 1px solid #ddd;
            }}
            
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            
            p {{
                margin: 8px 0;
                text-align: justify;
            }}
            
            strong {{
                color: #1f4788;
            }}
            
            .metrics-grid {{
                display: flex;
                flex-wrap: wrap;
                gap: 15px;
                margin: 15px 0;
            }}
            
            .metric {{
                background: #f5f7fa;
                border-left: 4px solid #1f4788;
                padding: 10px 15px;
                flex: 1;
                min-width: 150px;
            }}
            
            .metric-label {{
                display: block;
                font-size: 9pt;
                color: #666;
                margin-bottom: 5px;
            }}
            
            .metric-value {{
                display: block;
                font-size: 14pt;
                font-weight: bold;
                color: #1f4788;
            }}
            
            ul {{
                margin: 10px 0;
                padding-left: 20px;
            }}
            
            li {{
                margin: 5px 0;
            }}
            
            .footer {{
                margin-top: 30px;
                padding-top: 15px;
                border-top: 2px solid #ddd;
                font-size: 8pt;
                color: #666;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <h1>Economic Impact Report</h1>
        <p style="font-size: 12pt; color: #1f4788; margin-bottom: 20px;"><strong>{project_name}</strong></p>
        {content_html}
        <div class="footer">
            <p>Powered by Street Economics | BusinessFlare® Analytics</p>
            <p>Homestead Community Redevelopment Agency</p>
        </div>
    </body>
    </html>
    """
    
    # Generate PDF
    font_config = FontConfiguration()
    html = HTML(string=html_template)
    pdf_bytes = html.write_pdf(font_config=font_config)
    
    if pdf_bytes is None:
        raise ValueError("PDF generation failed - no bytes returned")
    
    return pdf_bytes


def generate_pdf_from_markdown(markdown_text: str, title: str = "Economic Impact Report") -> bytes:
    """
    Legacy function - converts markdown text to PDF
    Kept for backwards compatibility
    """
    import markdown
    html_content = markdown.markdown(markdown_text, extensions=['tables', 'nl2br'])
    
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        <style>
            @page {{ size: Letter; margin: 1in; }}
            body {{ font-family: Arial, sans-serif; font-size: 11pt; line-height: 1.6; color: #333; }}
            h1 {{ color: #1f4788; font-size: 24pt; border-bottom: 3px solid #1f4788; padding-bottom: 10px; }}
            h2 {{ color: #1f4788; font-size: 18pt; margin-top: 30px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th {{ background-color: #1f4788; color: white; padding: 10px; text-align: left; }}
            td {{ padding: 8px; border-bottom: 1px solid #ddd; }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        {html_content}
    </body>
    </html>
    """
    
    font_config = FontConfiguration()
    html = HTML(string=html_template)
    pdf_bytes = html.write_pdf(font_config=font_config)
    if pdf_bytes is None:
        raise ValueError("PDF generation failed")
    return pdf_bytes
