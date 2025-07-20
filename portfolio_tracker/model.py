# portfolio_tracker/model.py
import dataclasses
from financetoolkit import Toolkit

@dataclasses.dataclass
class Asset:
    ticker: str
    sector: str
    asset_class: str
    quantity: float
    purchase_price: float

class Portfolio:
    def __init__(self, api_key: str):
        self.assets = []
        # Store the API key for later use
        self.api_key = api_key

    def add_asset(self, asset: Asset):
        self.assets.append(asset)

    def get_enriched_portfolio_data(self):
        """Fetches current prices and calculates values for all assets."""
        if not self.assets:
            return []

        tickers = [asset.ticker for asset in self.assets]
        
        # Initialize the toolkit with your tickers and API key
        companies = Toolkit(
            tickers=tickers,
            api_key=self.api_key,
        )
        
        # Get the real-time quotes for all assets at once
        prices = companies.get_quote()

        enriched_assets = []
        for asset in self.assets:
            # The toolkit returns a pandas DataFrame, so we access prices like this
            current_price = prices.loc[asset.ticker, 'Previous Close']
            
            enriched_data = {
                "ticker": asset.ticker,
                "sector": asset.sector,
                "asset_class": asset.asset_class,
                "quantity": asset.quantity,
                "purchase_price": asset.purchase_price,
                "transaction_value": asset.quantity * asset.purchase_price,
                "current_price": current_price,
                "current_value": asset.quantity * current_price,
            }
            enriched_assets.append(enriched_data)
            
        return enriched_assets