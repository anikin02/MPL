import pandas

dataFrame = pandas.read_csv("bdf92d44747096a5.csv")
dataFrame = dataFrame.fillna(0)

columnsDelete = []

for item in dataFrame:
    if dataFrame[item].max() == 0:
        columnsDelete.append(item)

dataFrame = dataFrame.drop(columns = columnsDelete)

print(dataFrame)