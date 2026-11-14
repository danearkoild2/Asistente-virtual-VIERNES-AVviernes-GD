import sys

mods = ['requests', 'httpx', 'bs4', 'playwright', 'duckduckgo_search', 'urllib3', 'google_search_results', 'serpapi']
for m in mods:
    try:
        __import__(m)
        print(f"{m}: AVAILABLE")
    except ImportError:
        print(f"{m}: NOT INSTALLED")
sys.exit(0)
