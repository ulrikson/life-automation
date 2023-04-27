import yfinance as yf
import datetime


class StockPrice:
    def __init__(self, symbol, days_back):
        self.symbol = symbol
        self.days_back = days_back

    def get_percent_change(self):
        # Define the start and end dates for the analysis
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=self.days_back)

        # Download the historical stock data
        stock_data = yf.download(
            self.symbol, start=start_date, end=end_date, progress=False
        )

        last_close_price = stock_data["Adj Close"][-1]
        first_close_price = stock_data["Adj Close"][0]

        # Calculate the percentage change
        percent_change = (last_close_price / first_close_price - 1) * 100

        # Return the percentage change
        return percent_change

    def get_change_formatted(self):
        text = "## Stocks 📈\n"
        change = self.get_percent_change()
        changeDirection = "up" if change > 0 else "down"
        text += (
            f"{self.symbol} is {changeDirection} {change:.2f}% in the last {self.days_back} days"
        )
        return text


if __name__ == "__main__":
    stock = StockPrice("^OMX", 90)
    print(stock.get_change_formatted())