import sqlite3
import tkinter
from tkinter import ttk
import matplotlib.pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# sqlite database
sqlConnection = sqlite3.connect("sqlDatabase.db")
sqlCursor = sqlConnection.cursor()


# tkinter closing section
def closingSection():
    window.quit()  # stops mainloop
    window.destroy()  # this is necessary on Windows to prevent Fatal Python Error: PyEval_RestoreThread: NULL tstate
    sqlConnection.commit()
    sqlConnection.close()


# database functions
def dropTables():
    sqlCursor.execute("DROP TABLE IF EXISTS owner")
    sqlCursor.execute("DROP TABLE IF EXISTS features")
    sqlCursor.execute("DROP TABLE IF EXISTS building")


def createTables():  # for creating tables
    sqlCursor.execute("CREATE TABLE IF NOT EXISTS building(id, owner, name, number, address, "
                      "coordinate);")  # building table
    sqlCursor.execute("CREATE TABLE IF NOT EXISTS features(buildingName, floors, square, year, zone, type, geometry, "
                      "isBasement, width, length, damaged, risk);")  # building features table
    sqlCursor.execute("CREATE TABLE IF NOT EXISTS owner(no INTEGER PRIMARY KEY, ownerName, ownerSurname, gender, age);")  # owner table


def fillTables():  # for filling the tables
    sqlCursor.execute("""
        INSERT INTO owner VALUES
            (1, "Henry", "Blackburne", "male", 35),
            (2, "Emily", "Scarlett", "female", 27),
            (3, "Diva", "Smith", "female", 56),
            (4, "John", "Tractor", "male", 98),
            (5, "Elliot", "Pearl", "other", 21);
        """)
    sqlCursor.execute("""
        INSERT INTO building VALUES
            (1, "Henry Blackburne", "Building1", 11, "Province1, District1, Neighbourhood1, Street1", "0, 0"),
            (2, "Henry Blackburne", "Building2", 12, "Province2, District2, Neighbourhood2, Street2", "0, 1"),
            (3, "Henry Blackburne", "Building3", 13, "Province3, District3, Neighbourhood3, Street3", "0, 2"),
            (4, "Emily Scarlett", "Building4", 14, "Province4, District4, Neighbourhood4, Street4", "1, 0"),
            (5, "Emily Scarlett", "Building5", 15, "Province5, District5, Neighbourhood5, Street5", "1, 1"),
            (6, "Emily Scarlett", "Building6", 16, "Province6, District6, Neighbourhood6, Street6", "1, 2"),
            (7, "Diva Smith", "Building7", 17, "Province, District7, Neighbourhood7, Street7", "2, 0"),
            (8, "Diva Smith", "Building8", 18, "Province8, District8, Neighbourhood8, Street8", "2, 1"),
            (9, "Diva Smith", "Building9", 19, "Province9, District9, Neighbourhood9, Street9", "2, 2"),
            (10, "John Tractor", "Building10", 20, "Province10, District10, Neighbourhood10, Street10", "3, 0"),
            (11, "John Tractor", "Building11", 21, "Province11, District11, Neighbourhood11, Street11", "3, 1"),
            (12, "John Tractor", "Building12", 22, "Province12, District12, Neighbourhood12, Street12", "3, 2"),
            (13, "Elliot Pearl", "Building13", 23, "Province13, District13, Neighbourhood13, Street13", "4, 0"),
            (14, "Elliot Pearl", "Building14", 24, "Province14, District14, Neighbourhood14, Street14", "4, 1"),
            (15, "Elliot Pearl", "Building15", 25, "Province15, District15, Neighbourhood15, Street15", "4, 2");
        """)


def resetTables():
    dropTables()
    createTables()
    fillTables()
    successPopUp("The database is reset to its initial state.")


# GUI functions
def setMainFrame():
    global mainFrame
    mainFrame = ttk.Frame(window)
    mainFrame.grid(row=0, column=0)

    tkinter.Label(mainFrame, text="Select Operation").grid(row=0, column=0)
    tkinter.Label(mainFrame, text="--------").grid(row=1, column=0)
    ttk.Button(mainFrame, text="Owner Operations", command=resetOwnerFrame).grid(row=2, column=0)
    ttk.Button(mainFrame, text="Add Building Information", command=resetBuildingFrame).grid(row=3, column=0)
    ttk.Button(mainFrame, text="Display Risk Score Graphics", command=resetRiskFrame).grid(row=4, column=0)
    ttk.Button(mainFrame, text="Other Query Operations", command=resetOtherFrame).grid(row=5, column=0)
    tkinter.Label(mainFrame, text="--------").grid(row=6, column=0)
    ttk.Button(mainFrame, text="Reset Database", command=resetTables).grid(row=7, column=0)


def deleteFrames():
    for widget in window.winfo_children():
        widget.destroy()


def setBackFrame():
    global backFrame
    backFrame = ttk.Frame(window)
    backFrame.grid(row=1, column=0)

    tkinter.Label(backFrame, text="--------").grid(row=0, column=0)
    ttk.Button(backFrame, text="Back", command=getBack2Main).grid(row=1, column=0)


def getBack2Main():
    deleteFrames()
    setMainFrame()


def resetOwnerFrame():
    deleteFrames()

    global ownerFrame
    global ownerSelectCombobox
    ownerFrame = ttk.Frame(window)
    ownerFrame.grid(row=0, column=0)

    setBackFrame()

    tkinter.Label(ownerFrame, text="Building Owner").grid(row=0, column=1)
    tkinter.Label(ownerFrame, text="Select Operation:   ").grid(row=1, column=0)
    ownerSelectCombobox = ttk.Combobox(ownerFrame, state="readonly",
                                       values=["Add", "Edit", "Delete", "List Information"])
    ownerSelectCombobox.grid(row=1, column=1)
    ttk.Button(ownerFrame, text="OK", command=ownerSelectButtonFunc).grid(row=1, column=2)


