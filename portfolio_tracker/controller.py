# portfolio_tracker/controller.py
from . import model
from . import view

class Controller:
    def __init__(self, portfolio: model.Portfolio):
        self.portfolio = portfolio

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
            view.display_message(f"Added {asset.quantity} of {asset.ticker} to portfolio.")
        except ValueError:
            view.display_error("Invalid quantity or price. Please enter numbers.")
        except Exception as e:
            view.display_error(f"An error occurred: {e}")

    def show_portfolio(self):
        """Gets enriched data from the model and tells the view to display it."""
        portfolio_data = self.portfolio.get_enriched_portfolio_data()
        view.display_portfolio(portfolio_data)