import yfinance as yf
import pandas as pd
import json
import numpy as np
from datetime import date, timedelta, datetime
from argparse import ArgumentParser


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


def extendDataFrameByResult1(dataFrame):
    closeArr = dataFrame["Close"].values
    resultArr = []

    index = 0
    while index < len(closeArr) - 1:
        resultArr.append(int(closeArr[index + 1] > closeArr[index]))
        index += 1
    resultArr.append(0)

    dataFrame["Result"] = resultArr

    return dataFrame


def extendDataFrameByResult2(dataFrame):
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


def extendDataFrameByResult4(dataFrame):
    closeArr = dataFrame["Close"].values
    resultArr = []

    index = 0
    while index < len(closeArr) - 1:
        if closeArr[index + 1] - closeArr[index] > 0.7:
            resultArr.append(4)
        elif closeArr[index + 1] - closeArr[index] > 0.2:
            resultArr.append(3)
        elif closeArr[index + 1] - closeArr[index] > -0.2:
            resultArr.append(2)
        elif closeArr[index + 1] - closeArr[index] > -0.7:
            resultArr.append(1)
        else:
            resultArr.append(0)
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
    parser = ArgumentParser()
    print(date.today().strftime("%Y-%m-%d"))
    parser.add_argument(
        "--start-date",
        dest="startDate",
        # default=date.today().strftime("%Y-%m-%d"),
        default=str((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")),
        help="Start date in YYYY-MM-DD format",
    )

    parser.add_argument(
        "--end-date",
        dest="endDate",
        default=date.today().strftime("%Y-%m-%d"),
        help="End date in YYYY-MM-DD format",
    )

    parser.add_argument(
        "--output",
        dest="outputFilename",
        default="stock.csv",
        help="Output file name in datasets/support directory (store output data)",
    )

    parser.add_argument(
        "--plain",
        dest="plainFilename",
        default="plain.csv",
        help="File name in datasets/support directory (store plain stock data)",
    )

    parser.add_argument(
        "--result",
        dest="resultMode",
        default="1",
        help="Result mode 0-x (possible: 1, 2, 4)"
    )

    args = parser.parse_args()

    stockDataFrame = fetchDataFromPeriod(args.startDate, args.endDate)
    # stockDataFrame = fetchDataFromPredefinedPeriod("5d")
    print(stockDataFrame)

    saveDataFrameToCsv(stockDataFrame, "../datasets/support/" +
                       args.plainFilename, indexArg=True, headerArg=True)
    stockDataFrame = readCsvfFile("../datasets/support/" + args.plainFilename)

    # stockDataFrame = stockDataFrame.reset_index()

    stockDataFrame = extendDataFrameByP5(stockDataFrame)
    stockDataFrame = extendDataFrameByP6(stockDataFrame)
    stockDataFrame = extendDataFrameByP7(stockDataFrame)

    if args.resultMode == 1:
        stockDataFrame = extendDataFrameByResult1(stockDataFrame)
    elif args.resultMode == 2:
        stockDataFrame = extendDataFrameByResult2(stockDataFrame)
    else:
        stockDataFrame = extendDataFrameByResult4(stockDataFrame)

    stockDataFrame = dropDataFrameColumns(stockDataFrame)

    if(args.startDate != args.endDate):
        stockDataFrame = dropDataFrameLastRow(stockDataFrame)

    saveDataFrameToCsv(stockDataFrame, "../datasets/support/" +
                       args.outputFilename, indexArg=False, headerArg=False)


if __name__ == "__main__":
    main()
