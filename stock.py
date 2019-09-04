import yfinance as yf

def fetchDataFromPeriod(start_arg, end_arg):
    return yf.download("INTC", start = start_arg, end = end_arg)

def fetchDataFromPredefinedPeriod(period_arg):
    return yf.download("INTC", period = period_arg)

def extendDataFrame(df):
    df = df.assign(
        ValuesVariety = lambda df: abs(df["Close"] - df["Open"]) / (df["High"] - df["Low"]),
        OpenCloseDerivative = lambda df: (df["Close"] - df["Open"]) / df["Open"]
    )

    return df

def main():
    five_days = fetchDataFromPredefinedPeriod("1d")
    print((five_days))

if __name__ == "__main__":
    main()