def resetBuildingFrame():
    deleteFrames()

    global buildingFrame
    global buildingSelectCombobox
    buildingFrame = ttk.Frame(window)
    buildingFrame.grid(row=0, column=0)

    setBackFrame()

    tkinter.Label(buildingFrame, text="Add Building Information to Calculate Risk Score").grid(row=0, column=1)
    tkinter.Label(buildingFrame, text="Select Building:   ").grid(row=1, column=0)
    sqlCursor.execute("SELECT name FROM building")

    buildingList = list()
    for building in sqlCursor:
        buildingList.append(building[0])
    sqlCursor.execute("SELECT buildingName FROM features")
    buildingsWithInfo = list()
    for building in sqlCursor:
        buildingsWithInfo.append(building[0])
    if len(buildingsWithInfo) != 0:
        buildingList = [build for build in buildingList if build not in buildingsWithInfo]

    buildingSelectCombobox = ttk.Combobox(buildingFrame, state="readonly", values=buildingList)
    buildingSelectCombobox.grid(row=1, column=1)

    ttk.Button(buildingFrame, text="OK", command=buildingSelectButtonFunc).grid(row=1, column=2)


def resetRiskFrame():
    deleteFrames()

    global riskFrame
    riskFrame = ttk.Frame(window)
    riskFrame.grid(row=0, column=0)

    setBackFrame()

    tkinter.Label(riskFrame, text="Risk Score").grid(row=0, column=0)
    tkinter.Label(riskFrame, text="-----").grid(row=1, column=0)

    sqlCursor.execute("SELECT buildingName, risk, type, floors, year FROM features")
    features = sqlCursor.fetchall()

    nameRC = list()  # reinforced concrete
    riskRC = list()
    yearRC = list()

    nameM = list()  # masonry
    riskM = list()
    floorsM = list()

    for building in features:
        if building[2] == "reinforced concrete":
            nameRC.append(building[0])
            riskRC.append(building[1])
            yearRC.append(building[4])
        else:  # masonry
            nameM.append(building[0])
            riskM.append(building[1])
            floorsM.append(building[3])

    reinforcedFig = matplotlib.pyplot.figure(figsize=(4, 4), dpi=70)
    if len(riskRC) > 0:
        for i in range(len(riskRC)):
            matplotlib.pyplot.bar(yearRC[i], riskRC[i], label=nameRC[i])
        reinforcedFig.legend()
    reinforcedFig.suptitle("Reinforced Concrete Buildings")
    reinforcedFig.supxlabel("Year")
    reinforcedFig.supylabel("Risk Score")
    reinforcedCanvas = FigureCanvasTkAgg(reinforcedFig, master=riskFrame)
    reinforcedCanvas.draw()
    reinforcedCanvas.get_tk_widget().grid(row=2, column=0)

    masonryFig = matplotlib.pyplot.figure(figsize=(4, 4), dpi=70)
    if len(riskM) > 0:
        for i in range(len(riskM)):
            matplotlib.pyplot.bar(floorsM[i], riskM[i], label=nameM[i])
        masonryFig.legend()
    masonryFig.suptitle("Masonry Buildings")
    masonryFig.supxlabel("Floor count")
    masonryFig.supylabel("Risk Score")
    masonryCanvas = FigureCanvasTkAgg(masonryFig, master=riskFrame)
    masonryCanvas.draw()
    masonryCanvas.get_tk_widget().grid(row=3, column=0)


