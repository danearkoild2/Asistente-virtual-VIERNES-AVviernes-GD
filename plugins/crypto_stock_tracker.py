"""
Crypto & Stock Market Real-Time Price Checker for MARK LV / Viernes.
Fetches live asset prices via public CoinGecko & Yahoo Finance APIs.
"""
from __future__ import annotations
import urllib.request
import urllib.parse
import json

PLUGIN = {
    "name": "crypto_stock_tracker",
    "description": (
        "Checks real-time market prices for cryptocurrencies (Bitcoin, Ethereum, Solana...) "
        "and major stocks (Apple, Tesla, Nvidia, S&P 500...). "
        "Use when user asks 'cuánto vale bitcoin', 'precio de ethereum', 'cómo está tesla', "
        "or 'stock price of nvidia'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "asset": {
                "type": "STRING",
                "description": "The symbol or name of the coin or stock (e.g. 'bitcoin', 'btc', 'eth', 'tesla', 'nvda', 'aapl').",
            }
        },
        "required": ["asset"],
    },
}

COIN_MAP = {
    "btc": "bitcoin",
    "bitcoin": "bitcoin",
    "eth": "ethereum",
    "ethereum": "ethereum",
    "sol": "solana",
    "solana": "solana",
    "doge": "dogecoin",
    "dogecoin": "dogecoin",
    "xrp": "ripple",
    "cardano": "cardano",
    "ada": "cardano",
}

def run(parameters: dict, player=None, session_memory=None) -> str:
    raw_asset = parameters.get("asset", "bitcoin").strip().lower()
    coin_id = COIN_MAP.get(raw_asset)

    # 1. Try CoinGecko for cryptos
    if coin_id or raw_asset in ("crypto", "cripto"):
        target_coin = coin_id or "bitcoin"
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={target_coin}&vs_currencies=usd&include_24hr_change=true"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if target_coin in data:
                    usd = data[target_coin]["usd"]
                    change = data[target_coin].get("usd_24h_change", 0.0)
                    sign = "+" if change >= 0 else ""
                    msg = f"El precio actual de {target_coin.capitalize()} es de ${usd:,.2f} dólares ({sign}{change:.2f}% en 24h)."
                    if player: player.write_log(f"SYS: [Crypto] {msg}")
                    return msg
        except Exception:
            pass

    # 2. Try Yahoo Finance free quote endpoint for stocks
    stock_ticker = raw_asset.upper().replace("TESLA", "TSLA").replace("APPLE", "AAPL").replace("NVIDIA", "NVDA")
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(stock_ticker)}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            meta = data["chart"]["result"][0]["meta"]
            price = meta.get("regularMarketPrice") or meta.get("chartPreviousClose")
            currency = meta.get("currency", "USD")
            msg = f"La cotización de {stock_ticker} es de {price:.2f} {currency}."
            if player: player.write_log(f"SYS: [Market] {msg}")
            return msg
    except Exception as e:
        msg = f"No pude consultar la cotización de '{raw_asset}': {e}"

    if player:
        try: player.write_log(f"SYS: {msg}")
        except Exception: pass
    return msg
