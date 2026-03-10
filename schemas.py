TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_exchange_rate",
            "description": "Get the exchange rate for a given currency pair.",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "currency_pair": {
                        "type": "string",
                        "description": "The currency pair to query, such as USD_TWD, JPY_TWD, or EUR_USD."
                    }
                },
                "required": ["currency_pair"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Get the stock price for a given stock symbol.",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "The stock symbol to query, such as AAPL, TSLA, or NVDA."
                    }
                },
                "required": ["symbol"],
                "additionalProperties": False
            }
        }
    }
]