def resetOtherFrame():
    # the code below can be shortened so much

    deleteFrames()

    global otherFrame
    otherFrame = ttk.Frame(window)
    otherFrame.grid(row=0, column=0)

    setBackFrame()

    tkinter.Label(otherFrame, text="Other").grid(row=0, column=1, columnspan=2)
    tkinter.Label(otherFrame, text="-----").grid(row=1, column=1, columnspan=2)

    # select owners by gender
    tkinter.Label(otherFrame, text="Owner by Gender:").grid(row=2, column=0)
    otherGender = ttk.Combobox(otherFrame, state="readonly", values=["male", "female", "other"])
    otherGender.grid(row=2, column=1)
    otherGenderResult = ttk.Combobox(otherFrame, state="readonly", values=[])
    otherGenderResult.grid(row=2, column=3)

    def otherGenderButtonFunc():
        nonlocal otherGenderResult
        gender = otherGender.get()
        sqlCursor.execute(f"SELECT ownerName, ownerSurname FROM owner WHERE gender = '{gender}'")
        ownerNamesGender = list()
        for name_, surname_ in sqlCursor:
            ownerNamesGender.append(name_ + " " + surname_)
        if len(ownerNamesGender) == 0:
            otherGenderResult = ttk.Combobox(otherFrame, state="readonly", values=["<No Suitable Data>"])
        else:
            otherGenderResult = ttk.Combobox(otherFrame, state="readonly", values=ownerNamesGender)
        otherGenderResult.grid(row=2, column=3)

    ttk.Button(otherFrame, text="LIST", command=otherGenderButtonFunc).grid(row=2, column=2)

    # select buildings by owner
    tkinter.Label(otherFrame, text="Owned by:").grid(row=3, column=0)
    sqlCursor.execute(f"SELECT ownerName, ownerSurname FROM owner")
    ownerNames = list()
    for name, surname in sqlCursor:
        ownerNames.append(name + " " + surname)
    otherOwner2Building = ttk.Combobox(otherFrame, state="readonly", values=ownerNames)
    otherOwner2Building.grid(row=3, column=1)
    otherOwner2BuildingResult = ttk.Combobox(otherFrame, state="readonly", values=[])
    otherOwner2BuildingResult.grid(row=3, column=3)

    def otherOwner2BuildingButtonFunc():
        nonlocal otherOwner2BuildingResult
        owner = otherOwner2Building.get()
        sqlCursor.execute(f"SELECT name FROM building WHERE owner = '{owner}'")
        buildingNames = list()
        for building in sqlCursor:
            buildingNames.append(building)
        if len(buildingNames) == 0:
            otherOwner2BuildingResult = ttk.Combobox(otherFrame, state="readonly", values=["<No Suitable Data>"])
        else:
            otherOwner2BuildingResult = ttk.Combobox(otherFrame, state="readonly", values=buildingNames)
        otherOwner2BuildingResult.grid(row=3, column=3)

    ttk.Button(otherFrame, text="LIST", command=otherOwner2BuildingButtonFunc).grid(row=3, column=2)

    # select buildings by type
    tkinter.Label(otherFrame, text="Building by Type:").grid(row=4, column=0)
    otherType = ttk.Combobox(otherFrame, state="readonly", values=["reinforced concrete", "masonry"])
    otherType.grid(row=4, column=1)
    otherTypeResult = ttk.Combobox(otherFrame, state="readonly", values=[])
    otherTypeResult.grid(row=4, column=3)

    def otherTypeButtonFunc():
        nonlocal otherTypeResult
        type_ = otherType.get()
        sqlCursor.execute(f"SELECT buildingName FROM features WHERE type = '{type_}'")
        buildings = list()
        for building in sqlCursor:
            buildings.append(building)
        if len(buildings) == 0:
            otherTypeResult = ttk.Combobox(otherFrame, state="readonly", values=["<No Suitable Data>"])
        else:
            otherTypeResult = ttk.Combobox(otherFrame, state="readonly", values=buildings)
        otherTypeResult.grid(row=4, column=3)

    ttk.Button(otherFrame, text="LIST", command=otherTypeButtonFunc).grid(row=4, column=2)

    # select buildings by basement
    tkinter.Label(otherFrame, text="Has Basement:").grid(row=5, column=0)
    otherBasement = ttk.Combobox(otherFrame, state="readonly", values=["true", "false"])
    otherBasement.grid(row=5, column=1)
    otherBasementResult = ttk.Combobox(otherFrame, state="readonly", values=[])
    otherBasementResult.grid(row=5, column=3)

    def otherBasementButtonFunc():
        nonlocal otherBasementResult
        basement = otherBasement.get()
        sqlCursor.execute(f"SELECT buildingName FROM features WHERE isBasement = '{basement}'")
        buildings = list()
        for building in sqlCursor:
            buildings.append(building)
        if len(buildings) == 0:
            otherBasementResult = ttk.Combobox(otherFrame, state="readonly", values=["<No Suitable Data>"])
        else:
            otherBasementResult = ttk.Combobox(otherFrame, state="readonly", values=buildings)
        otherBasementResult.grid(row=5, column=3)

    ttk.Button(otherFrame, text="LIST", command=otherBasementButtonFunc).grid(row=5, column=2)

    # select building by damaged
    tkinter.Label(otherFrame, text="Is Damaged:").grid(row=6, column=0)
    otherDamaged = ttk.Combobox(otherFrame, state="readonly", values=["true", "false"])
    otherDamaged.grid(row=6, column=1)
    otherDamagedResult = ttk.Combobox(otherFrame, state="readonly", values=[])
    otherDamagedResult.grid(row=6, column=3)

    def otherDamagedButtonFunc():
        nonlocal otherDamagedResult
        damaged = otherDamaged.get()
        sqlCursor.execute(f"SELECT buildingName FROM features WHERE damaged = '{damaged}'")
        buildings = list()
        for building in sqlCursor:
            buildings.append(building)
        if len(buildings) == 0:
            otherDamagedResult = ttk.Combobox(otherFrame, state="readonly", values=["<No Suitable Data>"])
        else:
            otherDamagedResult = ttk.Combobox(otherFrame, state="readonly", values=buildings)
        otherDamagedResult.grid(row=6, column=3)

    ttk.Button(otherFrame, text="LIST", command=otherDamagedButtonFunc).grid(row=6, column=2)

    # select building by geometry
    tkinter.Label(otherFrame, text="Building by Geometry:").grid(row=7, column=0)
    otherGeometry = ttk.Combobox(otherFrame, state="readonly", values=["regular", "irregular"])
    otherGeometry.grid(row=7, column=1)
    otherGeometryResult = ttk.Combobox(otherFrame, state="readonly", values=[])
    otherGeometryResult.grid(row=7, column=3)

    def otherGeometryButtonFunc():
        nonlocal otherGeometryResult
        geometry = otherGeometry.get()
        sqlCursor.execute(f"SELECT buildingName FROM features WHERE geometry = '{geometry}'")
        buildings = list()
        for building in sqlCursor:
            buildings.append(building)
        if len(buildings) == 0:
            otherGeometryResult = ttk.Combobox(otherFrame, state="readonly", values=["<No Suitable Data>"])
        else:
            otherGeometryResult = ttk.Combobox(otherFrame, state="readonly", values=buildings)
        otherGeometryResult.grid(row=7, column=3)

    ttk.Button(otherFrame, text="LIST", command=otherGeometryButtonFunc).grid(row=7, column=2)

    # select building by zone
    tkinter.Label(otherFrame, text="Select Zone:").grid(row=8, column=0)
    otherZone = ttk.Combobox(otherFrame, state="readonly", values=["1", "2", "3", "4"])
    otherZone.grid(row=8, column=1)
    otherZoneResult = ttk.Combobox(otherFrame, state="readonly", values=[])
    otherZoneResult.grid(row=8, column=3)

    def otherZoneButtonFunc():
        nonlocal otherZoneResult
        zone = otherZone.get()
        sqlCursor.execute(f"SELECT buildingName FROM features WHERE zone = {zone}")
        buildings = list()
        for building in sqlCursor:
            buildings.append(building)
        if len(buildings) == 0:
            otherZoneResult = ttk.Combobox(otherFrame, state="readonly", values=["<No Suitable Data>"])
        else:
            otherZoneResult = ttk.Combobox(otherFrame, state="readonly", values=buildings)
        otherZoneResult.grid(row=8, column=3)

    ttk.Button(otherFrame, text="LIST", command=otherZoneButtonFunc).grid(row=8, column=2)

    # select building by risk score (lower than)
    tkinter.Label(otherFrame, text="Risk Lower Than:").grid(row=9, column=0)
    otherRiskLower = ttk.Entry(otherFrame)
    otherRiskLower.grid(row=9, column=1)
    otherRiskLowerResult = ttk.Combobox(otherFrame, state="readonly", values=[])
    otherRiskLowerResult.grid(row=9, column=3)

    def otherRiskLowerButtonFunc():
        nonlocal otherRiskLowerResult
        riskLower = otherRiskLower.get()
        if not riskLower.isdigit():
            errorPopUp("Risk Score should be numeric.")
            return
        sqlCursor.execute(f"SELECT buildingName FROM features WHERE risk < {riskLower}")
        buildings = list()
        for building in sqlCursor:
            buildings.append(building)
        if len(buildings) == 0:
            otherRiskLowerResult = ttk.Combobox(otherFrame, state="readonly", values=["<No Suitable Data>"])
        else:
            otherRiskLowerResult = ttk.Combobox(otherFrame, state="readonly", values=buildings)
        otherRiskLowerResult.grid(row=9, column=3)

    ttk.Button(otherFrame, text="LIST", command=otherRiskLowerButtonFunc).grid(row=9, column=2)

    # select building by risk score (higher than)
    tkinter.Label(otherFrame, text="Risk Higher Than:").grid(row=10, column=0)
    otherRiskHigher = ttk.Entry(otherFrame)
    otherRiskHigher.grid(row=10, column=1)
    otherRiskHigherResult = ttk.Combobox(otherFrame, state="readonly", values=[])
    otherRiskHigherResult.grid(row=10, column=3)

    def otherRiskHigherButtonFunc():
        nonlocal otherRiskHigherResult
        riskHigher = otherRiskHigher.get()
        if not riskHigher.isdigit():
            errorPopUp("Risk Score should be numeric.")
            return
        sqlCursor.execute(f"SELECT buildingName FROM features WHERE risk > {riskHigher}")
        buildings = list()
        for building in sqlCursor:
            buildings.append(building)
        if len(buildings) == 0:
            otherRiskHigherResult = ttk.Combobox(otherFrame, state="readonly", values=["<No Suitable Data>"])
        else:
            otherRiskHigherResult = ttk.Combobox(otherFrame, state="readonly", values=buildings)
        otherRiskHigherResult.grid(row=10, column=3)

    ttk.Button(otherFrame, text="LIST", command=otherRiskHigherButtonFunc).grid(row=10, column=2)

    # select building by year (before)
    tkinter.Label(otherFrame, text="Year Before:").grid(row=11, column=0)
    otherYearBefore = ttk.Entry(otherFrame)
    otherYearBefore.grid(row=11, column=1)
    otherYearBeforeResult = ttk.Combobox(otherFrame, state="readonly", values=[])
    otherYearBeforeResult.grid(row=11, column=3)

    def otherYearBeforeButtonFunc():
        nonlocal otherYearBeforeResult
        yearBefore = otherYearBefore.get()
        if not yearBefore.isdigit():
            errorPopUp("Year should be numeric.")
            return
        sqlCursor.execute(f"SELECT buildingName FROM features WHERE year < {yearBefore}")
        buildings = list()
        for building in sqlCursor:
            buildings.append(building)
        if len(buildings) == 0:
            otherYearBeforeResult = ttk.Combobox(otherFrame, state="readonly", values=["<No Suitable Data>"])
        else:
            otherYearBeforeResult = ttk.Combobox(otherFrame, state="readonly", values=buildings)
        otherYearBeforeResult.grid(row=11, column=3)

    ttk.Button(otherFrame, text="LIST", command=otherYearBeforeButtonFunc).grid(row=11, column=2)

    # select building by year (after)
    tkinter.Label(otherFrame, text="Year After:").grid(row=12, column=0)
    otherYearAfter = ttk.Entry(otherFrame)
    otherYearAfter.grid(row=12, column=1)
    otherYearAfterResult = ttk.Combobox(otherFrame, state="readonly", values=[])
    otherYearAfterResult.grid(row=12, column=3)

    def otherYearAfterButtonFunc():
        nonlocal otherYearAfterResult
        yearAfter = otherYearAfter.get()
        if not yearAfter.isdigit():
            errorPopUp("Year should be numeric.")
            return
        sqlCursor.execute(f"SELECT buildingName FROM features WHERE year > {yearAfter}")
        buildings = list()
        for building in sqlCursor:
            buildings.append(building)
        if len(buildings) == 0:
            otherYearAfterResult = ttk.Combobox(otherFrame, state="readonly", values=["<No Suitable Data>"])
        else:
            otherYearAfterResult = ttk.Combobox(otherFrame, state="readonly", values=buildings)
        otherYearAfterResult.grid(row=12, column=3)

    ttk.Button(otherFrame, text="LIST", command=otherYearAfterButtonFunc).grid(row=12, column=2)

    # select building by floor count (less than)
    tkinter.Label(otherFrame, text="Floor Less Than:").grid(row=13, column=0)
    otherFloorLess = ttk.Entry(otherFrame)
    otherFloorLess.grid(row=13, column=1)
    otherFloorLessResult = ttk.Combobox(otherFrame, state="readonly", values=[])
    otherFloorLessResult.grid(row=13, column=3)

    def otherFloorLessButtonFunc():
        nonlocal otherFloorLessResult
        floorLess = otherFloorLess.get()
        if not floorLess.isdigit():
            errorPopUp("Floor count should be numeric.")
            return
        sqlCursor.execute(f"SELECT buildingName FROM features WHERE floors < {floorLess}")
        buildings = list()
        for building in sqlCursor:
            buildings.append(building)
        if len(buildings) == 0:
            otherFloorLessResult = ttk.Combobox(otherFrame, state="readonly", values=["<No Suitable Data>"])
        else:
            otherFloorLessResult = ttk.Combobox(otherFrame, state="readonly", values=buildings)
        otherFloorLessResult.grid(row=13, column=3)

    ttk.Button(otherFrame, text="LIST", command=otherFloorLessButtonFunc).grid(row=13, column=2)

    # select building by risk score (higher than)
    tkinter.Label(otherFrame, text="Floor More Than:").grid(row=14, column=0)
    otherFloorMore = ttk.Entry(otherFrame)
    otherFloorMore.grid(row=14, column=1)
    otherFloorMoreResult = ttk.Combobox(otherFrame, state="readonly", values=[])
    otherFloorMoreResult.grid(row=14, column=3)

    def otherFloorMoreButtonFunc():
        nonlocal otherFloorMoreResult
        floorMore = otherFloorMore.get()
        if not floorMore.isdigit():
            errorPopUp("Floor count should be numeric.")
            return
        sqlCursor.execute(f"SELECT buildingName FROM features WHERE floors > {floorMore}")
        buildings = list()
        for building in sqlCursor:
            buildings.append(building)
        if len(buildings) == 0:
            otherFloorMoreResult = ttk.Combobox(otherFrame, state="readonly", values=["<No Suitable Data>"])
        else:
            otherFloorMoreResult = ttk.Combobox(otherFrame, state="readonly", values=buildings)
        otherFloorMoreResult.grid(row=14, column=3)

    ttk.Button(otherFrame, text="LIST", command=otherFloorMoreButtonFunc).grid(row=14, column=2)

    # select owners by age (younger than)
    tkinter.Label(otherFrame, text="Owner Younger Than:").grid(row=15, column=0)
    otherOwnerYounger = ttk.Entry(otherFrame)
    otherOwnerYounger.grid(row=15, column=1)
    otherOwnerYoungerResult = ttk.Combobox(otherFrame, state="readonly", values=[])
    otherOwnerYoungerResult.grid(row=15, column=3)

    def otherOwnerYoungerButtonFunc():
        nonlocal otherOwnerYoungerResult
        ownerYounger = otherOwnerYounger.get()
        if not ownerYounger.isdigit():
            errorPopUp("Age should be numeric.")
            return
        sqlCursor.execute(f"SELECT ownerName, ownerSurname FROM owner WHERE age < {ownerYounger}")
        ownerNamesYounger = list()
        for name_, surname_ in sqlCursor:
            ownerNamesYounger.append(name_ + " " + surname_)
        if len(ownerNamesYounger) == 0:
            otherOwnerYoungerResult = ttk.Combobox(otherFrame, state="readonly", values=["<No Suitable Data>"])
        else:
            otherOwnerYoungerResult = ttk.Combobox(otherFrame, state="readonly", values=ownerNamesYounger)
        otherOwnerYoungerResult.grid(row=15, column=3)

    ttk.Button(otherFrame, text="LIST", command=otherOwnerYoungerButtonFunc).grid(row=15, column=2)

    # select owners by age (older than)
    tkinter.Label(otherFrame, text="Owner Older Than:").grid(row=16, column=0)
    otherOwnerOlder = ttk.Entry(otherFrame)
    otherOwnerOlder.grid(row=16, column=1)
    otherOwnerOlderResult = ttk.Combobox(otherFrame, state="readonly", values=[])
    otherOwnerOlderResult.grid(row=16, column=3)

    def otherOwnerOlderButtonFunc():
        nonlocal otherOwnerOlderResult
        ownerOlder = otherOwnerOlder.get()
        if not ownerOlder.isdigit():
            errorPopUp("Age should be numeric.")
            return
        sqlCursor.execute(f"SELECT ownerName, ownerSurname FROM owner WHERE age > {ownerOlder}")
        ownerNamesOlder = list()
        for name_, surname_ in sqlCursor:
            ownerNamesOlder.append(name_ + " " + surname_)
        if len(ownerNamesOlder) == 0:
            otherOwnerOlderResult = ttk.Combobox(otherFrame, state="readonly", values=["<No Suitable Data>"])
        else:
            otherOwnerOlderResult = ttk.Combobox(otherFrame, state="readonly", values=ownerNamesOlder)
        otherOwnerOlderResult.grid(row=16, column=3)

    ttk.Button(otherFrame, text="LIST", command=otherOwnerOlderButtonFunc).grid(row=16, column=2)


