import json


EXCHANGE_RATES = {
    "USD_TWD": "32.0",
    "JPY_TWD": "0.2",
    "EUR_USD": "1.2",
}

STOCK_PRICES = {
    "AAPL": "260.00",
    "TSLA": "430.00",
    "NVDA": "190.00",
}


def get_exchange_rate(currency_pair: str) -> str:
    """
    Return a JSON string containing the exchange rate for the given currency pair.
    If the currency pair is not found, return a JSON string with an error message.
    """
    normalized_pair = currency_pair.strip().upper()

    if normalized_pair not in EXCHANGE_RATES:
        return json.dumps({"error": "Data not found"})

    return json.dumps({
        "currency_pair": normalized_pair,
        "rate": EXCHANGE_RATES[normalized_pair]
    })


def get_stock_price(symbol: str) -> str:
    """
    Return a JSON string containing the stock price for the given symbol.
    If the symbol is not found, return a JSON string with an error message.
    """
    normalized_symbol = symbol.strip().upper()

    if normalized_symbol not in STOCK_PRICES:
        return json.dumps({"error": "Data not found"})

    return json.dumps({
        "symbol": normalized_symbol,
        "price": STOCK_PRICES[normalized_symbol]
    })