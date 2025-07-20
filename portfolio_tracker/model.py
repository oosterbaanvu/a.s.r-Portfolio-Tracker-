# portfolio_tracker/model.py

# Add pandas to your imports
import dataclasses
import pandas as pd
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
        self.api_key = api_key

    def add_asset(self, asset: Asset):
        self.assets.append(asset)

    def get_enriched_portfolio_data(self):
        if not self.assets:
            return []

        tickers = [asset.ticker for asset in self.assets]
        
        try:
            companies = Toolkit(tickers=tickers, api_key=self.api_key)
            prices_df = companies.get_quote()
        except Exception as e:
            print(f"❌ Failed to fetch prices: {e}")
            return []

        # It seems the toolkit returns tickers as columns, so we transpose
        prices_df = prices_df.transpose()

        enriched_assets = []
        # Using 'Previous Close' as it appears to be a reliable field from your debug output
        price_column = 'Previous Close' 
        
        for asset in self.assets:
            if asset.ticker in prices_df.index and price_column in prices_df.columns:
                current_price = prices_df.loc[asset.ticker, price_column]
                enriched_assets.append({
                    "ticker": asset.ticker, "sector": asset.sector, "asset_class": asset.asset_class,
                    "quantity": asset.quantity, "purchase_price": asset.purchase_price,
                    "transaction_value": asset.quantity * asset.purchase_price,
                    "current_price": current_price, "current_value": asset.quantity * current_price,
                })
        return enriched_assets
    
    # --- NEW METHOD ---
    def get_portfolio_analysis(self):
        """Calculates total value and weights for assets, sectors, and classes."""
        enriched_data = self.get_enriched_portfolio_data()
        if not enriched_data:
            return None
        
        df = pd.DataFrame(enriched_data)
        total_portfolio_value = df['current_value'].sum()
        
        if total_portfolio_value == 0:
            return None
        
        # Calculate weights for each individual asset
        df['weight'] = df['current_value'] / total_portfolio_value
        
        # Calculate weights grouped by sector
        sector_weights = df.groupby('sector')['current_value'].sum() / total_portfolio_value
        
        # Calculate weights grouped by asset class
        class_weights = df.groupby('asset_class')['current_value'].sum() / total_portfolio_value
        
        return {
            "total_value": total_portfolio_value,
            "asset_weights": df[['ticker', 'weight']].to_dict('records'),
            "sector_weights": sector_weights.to_dict(),
            "class_weights": class_weights.to_dict()
        }