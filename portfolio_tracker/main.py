# main.py
from portfolio_tracker.model import Portfolio
from portfolio_tracker.controller import Controller

def main():
    FMP_API_KEY = "b2kyxgJgXLcvJjWUDz5SsNkel1A1GuJU"



    # Pass the API key when creating the portfolio
    portfolio = Portfolio(api_key=FMP_API_KEY)
    controller = Controller(portfolio)

    # Add some assets
    controller.add_asset("AAPL", "Technology", "Stock", "10", "150.25")
    controller.add_asset("MSFT", "Technology", "Stock", "5", "300.50")
    
    # --- New functionality ---
    # Show the portfolio with live data
    print("\nFetching live data and displaying portfolio...")
    controller.show_portfolio()


if __name__ == "__main__":
    main()