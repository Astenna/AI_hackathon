import yfinance as yf
import pandas as pd
import json
import numpy as np
from datetime import date


def fetchDataFromPeriod(start_arg, end_arg):
    return yf.download("INTC", start=start_arg, end=end_arg)


def fetchDataFromPredefinedPeriod(period_arg):
    return yf.download("INTC", period=period_arg)


def getMaxFromMaxs(dataFrame):
    maxVal = dataFrame["High"].max()
    print("MaxFromMaxs", maxVal)
    return maxVal


def getMinFromMins(dataFrame):
    minVal = dataFrame["Low"].min()
    print("MinFromMins", minVal)
    return minVal


def extendDataFrameByP5(dataFrame):
    return dataFrame.assign(
        P5=lambda dataFrame: abs(
            dataFrame["Close"] - dataFrame["Open"]) / (dataFrame["High"] - dataFrame["Low"]),
    )


def extendDataFrameByP6(dataFrame):
    maxFromMaxs = getMaxFromMaxs(dataFrame)
    minFromMins = getMinFromMins(dataFrame)

    return dataFrame.assign(
        P6=lambda dataFrame: (
            dataFrame["Close"] - minFromMins) / (maxFromMaxs - minFromMins)
    )


def extendDataFrameByP7(dataFrame):
    return dataFrame.assign(
        P7=lambda row: (row["Close"] - row["Open"]) / row["Open"] * 20
    )


def extendDataFrameByResult(dataFrame):
    closeArr = dataFrame["Close"].values
    resultArr = []

    index = 0
    while index < len(closeArr) - 1:
        resultArr.append(int(closeArr[index + 1] > closeArr[index]))
        index += 1
    resultArr.append(0)

    dataFrame["Result"] = resultArr

    return dataFrame


def extendDataFrameByResult02(dataFrame):
    closeArr = dataFrame["Close"].values
    resultArr = []

    index = 0
    while index < len(closeArr) - 1:
        if closeArr[index + 1] - closeArr[index] > 0.24:
            resultArr.append(2)
        elif closeArr[index + 1] - closeArr[index] < -0.24:
            resultArr.append(0)
        else:
            resultArr.append(1)
        index += 1
    resultArr.append(0)

    dataFrame["Result"] = resultArr

    return dataFrame


def dropDataFrameColumns(dataFrame):
    return dataFrame.drop(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])

def dropDataFrameLastRow(dataFrame):
    return dataFrame.drop(dataFrame.tail(1).index)


def saveDataFrameToCsv(dataFrame, fileName, indexArg, headerArg):
    dataCsvFile = open(fileName, "w")
    dataCsvFile.write(dataFrame.to_csv(index=indexArg, header=headerArg))
    dataCsvFile.close()

def readCsvfFile(fileName):
    return pd.read_csv(fileName, sep=",")


def main():
    stockDataFrame = readCsvfFile("../datasets/support/plain_05-09-2019.csv")

    # stockDataFrame = stockDataFrame.reset_index()

    stockDataFrame = extendDataFrameByP5(stockDataFrame)
    stockDataFrame = extendDataFrameByP6(stockDataFrame)
    stockDataFrame = extendDataFrameByP7(stockDataFrame)
    stockDataFrame = extendDataFrameByResult(stockDataFrame)
    # stockDataFrame = extendDataFrameByResult02(stockDataFrame)

    stockDataFrame = dropDataFrameColumns(stockDataFrame)
    stockDataFrame = dropDataFrameLastRow(stockDataFrame)

    saveDataFrameToCsv(stockDataFrame, "../datasets/support/stock_result_0-1.csv", indexArg=False, headerArg=False)

if __name__ == "__main__":
    main()
