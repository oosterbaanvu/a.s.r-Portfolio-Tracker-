import pandas as pd
import matplotlib.pyplot as plt
from rich.table import Table
from rich.console import Console
from rich.panel import Panel

def display_message(message: str):
    print(f"✅ {message}")

def display_error(message: str):
    print(f"❌ {message}")

def display_portfolio(portfolio_data: list):
    # ... (This function remains the same as before, no changes needed) ...
    if not portfolio_data:
        display_message("Your portfolio is empty."); return
    table = Table(title="Investment Portfolio")
    headers = ["Ticker", "Sector", "Asset Class", "Qty", "Purchase Price", "Txn Value", "Current Price", "Current Value"]
    for header in headers: table.add_column(header, justify="right")
    for asset in portfolio_data:
        table.add_row(asset["ticker"], asset["sector"], asset["asset_class"], f'{asset["quantity"]:.2f}',
                      f'${asset["purchase_price"]:.2f}', f'${asset["transaction_value"]:.2f}',
                      f'${asset["current_price"]:.2f}', f'${asset["current_value"]:.2f}')
    Console().print(table)

def display_portfolio_analysis(analysis_data: dict):
    # ... (This function remains the same as before, no changes needed) ...
    if not analysis_data:
        display_error("Could not generate portfolio analysis."); return
    console = Console()
    total_value_panel = Panel(f"[bold green]${analysis_data['total_value']:,.2f}[/bold green]", title="Total Portfolio Value", expand=False)
    console.print(total_value_panel)
    asset_table = Table(title="Asset Weights"); asset_table.add_column("Ticker", style="cyan"); asset_table.add_column("Weight", justify="right")
    for item in analysis_data['asset_weights']: asset_table.add_row(item['ticker'], f"{item['weight']:.2%}")
    sector_table = Table(title="Sector Weights"); sector_table.add_column("Sector", style="magenta"); sector_table.add_column("Weight", justify="right")
    for sector, weight in analysis_data['sector_weights'].items(): sector_table.add_row(sector, f"{weight:.2%}")
    class_table = Table(title="Asset Class Weights"); class_table.add_column("Asset Class", style="yellow"); class_table.add_column("Weight", justify="right")
    for asset_class, weight in analysis_data['class_weights'].items(): class_table.add_row(asset_class, f"{weight:.2%}")
    console.print(asset_table, sector_table, class_table)

def create_price_graph(data, ticker: str):
    # ... (This function remains the same as before, no changes needed) ...
    if data is None or data.empty:
        display_error(f"No data available to graph for {ticker}."); return
    data.index = data.index.to_timestamp()
    plt.figure(figsize=(10, 5)); plt.plot(data.index, data['Close']); plt.title(f"{ticker} Historical Price")
    plt.xlabel("Date"); plt.ylabel("Price (USD)"); plt.grid(True)
    filename = f"{ticker}_price_chart.png"
    plt.savefig(filename)
    display_message(f"Graph saved as {filename}")

def display_simulation_results(results: dict):
    """Displays the simulation results in a formatted table."""
    if not results:
        display_error("Could not run simulation.")
        return

    table = Table(title=f"Portfolio Simulation Results (15 Years, 100,000 Paths)")
    table.add_column("Statistic", style="cyan")
    table.add_column("Value", justify="right")
    
    table.add_row("Initial Value", f"${results['initial_value']:,.2f}")
    table.add_row("Mean (Average) Final Value", f"${results['mean']:,.2f}")
    table.add_row("Median (50th Percentile) Final Value", f"${results['median']:,.2f}")
    table.add_row("5th Percentile", f"${results['5th_percentile']:,.2f}")
    table.add_row("95th Percentile", f"${results['95th_percentile']:,.2f}")

    console = Console()
    console.print(table)
    console.print(f"There is a 90% probability that the portfolio value will be between "
                  f"[bold green]${results['5th_percentile']:,.2f}[/bold green] and "
                  f"[bold green]${results['95th_percentile']:,.2f}[/bold green] in 15 years.")