# pop up notifications
def successPopUp(message: str):
    success = tkinter.Toplevel(window)
    success.title("Done!")
    success.geometry('400x40')
    tkinter.Label(success, text=message).pack()


def errorPopUp(errorMessage: str):
    error = tkinter.Toplevel(window)
    error.title("Error!")
    error.geometry('400x40')
    tkinter.Label(error, text=errorMessage).pack()


# algorithms
def ownerSelectButtonFunc():
    selectedOperation = ownerSelectCombobox.get()
    resetOwnerFrame()

    tkinter.Label(ownerFrame, text="--------").grid(row=2, column=1)

    if selectedOperation == "Add":
        def ownerAddButtonFunc():
            inputName = ownerAddName.get()
            inputSurname = ownerAddSurname.get()
            inputGender = ownerAddGender.get()
            inputAge = ownerAddAge.get()

            if inputName == "" or inputSurname == "" or inputGender == "" or inputAge == "":
                errorPopUp("Please fill all of the elements.")
            elif len((inputName + inputSurname + inputAge + inputGender).split()) != 1:
                errorPopUp("Space character is not allowed in elements")
            elif not inputAge.isdigit():
                errorPopUp("Age should be numeric")
            else:
                sqlCursor.execute(f"""
                    INSERT INTO owner (ownerName, ownerSurname, gender, age) VALUES
                    ("{inputName}", "{inputSurname}", "{inputGender}", {inputAge})
                    """)
                sqlConnection.commit()
                getBack2Main()
                successPopUp("New owner is added.")


        ownerAddNameLabel = tkinter.Label(ownerFrame, text="Name:  ")
        ownerAddNameLabel.grid(row=3, column=0)
        ownerAddName = tkinter.Entry(ownerFrame)
        ownerAddName.grid(row=3, column=1)

        ownerAddSurnameLabel = tkinter.Label(ownerFrame, text="Surname:  ")
        ownerAddSurnameLabel.grid(row=4, column=0)
        ownerAddSurname = tkinter.Entry(ownerFrame)
        ownerAddSurname.grid(row=4, column=1)

        ownerAddGenderLabel = tkinter.Label(ownerFrame, text="Gender:  ")
        ownerAddGenderLabel.grid(row=5, column=0)
        ownerAddGender = ttk.Combobox(ownerFrame, state="readonly", values=["male", "female", "other"])
        ownerAddGender.grid(row=5, column=1)

        ownerAddAgeLabel = tkinter.Label(ownerFrame, text="Age:  ")
        ownerAddAgeLabel.grid(row=6, column=0)
        ownerAddAge = tkinter.Entry(ownerFrame)
        ownerAddAge.grid(row=6, column=1)

        ownerAddButton = ttk.Button(ownerFrame, text="Add Owner", command=ownerAddButtonFunc)
        ownerAddButton.grid(row=6, column=2)

    elif selectedOperation == "Edit":
        ownerSelectLabel = tkinter.Label(ownerFrame, text="Select a owner to edit:   ")
        ownerSelectLabel.grid(row=3, column=0)

        sqlCursor.execute("SELECT ownerName, ownerSurname FROM owner")
        ownerFullNames = list()
        for name, surname in sqlCursor:
            ownerFullNames.append(name + " " + surname)

        ownerEditCombobox = ttk.Combobox(ownerFrame, state="readonly", values=ownerFullNames)
        ownerEditCombobox.grid(row=3, column=1)

        def ownerEditButtonFunc():
            selectedOwner = ownerEditCombobox.get()
            ownerName, ownerSurname = selectedOwner.split()
            sqlCursor.execute(
                f"SELECT * FROM owner WHERE ownerName = '{ownerName}' AND ownerSurname = '{ownerSurname}'")
            ownerInformation = sqlCursor.fetchall()

            ownerEditNameLabel = tkinter.Label(ownerFrame, text="Name:  ")
            ownerEditNameLabel.grid(row=4, column=0)
            ownerEditName = ttk.Entry(ownerFrame)
            ownerEditName.grid(row=4, column=1)
            ownerEditName.insert(-1, ownerInformation[0][1])

            ownerEditSurnameLabel = tkinter.Label(ownerFrame, text="Surname:  ")
            ownerEditSurnameLabel.grid(row=5, column=0)
            ownerEditSurname = ttk.Entry(ownerFrame)
            ownerEditSurname.grid(row=5, column=1)
            ownerEditSurname.insert(-1, ownerInformation[0][2])

            ownerEditGenderLabel = tkinter.Label(ownerFrame, text="Gender:  ")
            ownerEditGenderLabel.grid(row=6, column=0)
            ownerEditGender = ttk.Combobox(ownerFrame, state="readonly", values=["male", "female", "other"])
            ownerEditGender.grid(row=6, column=1)
            if ownerInformation[0][3] == "male":
                ownerEditGender.current(0)
            elif ownerInformation[0][3] == "female":
                ownerEditGender.current(1)
            elif ownerInformation[0][3] == "other":
                ownerEditGender.current(2)

            ownerEditAgeLabel = tkinter.Label(ownerFrame, text="Age:  ")
            ownerEditAgeLabel.grid(row=7, column=0)
            ownerEditAge = ttk.Entry(ownerFrame)
            ownerEditAge.grid(row=7, column=1)
            ownerEditAge.insert(-1, ownerInformation[0][4])

            def ownerEditSubmitButtonFunc():
                inputName = ownerEditName.get()
                inputSurname = ownerEditSurname.get()
                inputGender = ownerEditGender.get()
                inputAge = ownerEditAge.get()

                if inputName == "" or inputSurname == "" or inputGender == "" or inputAge == "":
                    errorPopUp("Please fill all of the elements.")
                elif len((inputName + inputSurname + inputAge + inputGender).split()) != 1:
                    errorPopUp("Space character is not allowed in elements")
                elif not inputAge.isdigit():
                    errorPopUp("Age should be numeric")
                else:
                    sqlCursor.execute(f"""
                                    UPDATE owner SET ownerName = "{inputName}", ownerSurname = "{inputSurname}", 
                                        gender = "{inputGender}", age = {inputAge} WHERE ownerName =
                                        "{ownerInformation[0][1]}" AND ownerSurname = "{ownerInformation[0][2]}"
                                    """)
                    newOwnerName = inputName + " " + inputSurname
                    oldOwnerName = ownerInformation[0][1] + " " + ownerInformation[0][2]
                    sqlCursor.execute(f"""
                                    UPDATE building SET owner = "{newOwnerName}" WHERE owner = "{oldOwnerName}"
                                    """)
                    sqlConnection.commit()
                    getBack2Main()
                    successPopUp("Owner information is updated.")

            ownerEditSubmitButton = ttk.Button(ownerFrame, text="Submit", command=ownerEditSubmitButtonFunc)
            ownerEditSubmitButton.grid(row=7, column=2)

        ownerEditButton = ttk.Button(ownerFrame, text="Edit Owner", command=ownerEditButtonFunc)
        ownerEditButton.grid(row=3, column=2)

    elif selectedOperation == "Delete":
        ownerDeleteLabel = tkinter.Label(ownerFrame, text="Select a owner to delete:   ")
        ownerDeleteLabel.grid(row=3, column=0)

        sqlCursor.execute("SELECT ownerName, ownerSurname FROM owner")
        ownerFullNames = list()
        for name, surname in sqlCursor:
            ownerFullNames.append(name + " " + surname)

        ownerDeleteCombobox = ttk.Combobox(ownerFrame, state="readonly", values=ownerFullNames)
        ownerDeleteCombobox.grid(row=3, column=1)

        def ownerDeleteButtonFunc():
            selectedOwner = ownerDeleteCombobox.get()
            ownerName, ownerSurname = selectedOwner.split()
            sqlCursor.execute(
                f"DELETE FROM owner WHERE ownerName = '{ownerName}' AND ownerSurname = '{ownerSurname}'")
            sqlCursor.execute(f"UPDATE building SET owner = '<No Owner>' WHERE owner = '{selectedOwner}'")

            sqlConnection.commit()
            getBack2Main()
            successPopUp("Selected owner is deleted.")


        ownerDeleteButton = ttk.Button(ownerFrame, text="Delete Owner", command=ownerDeleteButtonFunc)
        ownerDeleteButton.grid(row=3, column=2)

    elif selectedOperation == "List Information":
        ownerListLabel = tkinter.Label(ownerFrame, text="Select a owner to list its information:   ")
        ownerListLabel.grid(row=3, column=0)

        sqlCursor.execute("SELECT ownerName, ownerSurname FROM owner")
        ownerFullNames = list()
        for name, surname in sqlCursor:
            ownerFullNames.append(name + " " + surname)

        ownerListCombobox = ttk.Combobox(ownerFrame, state="readonly", values=ownerFullNames)
        ownerListCombobox.grid(row=3, column=1)

        def ownerListButtonFunc():
            nonlocal isListed

            selectedOwner = ownerListCombobox.get()
            ownerName, ownerSurname = selectedOwner.split()
            sqlCursor.execute(f"SELECT * FROM owner WHERE ownerName = '{ownerName}' AND ownerSurname = '{ownerSurname}'")
            ownerInformation = sqlCursor.fetchall()

            tkinter.Label(ownerFrame, text="ID:  ").grid(row=4, column=0)
            tkinter.Label(ownerFrame, text=ownerInformation[0][0]).grid(row=4, column=1)
            tkinter.Label(ownerFrame, text="Name:  ").grid(row=5, column=0)
            tkinter.Label(ownerFrame, text=ownerInformation[0][1]).grid(row=5, column=1)
            tkinter.Label(ownerFrame, text="Surname:  ").grid(row=6, column=0)
            tkinter.Label(ownerFrame, text=ownerInformation[0][2]).grid(row=6, column=1)
            tkinter.Label(ownerFrame, text="Gender:  ").grid(row=7, column=0)
            tkinter.Label(ownerFrame, text=ownerInformation[0][3]).grid(row=7, column=1)
            tkinter.Label(ownerFrame, text="Age:  ").grid(row=8, column=0)
            tkinter.Label(ownerFrame, text=ownerInformation[0][4]).grid(row=8, column=1)

            # reset gui
            if isListed:
                resetOwnerFrame()
                isListed = False
            else:
                ownerListButton.config(text="Clear")
                isListed = True
        isListed = False
        ownerListButton = ttk.Button(ownerFrame, text="List Information", command=ownerListButtonFunc)
        ownerListButton.grid(row=3, column=2)


