import markdown
import os

os.add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64\bin")

from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

def convert_markdown_to_pdf(md_file, output_file=None, title=None, 
                           font_size=12, font_family='Roboto', 
                           margin_top=2, margin_bottom=2, 
                           margin_left=2, margin_right=2,
                           page_width=8.27, page_height=11.7,
                           header=None, footer=None,
                           css_file=None):
    """
    Convert a markdown file to PDF with customizable options.
    
    Args:
        md_file (str): Path to the markdown file
        output_file (str, optional): Path for the output PDF file. If None, uses the same name as md_file with .pdf extension
        title (str, optional): Title for the document
        font_size (int, optional): Base font size in points
        font_family (str, optional): Font family to use
        margin_top, margin_bottom, margin_left, margin_right (float, optional): Margins in inches
        page_width, page_height (float, optional): Page dimensions in inches
        header (str, optional): Text for the header
        footer (str, optional): Text for the footer
        css_file (str, optional): Path to a custom CSS file
    """
    # Set default output file if not provided
    if not output_file:
        output_file = os.path.splitext(md_file)[0] + '.pdf'
        
    # Read markdown content
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown.markdown(md_content, extensions=['extra', 'codehilite', 'tables'])
    
    # Create document title if provided
    title_html = f"<h1 class='document-title'>{title}</h1>" if title else ""
    
    # Create header and footer if provided
    header_html = f"<div class='header'>{header}</div>" if header else ""
    footer_html = f"<div class='footer'>{footer}</div>" if footer else ""
    
    # Construct full HTML document
    html_document = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>{title if title else 'Markdown Document'}</title>
    </head>
    <body>
        {header_html}
        {title_html}
        {html_content}
        {footer_html}
    </body>
    </html>
    """
    
    # Base CSS with customizable properties
    base_css = CSS(string=f"""
        @page {{
            size: {page_width}in {page_height}in;
            margin-top: {margin_top}in;
            margin-bottom: {margin_bottom}in;
            margin-left: {margin_left}in;
            margin-right: {margin_right}in;
            @top-center {{
                content: "";
            }}
            @bottom-center {{
                content: counter(page);
            }}
        }}
        
        body {{
            font-family: {font_family}, sans-serif;
            font-size: {font_size}pt;
            line-height: 1.5;
        }}
        
        .document-title {{
            text-align: center;
            margin-bottom: 1.5em;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 1.5em;
            margin-bottom: 0.5em;
            font-weight: bold;
            page-break-after: avoid;
        }}
        
        h1 {{ font-size: {font_size * 1.8}pt; }}
        h2 {{ font-size: {font_size * 1.6}pt; }}
        h3 {{ font-size: {font_size * 1.4}pt; }}
        h4 {{ font-size: {font_size * 1.2}pt; }}
        
        p {{
            margin-top: 0.5em;
            margin-bottom: 0.75em;
        }}
        
        code {{
            font-family: monospace;
            background-color: #f5f5f5;
            padding: 0.2em 0.4em;
            border-radius: 3px;
        }}
        
        pre {{
            background-color: #f5f5f5;
            padding: 1em;
            overflow-x: auto;
            border-radius: 4px;
            page-break-inside: avoid;
        }}
        
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
            page-break-inside: avoid;
        }}
        
        th, td {{
            border: 1px solid #ddd;
            padding: 0.5em;
        }}
        
        th {{
            background-color: #f5f5f5;
            font-weight: bold;
        }}
        
        img {{
            max-width: 100%;
            height: auto;
        }}
        
        blockquote {{
            border-left: 4px solid #ddd;
            padding-left: 1em;
            margin-left: 0;
            color: #666;
        }}
        
        hr {{
            border: none;
            border-top: 1px solid #ddd;
            margin: 1.5em 0;
        }}
        
        .header {{
            position: running(header);
            text-align: center;
            font-size: {font_size * 0.9}pt;
            color: #666;
        }}
        
        .footer {{
            position: running(footer);
            text-align: center;
            font-size: {font_size * 0.9}pt;
            color: #666;
        }}
        
        @page {{
            @top-center {{ content: element(header) }}
            @bottom-center {{ content: element(footer), counter(page) }}
        }}
    """)
    
    css_files = [base_css]
    
    # Add custom CSS file if provided
    if css_file and os.path.exists(css_file):
        css_files.append(CSS(filename=css_file))
    
    # Configure fonts
    font_config = FontConfiguration()
    
    # Generate PDF
    HTML(string=html_document).write_pdf(
        output_file,
        stylesheets=css_files,
        font_config=font_config
    )
    
    return output_file