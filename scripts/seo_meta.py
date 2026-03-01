# SEO meta tags helper

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
    
    return f"""
    <meta name="description" content="{m['description']}">
    <meta property="og:title" content="{m['title']}">
    <meta property="og:description" content="{m['description']}">
    <meta property="og:url" content="{m['url']}">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{m['title']}">
    <meta name="twitter:description" content="{m['description']}">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
"""
