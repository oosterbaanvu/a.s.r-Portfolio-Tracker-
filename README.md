
## Installation

Follow these steps to set up and run the project on your local machine.

1.  **Clone the Repository**
    Open your terminal or command prompt and run:
    ```bash
    git clone <your-repository-url>
    cd investment_cli
    ```

2.  **Create a Python Virtual Environment**
    It is highly recommended to use a virtual environment to manage project dependencies.
    ```bash
    python -m venv venv
    ```

3.  **Activate the Environment**
    -   On **Windows** (PowerShell):
        ```powershell
        .\venv\Scripts\activate
        ```
    -   On **macOS/Linux**:
        ```bash
        source venv/bin/activate
        ```

4.  **Install Dependencies**
    Install all the required Python libraries from the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

---

## Setup

The application uses the `financetoolkit` library, which requires a free API key from **Financial Modeling Prep**.

1.  Go to [https://site.financialmodelingprep.com/](https://site.financialmodelingprep.com/) and sign up for a free account.
2.  Find your API key in your user dashboard.
3.  Open the `main.py` file and replace the placeholder key with your actual key:
    ```python
    # in main.py
    FMP_API_KEY = "YOUR_FMP_API_KEY"
    ```

---

## Usage (Commands)

All commands are run from the terminal in the project's root directory.

### Add an Asset
Adds a new asset to your portfolio and saves it.

-   **Format:** `python main.py add <TICKER> <SECTOR> <ASSET_CLASS> <QUANTITY> <PRICE>`
-   **Example:**
    ```bash
    python main.py add AAPL Technology Stock 10 150.25
    python main.py add VTI "Total Market" ETF 5 270.00
    ```
    *Note: Use quotes for multi-word arguments like "Total Market".*

### Show Portfolio
Displays all assets in your portfolio with their current market value.

-   **Command:**
    ```bash
    python main.py show
    ```

### Analyze Portfolio
Shows the total portfolio value and the weight distribution by asset, sector, and class.

-   **Command:**
    ```bash
    python main.py analyze
    ```

### Graph Historical Price
Generates a `.png` image file with the historical price chart for a single ticker.

-   **Format:** `python main.py graph <TICKER>`
-   **Example:**
    ```bash
    python main.py graph MSFT
    ```
    *(This will create a file named `MSFT_price_chart.png` in your project folder.)*

### Run Simulation
Runs the 15-year, 100,000-path Monte Carlo simulation on your current portfolio. This may take 5-30 seconds to complete.

-   **Command:**
    ```bash
    python main.py simulate
    ```

### Show Help
To see the list of available commands at any time, run:
```bash
python main.py -h