import yfinance as yf
from datetime import date

def fetchDataFromPeriod(start_arg, end_arg):
    return yf.download("INTC", start = start_arg, end = end_arg)

def fetchDataFromPredefinedPeriod(period_arg):
    return yf.download("INTC", period = period_arg)

def getMaxFromMaxs(dataFrame):
    return dataFrame["High"].max()


def extendDataFrameByP5(dataFrame):
    return dataFrame.assign(
        P5 = lambda dataFrame: abs(dataFrame["Close"] - dataFrame["Open"]) / (dataFrame["High"] - dataFrame["Low"]),
    )

def extendDataFrameByP6(dataFrame):
    maxFromMaxs = getMaxFromMaxs(dataFrame)
    return dataFrame.assign(
        P6 = lambda dataFrame: dataFrame["Close"] / maxFromMaxs
    )

def extendDataFrameByP7(dataFrame):
    return dataFrame.assign(
        P7 = lambda row: (row["Close"] - row["Open"]) / row["Open"] * 20
    )

def extendDataFrameByResult(dataFrame):
    closeArr = dataFrame["Close"].values
    resultArr = []

    index = 0
    while index < len(closeArr) - 1:
        resultArr.append(int(closeArr[index + 1] > closeArr [index]))
        index += 1
    resultArr.append(0)

    print(len(closeArr), len(resultArr))

    dataFrame["Result"] = resultArr

    return dataFrame

def dropDataFrameColumns(dataFrame):
    return dataFrame.drop(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])

def saveStockDataFrameToCsv(dataFrame):
    fileName = "stock_data_" + date.today().strftime("%d-%m-%Y") + ".csv"
    dataCsvFile = open(fileName, "w")
    dataCsvFile.write(dataFrame.to_csv())
    dataCsvFile.close()

def main():
    stockDataFrame = fetchDataFromPredefinedPeriod("1y")
    stockDataFrame = stockDataFrame.reset_index()
    stockDataFrame = extendDataFrameByP5(stockDataFrame)
    stockDataFrame = extendDataFrameByP6(stockDataFrame)
    stockDataFrame = extendDataFrameByP7(stockDataFrame)
    stockDataFrame = extendDataFrameByResult(stockDataFrame)
    stockDataFrame = dropDataFrameColumns(stockDataFrame)
    saveStockDataFrameToCsv(stockDataFrame)

    # stockDataFrame = extendDataFrameByOpenCloseDerivatives(stockDataFrame.reset_index())
    # print(stockDataFrame)
    # stockDataFrame = extendDataFrameByCloseToMaxRatio(stockDataFrame)
    # stockDataFrame = extendDataFrameByOpenCloseDerivative(stockDataFrame)
    # stockDataFrame = extendDataFrameByValuesVariety(stockDataFrame)

    # saveStockDataFrameToCsv(stockDataFrame)

if __name__ == "__main__":
    main()
