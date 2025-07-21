from . import model
from . import view

class Controller:
    def __init__(self, portfolio: model.Portfolio):
        self.portfolio = portfolio
        self.portfolio_filepath = "my_portfolio.json"
        self.portfolio.load_from_file(self.portfolio_filepath)

    def add_asset(self, ticker, sector, asset_class, quantity_str, price_str):
        try:
            asset = model.Asset(
                ticker=ticker.upper(),
                sector=sector,
                asset_class=asset_class,
                quantity=float(quantity_str),
                purchase_price=float(price_str)
            )
            self.portfolio.add_asset(asset)
            self.portfolio.save_to_file(self.portfolio_filepath)
            view.display_message(f"Added {asset.quantity} of {asset.ticker} to portfolio.")
        except ValueError:
            view.display_error("Invalid quantity or price. Please enter numbers.")
        except Exception as e:
            view.display_error(f"An error occurred: {e}")

    def show_portfolio(self):
        portfolio_data = self.portfolio.get_enriched_portfolio_data()
        view.display_portfolio(portfolio_data)

    def show_analysis(self):
        analysis_data = self.portfolio.get_portfolio_analysis()
        view.display_portfolio_analysis(analysis_data)
        
    def create_graph_for_ticker(self, tickers: list):
        # If the user provided no tickers, get them all from the portfolio
        if not tickers:
            tickers = self.portfolio.get_all_tickers()
            if not tickers:
                view.display_error("Your portfolio is empty. Add assets before creating a graph.")
                return

        # Remove duplicate tickers to prevent plotting the same line twice
        unique_tickers = sorted(list(set(tickers)))
        
        historical_data = self.portfolio.get_historical_data(unique_tickers)
        view.create_price_graph(historical_data, unique_tickers)
        
    def run_and_show_simulation(self):
        results = self.portfolio.run_simulation()
        view.display_simulation_results(results)