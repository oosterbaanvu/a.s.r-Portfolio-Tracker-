# portfolio_tracker/view.py
from rich.table import Table
from rich.console import Console
from rich.panel import Panel

def display_message(message: str):
    print(f"✅ {message}")

def display_error(message: str):
    print(f"❌ {message}")

def display_portfolio(portfolio_data: list):
    # ... (This function remains the same as before, no need to copy it again) ...
    if not portfolio_data:
        display_message("Your portfolio is empty.")
        return

    table = Table(title="Investment Portfolio")
    
    headers = ["Ticker", "Sector", "Asset Class", "Qty", "Purchase Price", "Txn Value", "Current Price", "Current Value"]
    for header in headers:
        table.add_column(header, justify="right")

    for asset in portfolio_data:
        table.add_row(
            asset["ticker"], asset["sector"], asset["asset_class"],
            f'{asset["quantity"]:.2f}', f'${asset["purchase_price"]:.2f}',
            f'${asset["transaction_value"]:.2f}', f'${asset["current_price"]:.2f}', f'${asset["current_value"]:.2f}',
        )

    console = Console()
    console.print(table)

# --- NEW FUNCTION ---
def display_portfolio_analysis(analysis_data: dict):
    """Displays the portfolio analysis in a series of tables."""
    if not analysis_data:
        display_error("Could not generate portfolio analysis.")
        return
        
    console = Console()
    
    # Display Total Value
    total_value_panel = Panel(
        f"[bold green]${analysis_data['total_value']:,.2f}[/bold green]",
        title="Total Portfolio Value",
        expand=False
    )
    console.print(total_value_panel)

    # Display Asset Weights
    asset_table = Table(title="Asset Weights")
    asset_table.add_column("Ticker", style="cyan")
    asset_table.add_column("Weight", justify="right")

    for item in analysis_data['asset_weights']:
        asset_table.add_row(item['ticker'], f"{item['weight']:.2%}")
    
    # Display Sector Weights
    sector_table = Table(title="Sector Weights")
    sector_table.add_column("Sector", style="magenta")
    sector_table.add_column("Weight", justify="right")
    
    for sector, weight in analysis_data['sector_weights'].items():
        sector_table.add_row(sector, f"{weight:.2%}")
        
    # Display Class Weights
    class_table = Table(title="Asset Class Weights")
    class_table.add_column("Asset Class", style="yellow")
    class_table.add_column("Weight", justify="right")
    
    for asset_class, weight in analysis_data['class_weights'].items():
        class_table.add_row(asset_class, f"{weight:.2%}")
    
    console.print(asset_table, sector_table, class_table)