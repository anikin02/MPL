import pandas

dataFrame = pandas.read_csv("Laboratory - 1/bdf92d44747096a5.csv")

# First Part
dataFrame = dataFrame.fillna(0)

def findColumsForDelete(data) -> []:
    columnsDelete = []
    for item in data:
        if data[item].max() == 0:
            columnsDelete.append(item)
    return columnsDelete

dataFrame = dataFrame.drop(columns = findColumsForDelete(dataFrame))
print(dataFrame)