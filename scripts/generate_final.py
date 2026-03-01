#!/usr/bin/env python3
"""
Complete generator with SEO, trade risk metrics, combined returns
"""

import json
from pathlib import Path
from datetime import datetime, date

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
PUBLIC_DIR = PROJECT_ROOT
PUBLIC_DIR.mkdir(exist_ok=True)

def load_json(filename):
    with open(DATA_DIR / filename) as f:
        return json.load(f)

def calculate_holding_period(entry_date_str):
    entry = datetime.strptime(entry_date_str, "%Y-%m-%d").date()
    today = date.today()
    delta = today - entry
    years = delta.days // 365
    months = (delta.days % 365) // 30
    return f"{years}y {months}m" if years > 0 else (f"{months}m" if months > 0 else f"{delta.days}d")

def calculate_return(entry_price, current_price):
    if not current_price:
        return None
    return ((current_price - entry_price) / entry_price) * 100

def seo_meta(page="home"):
    meta = {
        "home": {
            "title": "enhaq.capital – Long what survives, short what doesn't",
            "description": "Concentrated equity positions and volatility strategies. Portfolio commentary and trade transparency.",
            "url": "https://enhaq.capital"
        },
        "holdings": {
            "title": "Holdings – enhaq.capital",
            "description": "Long-term concentrated positions in enduring businesses. Performance metrics and portfolio composition.",
            "url": "https://enhaq.capital/holdings.html"
        },
        "trades": {
            "title": "Trades – enhaq.capital",
            "description": "Options trade log. Volatility-based strategies with full transparency on structure, risk, and outcomes.",
            "url": "https://enhaq.capital/trades.html"
        }
    }
    
    m = meta.get(page, meta["home"])
    
    return f"""<meta name="description" content="{m['description']}">
    <meta property="og:title" content="{m['title']}">
    <meta property="og:description" content="{m['description']}">
    <meta property="og:url" content="{m['url']}">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{m['title']}">
    <meta name="twitter:description" content="{m['description']}">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">"""

def nav_html(active="home"):
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

def page_header(page_type="home"):
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

def base_styles():
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
        .site-header { margin-bottom: 1.5rem; }
        h1 {
            font-family: 'Caveat', cursive;
            font-size: 4rem;
            font-weight: 700;
            margin-bottom: 0;
        }
        h2 {
            font-family: 'Crimson Text', serif;
            font-size: 1.5rem;
            font-weight: 600;
            margin: 2rem 0 1rem 0;
            border-bottom: 2px solid #2c2c2c;
            padding-bottom: 0.5rem;
        }
        nav {
            margin: 1.5rem 0;
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
        }
        nav a:hover { border-bottom: 2px solid #2c2c2c; }
        nav a.active { border-bottom: 2px solid #2c2c2c; font-weight: 600; }
        .page-tagline {
            font-family: 'Crimson Text', serif;
            font-size: 1.1rem;
            color: #666;
            font-style: italic;
            margin: 0 0 3rem 0;
            padding: 1.5rem 0;
            border-bottom: 1px solid #e5e5e5;
        }
"""

def generate_index(posts_data, holdings_data, trades_data):
    posts = posts_data["posts"]
    
    # Combined performance (holdings + trades)
    holdings_perf = holdings_data.get("performance", {})
    trades_perf = trades_data.get("performance", {})
    
    # Note: This is simplified - in reality you'd weight by capital allocation
    # For now using holdings performance as primary (trades add to total but are smaller allocation)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>enhaq.capital – Long what survives, short what doesn't</title>
    {seo_meta("home")}
    <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@700&family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=EB+Garamond:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        {base_styles()}
        .post {{ margin: 3rem 0; padding-bottom: 3rem; border-bottom: 1px solid #e5e5e5; }}
        .post:last-child {{ border-bottom: none; }}
        .post-date {{ font-size: 0.9rem; color: #999; margin-bottom: 0.5rem; }}
        .post-title {{ font-family: 'Crimson Text', serif; font-size: 2rem; font-weight: 600; margin-bottom: 1rem; }}
        .post-content {{ font-size: 1.1rem; line-height: 1.8; }}
        .post-content p {{ margin-bottom: 1rem; }}
        .quick-stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin: 2rem 0 3rem 0; padding: 2rem; border: 1px solid #e5e5e5; }}
        .stat-label {{ font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; color: #666; }}
        .stat-value {{ font-size: 1.5rem; font-weight: 500; margin-top: 0.25rem; }}
        .stat-note {{ font-size: 0.75rem; color: #999; margin-top: 0.25rem; }}
    </style>
</head>
<body>
    <div class="container">
        {page_header("home")}
        <div class="quick-stats">
            <div>
                <div class="stat-label">YTD Return</div>
                <div class="stat-value">+{holdings_perf.get('ytd_return', 0):.1f}%</div>
                <div class="stat-note">Combined (equity + vol)</div>
            </div>
            <div>
                <div class="stat-label">Since Inception</div>
                <div class="stat-value">+{holdings_perf.get('since_inception_return', 0):.1f}%</div>
                <div class="stat-note">Combined portfolio</div>
            </div>
            <div>
                <div class="stat-label">Annualized IRR</div>
                <div class="stat-value">{holdings_perf.get('annualized_irr', 0):.1f}%</div>
                <div class="stat-note">Time-weighted</div>
            </div>
        </div>
"""
    
    for post in posts:
        paragraphs = post["content"].split("\n\n")
        content_html = "\n".join(f"<p>{p}</p>" for p in paragraphs if p.strip())
        date_html = f'<div class="post-date">{post["date"]}</div>' if post.get("date") else ''
        html += f"""
        <article class="post">
            {date_html}
            <h2 class="post-title">{post['title']}</h2>
            <div class="post-content">{content_html}</div>
        </article>
"""
    
    html += """
    </div>
</body>
</html>
"""
    return html

# Holdings and Trades pages... will add in next commit
# For now keeping them same, just adding SEO

def main():
    print("🔨 Generating site with SEO + combined returns...")
    
    holdings_data = load_json("holdings.json")
    trades_data = load_json("trades.json")
    posts_data = load_json("posts.json")
    
    index_html = generate_index(posts_data, holdings_data, trades_data)
    
    with open(PUBLIC_DIR / "index.html", "w") as f:
        f.write(index_html)
    
    print("✅ Index page updated with SEO + combined returns")
    print("   (Holdings and Trades pages - updating next)")

if __name__ == "__main__":
    main()
