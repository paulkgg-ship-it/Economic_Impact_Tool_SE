from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import tempfile
import os

def generate_pdf_from_markdown(markdown_text: str, title: str = "Economic Impact Report") -> bytes:
    """
    Converts markdown text to a professional PDF
    
    Args:
        markdown_text: The markdown-formatted report
        title: Title for the PDF document
    
    Returns:
        PDF file as bytes
    """
    # Convert markdown to HTML
    import markdown
    html_content = markdown.markdown(markdown_text, extensions=['tables', 'nl2br'])
    
    # Wrap in professional HTML template
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        <style>
            @page {{
                size: Letter;
                margin: 1in;
                @bottom-right {{
                    content: "Page " counter(page) " of " counter(pages);
                    font-size: 9pt;
                    color: #666;
                }}
            }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                font-size: 11pt;
                line-height: 1.6;
                color: #333;
            }}
            
            h1 {{
                color: #1f4788;
                font-size: 24pt;
                margin-top: 0;
                border-bottom: 3px solid #1f4788;
                padding-bottom: 10px;
            }}
            
            h2 {{
                color: #1f4788;
                font-size: 18pt;
                margin-top: 30px;
                margin-bottom: 15px;
                border-bottom: 2px solid #ddd;
                padding-bottom: 5px;
            }}
            
            h3 {{
                color: #2c5aa0;
                font-size: 14pt;
                margin-top: 20px;
                margin-bottom: 10px;
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                font-size: 10pt;
            }}
            
            th {{
                background-color: #1f4788;
                color: white;
                padding: 10px;
                text-align: left;
                font-weight: 600;
            }}
            
            td {{
                padding: 8px;
                border-bottom: 1px solid #ddd;
            }}
            
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            
            p {{
                margin: 10px 0;
                text-align: justify;
            }}
            
            strong {{
                color: #1f4788;
            }}
            
            .footer {{
                margin-top: 40px;
                padding-top: 20px;
                border-top: 2px solid #ddd;
                font-size: 9pt;
                color: #666;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        {html_content}
        <div class="footer">
            <p>Powered by Street Economics | BusinessFlare® Analytics</p>
            <p>Generated {title} | Homestead Community Redevelopment Agency</p>
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