def buildingSelectButtonFunc():
    selectedBuilding = buildingSelectCombobox.get()
    if selectedBuilding == "":
        return
    resetBuildingFrame()
    tkinter.Label(buildingFrame, text="--------").grid(row=2, column=1)
    sqlCursor.execute(f"SELECT * FROM building WHERE name = '{selectedBuilding}'")
    buildingInfo = sqlCursor.fetchall()

    tkinter.Label(buildingFrame, text="Name:").grid(row=4, column=0)
    tkinter.Label(buildingFrame, text=buildingInfo[0][2]).grid(row=4, column=1)
    tkinter.Label(buildingFrame, text="Owner:").grid(row=5, column=0)
    tkinter.Label(buildingFrame, text=buildingInfo[0][1]).grid(row=5, column=1)
    tkinter.Label(buildingFrame, text="Number:").grid(row=6, column=0)
    tkinter.Label(buildingFrame, text=buildingInfo[0][3]).grid(row=6, column=1)
    tkinter.Label(buildingFrame, text="Address:").grid(row=7, column=0)
    tkinter.Label(buildingFrame, text=buildingInfo[0][4]).grid(row=7, column=1)
    tkinter.Label(buildingFrame, text="Coordinates:").grid(row=8, column=0)
    tkinter.Label(buildingFrame, text=buildingInfo[0][5]).grid(row=8, column=1)

    # code below can be improved so that already added info can be edited
    tkinter.Label(buildingFrame, text="Floors:").grid(row=9, column=0)
    buildingFloor = ttk.Entry(buildingFrame)
    buildingFloor.grid(row=9, column=1)
    tkinter.Label(buildingFrame, text="Square:").grid(row=10, column=0)
    buildingSquare = ttk.Entry(buildingFrame)
    buildingSquare.grid(row=10, column=1)
    tkinter.Label(buildingFrame, text="Year:").grid(row=11, column=0)
    buildingYear = ttk.Entry(buildingFrame)
    buildingYear.grid(row=11, column=1)
    tkinter.Label(buildingFrame, text="Zone:").grid(row=12, column=0)
    buildingZone = ttk.Combobox(buildingFrame, state="readonly", values=["1", "2", "3", "4"])
    buildingZone.grid(row=12, column=1)
    tkinter.Label(buildingFrame, text="Type:").grid(row=13, column=0)
    buildingType = ttk.Combobox(buildingFrame, state="readonly", values=["reinforced concrete", "masonry"])
    buildingType.grid(row=13, column=1)
    tkinter.Label(buildingFrame, text="Geometry:").grid(row=14, column=0)
    buildingGeometry = ttk.Combobox(buildingFrame, state="readonly", values=["regular", "irregular"])
    buildingGeometry.grid(row=14, column=1)
    tkinter.Label(buildingFrame, text="Has Basement:").grid(row=15, column=0)
    buildingBasement = ttk.Combobox(buildingFrame, state="readonly", values=["true", "false"])
    buildingBasement.grid(row=15, column=1)
    tkinter.Label(buildingFrame, text="Width (meter):").grid(row=16, column=0)
    buildingWidth = ttk.Entry(buildingFrame)
    buildingWidth.grid(row=16, column=1)
    tkinter.Label(buildingFrame, text="Length (meter):").grid(row=17, column=0)
    buildingLength = ttk.Entry(buildingFrame)
    buildingLength.grid(row=17, column=1)
    tkinter.Label(buildingFrame, text="Damaged:").grid(row=18, column=0)
    buildingDamaged = ttk.Combobox(buildingFrame, state="readonly", values=["true", "false"])
    buildingDamaged.grid(row=18, column=1)


    def buildingSubmit():
        floor = buildingFloor.get()
        square = buildingSquare.get()
        year = buildingYear.get()
        zone = buildingZone.get()
        type_ = buildingType.get()
        geometry = buildingGeometry.get()
        basement = buildingBasement.get()
        width = buildingWidth.get()
        length = buildingLength.get()
        damaged = buildingDamaged.get()

        if floor == "" or square == "" or year == "" or zone == "" or type_ == "" or geometry == "" or basement == "" \
                or width == "" or length == "" or damaged == "":
            errorPopUp("Please fill all of the elements.")
            return
        elif not floor.isdigit():
            errorPopUp("Floor count should be numeric.")
            return
        elif not square.isdigit():
            errorPopUp("Square should be numeric")
            return
        elif not year.isdigit():
            errorPopUp("Year should be numeric")
            return
        elif not width.isdigit():
            errorPopUp("Width should be numeric")
            return
        elif not length.isdigit():
            errorPopUp("Length should be numeric")
            return
        else:
            # calculating risk score
            floor = int(floor)
            square = int(square)
            year = int(year)
            zone = int(zone)
            width = int(width)
            length = int(length)

            point = 100
            if type_ == "reinforced concrete":
                point += 30
            else:
                point -= 15

            if 0 <= floor < 4:
                point += 10
            elif 4 <= floor < 7:
                point += 5
            else:
                point -= 5

            if 0 <= square < 100:
                point += 5
            else:
                point -= 5

            if year < 2000 and damaged == "true":
                point -= 5
            elif year >= 2000:
                if damaged == "true":
                    point -= 3
                else:
                    point += 5

            point += zone * 5

            if geometry == "regular":
                point += 10
            else:
                point -= 5

            if basement == "true":
                point -= 8
            else:
                point += 2

            if width/length < 0.5:
                point -= 3
            else:
                point += 3

            sqlCursor.execute(f"""
                INSERT INTO features VALUES ("{selectedBuilding}", {floor}, {square}, {year}, {zone}, "{type_}",
                "{geometry}", "{basement}", {width}, {length}, "{damaged}", {point})
                """)
            sqlConnection.commit()
            getBack2Main()
            successPopUp("Risk point has calculated and information is added to the database.")

    ttk.Button(buildingFrame, text="Submit", command=buildingSubmit).grid(row=18, column=2)


createTables()  # if database does not exist

# tkinter main window
window = tkinter.Tk()
window.title("Building Inventory and Earthquake Risk Score Calculation")
window.protocol("WM_DELETE_WINDOW", closingSection)
# window.geometry("500x650")

# main menu part
mainFrame = tkinter.Frame(window)
setMainFrame()

# building owner part
ownerFrame = tkinter.Frame(window)
ownerFrame.grid(row=0, column=0)
ownerSelectCombobox = ttk.Combobox(ownerFrame, state="readonly", values=["Add", "Edit", "Delete", "List Information"])

# building information part
buildingFrame = tkinter.Frame(window)
buildingFrame.grid(row=0, column=0)
buildingSelectCombobox = ttk.Combobox(buildingFrame, state="readonly", values=[])

# back to main menu
backFrame = tkinter.Frame(window)
backFrame.grid(row=1, column=0)


window.mainloop()
