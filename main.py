import argparse
from portfolio_tracker.model import Portfolio
from portfolio_tracker.controller import Controller

def main():
    FMP_API_KEY = "b2kyxgJgXLcvJjWUDz5SsNkel1A1GuJU"
    
    portfolio = Portfolio(api_key=FMP_API_KEY)
    controller = Controller(portfolio)

    # Set up the final command-line interface
    parser = argparse.ArgumentParser(description="Investment Portfolio Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)

    # Command: add
    add_parser = subparsers.add_parser("add", help="Add an asset to the portfolio.")
    add_parser.add_argument("ticker", type=str, help="e.g., AAPL")
    add_parser.add_argument("sector", type=str, help="e.g., Technology")
    add_parser.add_argument("asset_class", type=str, help="e.g., Stock")
    add_parser.add_argument("quantity", type=str, help="e.g., 10")
    add_parser.add_argument("price", type=str, help="e.g., 150.25")

    # Command: show
    subparsers.add_parser("show", help="Display the portfolio.")
    
    # Command: analyze
    subparsers.add_parser("analyze", help="Analyze the portfolio.")

    # Command: graph
    graph_parser = subparsers.add_parser("graph", help="Graph historical price for a ticker.")
    graph_parser.add_argument("ticker", type=str, help="The stock ticker to graph (e.g., AAPL).")

    # Command: simulate
    subparsers.add_parser("simulate", help="Run the 15-year portfolio simulation.")
    
    args = parser.parse_args()

    # Execute the appropriate command based on user input
    if args.command == "add":
        controller.add_asset(args.ticker, args.sector, args.asset_class, args.quantity, args.price)
    elif args.command == "show":
        controller.show_portfolio()
    elif args.command == "analyze":
        controller.show_analysis()
    elif args.command == "graph":
        controller.create_graph_for_ticker(args.ticker)
    elif args.command == "simulate":
        controller.run_and_show_simulation()

if __name__ == "__main__":
    main()