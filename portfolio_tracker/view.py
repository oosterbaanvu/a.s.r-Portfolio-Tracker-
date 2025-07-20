# portfolio_tracker/view.py
from rich.table import Table
from rich.console import Console

def display_message(message: str):
    print(f"✅ {message}")

def display_error(message: str):
    print(f"❌ {message}")

def display_portfolio(portfolio_data: list):
    """Displays the portfolio data in a formatted table."""
    if not portfolio_data:
        display_message("Your portfolio is empty.")
        return

    table = Table(title="Investment Portfolio")
    
    # Define table headers
    headers = [
        "Ticker", "Sector", "Asset Class", "Qty", 
        "Purchase Price", "Txn Value", "Current Price", "Current Value"
    ]
    for header in headers:
        table.add_column(header, justify="right")

    # Add rows from your portfolio data
    for asset in portfolio_data:
        table.add_row(
            asset["ticker"],
            asset["sector"],
            asset["asset_class"],
            f'{asset["quantity"]:.2f}',
            f'${asset["purchase_price"]:.2f}',
            f'${asset["transaction_value"]:.2f}',
            f'${asset["current_price"]:.2f}',
            f'${asset["current_value"]:.2f}',
        )

    console = Console()
    console.print(table)