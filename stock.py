import yfinance as yf
import pandas as pd 
import json
import numpy as np
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

def saveDataFrameToCsv(dataFrame, prefix):
    fileName = prefix+ "_" + date.today().strftime("%d-%m-%Y") + ".csv"
    dataCsvFile = open(fileName, "w")
    dataCsvFile.write(dataFrame.to_csv())
    dataCsvFile.close()

def readCsvfFile(fileName):
    return pd.read_csv(fileName, sep = ",")

def mergeTwitterStockDataFrames(twitterDataFrame, stockDataFrame):
    stockArr = list(stockDataFrame.values)
    # print(stockArr)
    with open("twitter.json", 'r') as json_file:
        twitterDict = json.load(json_file)

    for row in stockArr:
        row.append(twitterDict.get(str(row[0]).split(' ')[0], []))
        print(row)

    return stockArr
    # indexesToDrop = []
    # for stockIndex, stockRow in stockDataFrame.iterrows():
    #     found = False
    #     for twitterIndex, twitterRow in twitterDataFrame.iterrows():
    #         print(twitterRow["Date"], stockRow["Date"])
    #         if(twitterRow["Date"] == stockRow["Date"]):
    #             stockRow.set_value(stockIndex, "P1", twitterRow["P1"])
    #             stockRow.set_value(stockIndex, "P2", twitterRow["P2"])
    #             stockRow.set_value(stockIndex, "P3", twitterRow["P3"])
    #             stockRow.set_value(stockIndex, "P4", twitterRow["P4"])
    #             found = True
    #     if(found == False):
    #         indexesToDrop.append(stockIndex)
    
    # stockDataFrame = stockDataFrame.drop(index = indexesToDrop)
    # return stockDataFrame


def main():
    stockDataFrame = fetchDataFromPredefinedPeriod("5d")
    stockDataFrame = stockDataFrame.reset_index()
    stockDataFrame = extendDataFrameByP5(stockDataFrame)
    stockDataFrame = extendDataFrameByP6(stockDataFrame)
    stockDataFrame = extendDataFrameByP7(stockDataFrame)
    stockDataFrame = extendDataFrameByResult(stockDataFrame)
    stockDataFrame = dropDataFrameColumns(stockDataFrame)
    twitterDataFrame = readCsvfFile("twitter_data.csv")
    merged = mergeTwitterStockDataFrames(twitterDataFrame, stockDataFrame)
    print(merged)

if __name__ == "__main__":
    main()
