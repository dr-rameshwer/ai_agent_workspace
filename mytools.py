from langchain_core.tools import tool

# Tool 1: Mathematical Calculation Tool
@tool
def multiply(a: float, b: float) -> float:
    """Multiplies two numbers together and returns the exact mathematical product.
    
    Args:
        a: The first number.
        b: The second number.
    """
    return a * b

# Tool 2: External Knowledge / Mock Database Tool
@tool
def get_stock_price(ticker: str) -> str:
    """Fetches the latest mock stock price for a given stock ticker symbol.
    
    Args:
        ticker: The stock ticker symbol (e.g. AAPL, GOOG, TSLA, MSFT).
    """
    mock_database = {
        "AAPL": "$225.50",
        "GOOG": "$178.20",
        "TSLA": "$245.80",
        "MSFT": "$410.00"
    }
    key = ticker.upper().strip()
    return mock_database.get(key, f"Error: Ticker symbol '{ticker}' not found in database.")
if __name__ == "__main__":
    print("=" * 60)
    print("TOOL 1 METADATA & SCHEMA INSPECTION")
    print("=" * 60)
    print("Name:       ", multiply.name)
    print("Description:", multiply.description)
    print("Arguments:  ", multiply.args)

    print("\n" + "=" * 60)
    print("DIRECT LOCAL INVOCATION TEST")
    print("=" * 60)
    # Direct Python test using .invoke() with an argument dictionary
    result = multiply.invoke({"a": 12.5, "b": 4})
    print(f"multiply.invoke({{'a': 12.5, 'b': 4}}) => {result}")

