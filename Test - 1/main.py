import pandas
import matplotlib.pyplot as pyplot

dataFrame = pandas.read_excel("info.xlsx", sheet_name="Sheet1")

def deleteFirstRow(data):
    return data.drop(0)

def deleteEmptyRaws(data):
    dataFrameCleaned = data.dropna(subset=data.columns[2:], how="all")
    return dataFrameCleaned.reset_index(drop=True)

def setWatched(data):
    data.iloc[:, 3:8] = data.iloc[:, 3:8].notna()
    return data

def renameColumns(data):
    newNameColumns = {
        "Have you seen any of the 6 films in the Star Wars franchise?": "Смотрели Звездные войны?",
        "Do you consider yourself to be a fan of the Star Wars film franchise?": "Поклонник Звездных Войн?",
        "Which of the following Star Wars films have you seen? Please select all that apply.": "Смотрел Звездные Войны - 1",
        "Unnamed: 4": "Смотрел Звездные Войны - 2",
        "Unnamed: 5": "Смотрел Звездные Войны - 3",
        "Unnamed: 6": "Смотрел Звездные Войны - 4",
        "Unnamed: 7": "Смотрел Звездные Войны - 5",
        "Unnamed: 8": "Смотрел Звездные Войны - 6",
        "Please rank the Star Wars films in order of preference with 1 being your favorite film in the franchise and 6 being your least favorite film.": "1 часть Star Wars",
        "Unnamed: 10": "2 часть Star Wars",
        "Unnamed: 11": "3 часть Star Wars",
        "Unnamed: 12": "4 часть Star Wars",
        "Unnamed: 13": "5 часть Star Wars",
        "Unnamed: 14": "6 часть Star Wars",
        "Please state whether you view the following characters favorably, unfavorably, or are unfamiliar with him/her.": "Хан Соло",
        "Unnamed: 16": "Люк Скайвокер",
        "Unnamed: 17": "Принцесса Лея",
        "Unnamed: 18": "Энакин Скайвокер",
        "Unnamed: 19": "Оби Ван",
        "Unnamed: 20": "Император Палпатин",
        "Unnamed: 21": "Дарт Вейдер/Энакин Скайвокер",
        "Unnamed: 22": "Ландо Калриссиан",
        "Unnamed: 23": "Боба Фетт",
        "Unnamed: 24": "C-3P0",
        "Unnamed: 25": "R2 D2",
        "Unnamed: 26": "Джа Джа Бинкс",
        "Unnamed: 27": "Падме",
        "Unnamed: 28": "Магистр Йода",
        "Which character shot first?": "Кто выстрелил первым?",
        "Are you familiar with the Expanded Universe?": "Знакомы ли вы с Expanded Universe?",
        "Do you consider yourself to be a fan of the Expanded Universe?Œæ": "Поклонник Expanded Universe?",
        "Do you consider yourself to be a fan of the Star Trek franchise?": "Поклонник Star Trek?",
        "Gender": "Пол",
        "Age": "Возраст",
        "Education": "Образование",
        "Location (Census Region)": "Локация"
    }

    data.rename(columns=newNameColumns, inplace=True)
    return data

def splitIncomeRange(incomeRange):
    lowerBound = ""
    upperBound = ""

    if pandas.isna(incomeRange):
        lowerBound = "$0"
        upperBound = "$999,999"
    elif "+" in incomeRange:
        lowerBound = incomeRange[:-1]
        upperBound = "$999,999"
    elif "-" in incomeRange:
        lowerBound, upperBound = incomeRange.split(" - ")
    else:
        lowerBound = "$0"
        upperBound = "$999,999"

    return lowerBound, upperBound

def splitHouseholdIncomeColumn(data):
    data[["Нижняя граница дохода", "Верхняя граница дохода"]] = data["Household Income"].apply(splitIncomeRange).apply(pandas.Series)
    data = data.drop("Household Income", axis=1)
    return data

