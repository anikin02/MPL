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

# Second Part

def renameColumns(data, oldName, newName):
    return data.rename(columns={oldName: newName})

dataFrame = renameColumns(dataFrame, "Остаток", "ВсегоТовара")
dataFrame = renameColumns(dataFrame, "Количество", "НаВитрине")

# можно было написать все одной строчкой: dataFrame = dataFrame.rename(columns={"Остаток": "ВсегоТовара", "Остаток": "ВсегоТовара" })

def avgPricesCategory(data):
    groupPrice = data.groupby("КодКатегории")["Цена"].apply(list)
    
    for index, item in enumerate(groupPrice):
       groupPrice[index] = (round(sum(item) / len(item), 3)) # округляю до трех знаков после запятой, чтобы приятнее выглядило 
    
    return groupPrice

def findDifference(row, group):
    return row["Цена"] - group[row["КодКатегории"]]

def createColumnsDifference(data):
    group = avgPricesCategory(data)
    data["Разница"] = data.apply(lambda row: findDifference(row, group), axis=1)
    print(data)

createColumnsDifference(dataFrame)