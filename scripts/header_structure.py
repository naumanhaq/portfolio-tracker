# New header structure for all pages

def page_header(page_type="home"):
    """
    Consistent header + nav + page tagline
    """
    
    taglines = {
        "home": "Long what survives, short what doesn't.",
        "holdings": "Concentrated positions in enduring businesses.",
        "trades": "Volatility trades. Short duration, asymmetric payoff."
    }
    
    return f"""
        <header class="site-header">
            <h1>enhaq.capital</h1>
        </header>
        
        {nav_html(page_type)}
        
        <div class="page-tagline">
            {taglines.get(page_type, "")}
        </div>
"""

# CSS additions for new structure:
header_css = """
        .site-header {
            margin-bottom: 1.5rem;
        }
        
        .page-tagline {
            font-family: 'Crimson Text', serif;
            font-size: 1.1rem;
            color: #666;
            font-style: italic;
            margin: 1.5rem 0 3rem 0;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid #e5e5e5;
        }
"""