# Список людей, где мужчины поставили 4-6 часть на 1-2 место, а 1-3 часть на 5-6.
def getDataFrametMaleOldSchoolID(data):
    filtereData = data[
        (data['Пол'] == 'Male') &
        ((data['4 часть Star Wars'] <= "2") | (data['5 часть Star Wars'] <= "2") | (data['6 часть Star Wars'] <= "2")) &
        ((data['1 часть Star Wars'] >= "5") | (data['2 часть Star Wars'] >= "5") | (data['3 часть Star Wars'] >= "5"))
    ]

    return filtereData

def showCountFansAndUnfunsStarTrack(data):
    respondent_ids = getDataFrametMaleOldSchoolID(data)
    fanCount = (data["Поклонник Star Trek?"] == "Yes").sum()
    unfanCount = (data["Поклонник Star Trek?"] == "No").sum()
    print(f"Количество фанатов Star Trek: {fanCount}")
    print(f"Количество людей, которые не фанаты Star Trek: {unfanCount}")
    
def getDataFrameTop10Female(data):
    filtereData = data[
        (data["Пол"] == "Female") &
        ((data["4 часть Star Wars"] <= "2") | (data["5 часть Star Wars"] <= "2") | (data["6 часть Star Wars"] <= "2")) &
        (data["Поклонник Star Trek?"] == "Yes")
    ]
    return filtereData.head(10)

def getCountFanstMovie(data) -> {}:
    countFans = {}

    for i in range(1, 7):
        movie = f"{i} часть Star Wars"
        filtereData = data[
            (data[movie] == "1")
        ]
        countFans[movie] = len(filtereData)

    return countFans

def showGenderGraphFromFilm(data):
    groupedData = data[["1 часть Star Wars", "2 часть Star Wars", '3 часть Star Wars', '4 часть Star Wars', '5 часть Star Wars', '6 часть Star Wars', 'Пол']]
    groupedData[["1 часть Star Wars", "2 часть Star Wars", '3 часть Star Wars', '4 часть Star Wars', '5 часть Star Wars', '6 часть Star Wars']] = groupedData[['1 часть Star Wars', '2 часть Star Wars', '3 часть Star Wars', '4 часть Star Wars', '5 часть Star Wars', '6 часть Star Wars']].apply(pandas.to_numeric)
    groupedData = groupedData.groupby("Пол").mean()
    groupedData.T.plot(kind='bar', rot=0)
    pyplot.title("Средняя оценка по частям Star Wars в зависимости от пола")
    pyplot.xlabel("Часть Звездных Войн")
    pyplot.ylabel("Средняя оценка")
    pyplot.legend(title='Пол', loc='upper right')
    pyplot.show()

def showAgerGraphFromFilm(data):
    groupedData = data[["1 часть Star Wars", "2 часть Star Wars", '3 часть Star Wars', '4 часть Star Wars', '5 часть Star Wars', '6 часть Star Wars', 'Возраст']]
    groupedData[["1 часть Star Wars", "2 часть Star Wars", '3 часть Star Wars', '4 часть Star Wars', '5 часть Star Wars', '6 часть Star Wars']] = groupedData[['1 часть Star Wars', '2 часть Star Wars', '3 часть Star Wars', '4 часть Star Wars', '5 часть Star Wars', '6 часть Star Wars']].apply(pandas.to_numeric)
    groupedData = groupedData.groupby("Возраст").mean()
    groupedData.T.plot(kind='bar', rot=0)
    pyplot.title("Средняя оценка по частям Star Wars в зависимости от возраста")
    pyplot.xlabel("Часть Звездных Войн")
    pyplot.ylabel("Средняя оценка")
    pyplot.legend(title='Возраст', loc='upper right')
    pyplot.show()

dataFrame = deleteFirstRow(dataFrame)
dataFrame = deleteEmptyRaws(dataFrame)
dataFrame = setWatched(dataFrame)
dataFrame = renameColumns(dataFrame)
dataFrame = splitHouseholdIncomeColumn(dataFrame)

showCountFansAndUnfunsStarTrack(dataFrame)
print(getDataFrameTop10Female(dataFrame))

print(getCountFanstMovie(dataFrame))

showGenderGraphFromFilm(dataFrame)
showAgerGraphFromFilm(dataFrame)