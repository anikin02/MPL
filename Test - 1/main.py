import pandas

dataFrame = pandas.read_excel("info.xlsx", sheet_name="Sheet1")

def deleteFirstRow(data):
    return data.drop(0)

def deleteEmptyRaws(data):
    dataFrameCleaned = data.dropna(subset=data.columns[2:], how="all")
    return dataFrameCleaned.reset_index(drop=True)

def setWatched(data):
    data.iloc[:, 2:7] = data.iloc[:, 2:7].notna()
    return data

dataFrame = deleteFirstRow(dataFrame)
dataFrame = deleteEmptyRaws(dataFrame)
dataFrame = setWatched(dataFrame)



