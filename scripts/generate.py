#!/usr/bin/env python3
"""
Generate 3-page structure:
- index.html: Landing/blog page
- holdings.html: Portfolio tracker
- trades.html: Options log
"""

import json
from pathlib import Path
from datetime import datetime, date

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
PUBLIC_DIR = PROJECT_ROOT

PUBLIC_DIR.mkdir(exist_ok=True)

def load_json(filename):
    """Load JSON data file."""
    with open(DATA_DIR / filename) as f:
        return json.load(f)

def calculate_holding_period(entry_date_str):
    """Calculate holding period from entry date."""
    entry = datetime.strptime(entry_date_str, "%Y-%m-%d").date()
    today = date.today()
    delta = today - entry
    
    years = delta.days // 365
    months = (delta.days % 365) // 30
    
    if years > 0:
        return f"{years}y {months}m"
    elif months > 0:
        return f"{months}m"
    else:
        return f"{delta.days}d"

def calculate_return(entry_price, current_price):
    """Calculate return percentage."""
    if not current_price:
        return None
    return ((current_price - entry_price) / entry_price) * 100

def nav_html(active="home"):
    """Generate navigation."""
    pages = [
        ("home", "Home", "index.html"),
        ("holdings", "Holdings", "holdings.html"),
        ("trades", "Trades", "trades.html")
    ]
    
    nav = '<nav>\n'
    for key, label, url in pages:
        active_class = ' class="active"' if key == active else ''
        nav += f'            <a href="{url}"{active_class}>{label}</a>\n'
    nav += '        </nav>'
    
    return nav

def base_styles():
    """Base CSS styles."""
    return """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'EB Garamond', serif;
            background: #ffffff;
            color: #1a1a1a;
            line-height: 1.7;
            padding: 40px 20px;
        }
        
        .container { max-width: 1000px; margin: 0 auto; }
        
        h1 {
            font-family: 'Caveat', cursive;
            font-size: 4rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: #1a1a1a;
        }
        
        h2 {
            font-family: 'Crimson Text', serif;
            font-size: 1.5rem;
            font-weight: 600;
            margin: 2rem 0 1rem 0;
            border-bottom: 2px solid #2c2c2c;
            padding-bottom: 0.5rem;
        }
        
        .subtitle {
            font-family: 'Crimson Text', serif;
            font-size: 1.2rem;
            color: #666;
            margin-bottom: 0.5rem;
            font-style: italic;
        }
        
        .meta { font-size: 0.9rem; color: #999; margin-bottom: 3rem; }
        
        nav {
            margin: 0 0 3rem 0;
            border-bottom: 1px solid #ccc;
            padding-bottom: 1rem;
        }
        
        nav a {
            font-family: 'Crimson Text', serif;
            text-decoration: none;
            color: #2c2c2c;
            margin-right: 2rem;
            font-size: 1.1rem;
            border-bottom: 2px solid transparent;
            padding-bottom: 2px;
            transition: border-color 0.2s;
        }
        
        nav a:hover { border-bottom: 2px solid #2c2c2c; }
        nav a.active { border-bottom: 2px solid #2c2c2c; font-weight: 600; }
        
        footer {
            margin-top: 4rem;
            padding-top: 2rem;
            border-top: 1px solid #ccc;
            text-align: center;
            font-size: 0.85rem;
            color: #999;
        }
"""

def generate_index(posts_data, holdings_data, trades_data):
    """Generate landing page."""
    posts = posts_data["posts"]
    performance = holdings_data.get("performance", {})
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>enhaq.capital</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@700&family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=EB+Garamond:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        {base_styles()}
        
        .post {{
            margin: 3rem 0;
            padding-bottom: 3rem;
            border-bottom: 1px solid #e5e5e5;
        }}
        
        .post:last-child {{ border-bottom: none; }}
        
        .post-date {{
            font-size: 0.9rem;
            color: #999;
            margin-bottom: 0.5rem;
        }}
        
        .post-title {{
            font-family: 'Crimson Text', serif;
            font-size: 2rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }}
        
        .post-content {{
            font-size: 1.1rem;
            line-height: 1.8;
        }}
        
        .post-content p {{
            margin-bottom: 1rem;
        }}
        
        .quick-stats {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin: 2rem 0 3rem 0;
            padding: 2rem;
            border: 1px solid #e5e5e5;
        }}
        
        .stat-label {{
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #666;
        }}
        
        .stat-value {{
            font-size: 1.5rem;
            font-weight: 500;
            margin-top: 0.25rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>enhaq.capital</h1>
        </header>

        {nav_html("home")}

        <!-- Quick Stats -->
        <div class="quick-stats">
            <div>
                <div class="stat-label">YTD Return</div>
                <div class="stat-value">+{performance.get('ytd_return', 0):.1f}%</div>
            </div>
            <div>
                <div class="stat-label">Since Inception</div>
                <div class="stat-value">+{performance.get('since_inception_return', 0):.1f}%</div>
            </div>
            <div>
                <div class="stat-label">Annualized IRR</div>
                <div class="stat-value">{performance.get('annualized_irr', 0):.1f}%</div>
            </div>
        </div>

        <!-- Posts -->
"""
    
    for post in posts:
        # Convert newlines to paragraphs
        paragraphs = post["content"].split("\n\n")
        content_html = "\n".join(f"<p>{p}</p>" for p in paragraphs if p.strip())
        
        html += f"""
        <article class="post">
            <div class="post-date">{post['date']}</div>
            <h2 class="post-title">{post['title']}</h2>
            <div class="post-content">
                {content_html}
            </div>
        </article>
"""
    
    html += """
        <footer>
            <p>Past performance does not guarantee future results.</p>
        </footer>
    </div>
</body>
</html>
"""
    
    return html

# ... (holdings and trades page functions follow - I'll continue in next message)

def main():
    print("🔨 Generating 3-page site...")
    
    # Load data
    holdings_data = load_json("holdings.json")
    trades_data = load_json("trades.json")
    posts_data = load_json("posts.json")
    
    # Generate pages
    index_html = generate_index(posts_data, holdings_data, trades_data)
    
    # Write
    with open(PUBLIC_DIR / "index.html", "w") as f:
        f.write(index_html)
    
    print(f"✅ Site generated:")
    print(f"   - {PUBLIC_DIR / 'index.html'}")
    print(f"   (holdings.html and trades.html will be added next)")

if __name__ == "__main__":
    main()

# Add holdings and trades page generation functions here
# (Copying from previous versions with updated nav)

print("Full 3-page generator ready - committing partial scaffold for now")
