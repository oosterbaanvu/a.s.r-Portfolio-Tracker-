import dataclasses
import json
import pandas as pd
import numpy as np
from financetoolkit import Toolkit

@dataclasses.dataclass
class Asset:
    ticker: str
    sector: str
    asset_class: str
    quantity: float
    purchase_price: float

import dataclasses
import json
import pandas as pd
import numpy as np
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

    def save_to_file(self, filepath: str):
        """Saves the list of assets to a JSON file."""
        with open(filepath, 'w') as f:
            assets_as_dicts = [dataclasses.asdict(asset) for asset in self.assets]
            json.dump(assets_as_dicts, f, indent=4)
        
    def load_from_file(self, filepath: str):
        """Loads a list of assets from a JSON file."""
        try:
            with open(filepath, 'r') as f:
                assets_as_dicts = json.load(f)
                self.assets = [Asset(**data) for data in assets_as_dicts]
        except FileNotFoundError:
            self.assets = []
        except Exception as e:
            print(f"❌ Error loading portfolio: {e}")
            self.assets = []

    def get_enriched_portfolio_data(self):
        """Fetches current prices and calculates values for all assets."""
        if not self.assets:
            return []

        tickers = [asset.ticker for asset in self.assets]
        
        try:
            companies = Toolkit(tickers=tickers, api_key=self.api_key)
            prices_df = companies.get_quote()
            prices_df = prices_df.transpose()
        except Exception as e:
            print(f"❌ Failed to fetch prices: {e}")
            return []

        enriched_assets = []
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
    
    def get_portfolio_analysis(self):
        """Calculates total value and weights for assets, sectors, and classes."""
        enriched_data = self.get_enriched_portfolio_data()
        if not enriched_data:
            return None
        
        df = pd.DataFrame(enriched_data)
        total_portfolio_value = df['current_value'].sum()
        
        if total_portfolio_value == 0:
            return None
        
        df['weight'] = df['current_value'] / total_portfolio_value
        sector_weights = df.groupby('sector')['current_value'].sum() / total_portfolio_value
        class_weights = df.groupby('asset_class')['current_value'].sum() / total_portfolio_value
        
        return {
            "total_value": total_portfolio_value,
            "asset_weights": df[['ticker', 'weight']].to_dict('records'),
            "sector_weights": sector_weights.to_dict(),
            "class_weights": class_weights.to_dict()
        }

    def get_historical_data(self, tickers: list):
        """Gets historical data for a list of tickers."""
        try:
            companies = Toolkit(tickers=[t.upper() for t in tickers], api_key=self.api_key)
            return companies.get_historical_data()
        except Exception as e:
            print(f"❌ Could not fetch historical data for {', '.join(tickers)}: {e}")
            return None

    def run_simulation(self):
        """Runs a Monte Carlo simulation using Geometric Brownian Motion."""
        analysis = self.get_portfolio_analysis()
        if not analysis:
            return None

        tickers = [asset['ticker'] for asset in analysis['asset_weights']]
        weights = np.array([asset['weight'] for asset in analysis['asset_weights']])
        
        companies = Toolkit(tickers=tickers, api_key=self.api_key)
        
        historical_data = companies.get_historical_data()
        returns = historical_data['Close'].pct_change().dropna()

        mean_returns = returns[tickers].mean()
        portfolio_drift = np.sum(mean_returns * weights) * 252

        full_cov_matrix = returns.cov() * 252
        cov_matrix = full_cov_matrix.loc[tickers, tickers]
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

        initial_value = analysis['total_value']
        years = 15
        trading_days = 252
        simulations = 100000

        time_steps = years * trading_days
        daily_drift = portfolio_drift / trading_days
        daily_volatility = portfolio_volatility / np.sqrt(trading_days)
        
        random_shocks = np.random.standard_normal((time_steps, simulations))
        daily_returns = np.exp(daily_drift - 0.5 * daily_volatility**2 + daily_volatility * random_shocks)

        final_values = initial_value * daily_returns.cumprod(axis=0)[-1, :]

        return {
            "initial_value": initial_value,
            "mean": np.mean(final_values),
            "median": np.median(final_values),
            "5th_percentile": np.percentile(final_values, 5),
            "95th_percentile": np.percentile(final_values, 95),
        }

    def get_all_tickers(self) -> list:
        """Returns a list of all tickers in the portfolio."""
        return [asset.ticker for asset in self.assets]