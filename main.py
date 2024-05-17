import sqlite3
import tkinter
from tkinter import ttk

# sqlite database
sqlConnection = sqlite3.connect("sqlDatabase.db")
sqlCursor = sqlConnection.cursor()


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
    resetOwnerFrame()
    resetBuildingFrame()


# GUI functions
def resetOwnerFrame():
    global ownerSelectCombobox
    for widget in ownerFrame.winfo_children():
        widget.destroy()
    tkinter.Label(ownerFrame, text="Building Owner").grid(row=0, column=1)
    tkinter.Label(ownerFrame, text="Select Operation:   ").grid(row=1, column=0)
    ownerSelectCombobox = ttk.Combobox(ownerFrame, state="readonly",
                                       values=["Add", "Edit", "Delete", "List Information"])
    ownerSelectCombobox.grid(row=1, column=1)
    ttk.Button(ownerFrame, text="OK", command=ownerSelectButtonFunc).grid(row=1, column=2)
    tkinter.Label(ownerFrame, text="--------").grid(row=2, column=1)
    tkinter.Label(ownerFrame, text="--------").grid(row=2, column=1)
    tkinter.Label(ownerFrame, text="    |   ").grid(row=0, column=4)
    tkinter.Label(ownerFrame, text="    |   ").grid(row=1, column=4)
    tkinter.Label(ownerFrame, text="    |   ").grid(row=2, column=4)


def resetBuildingFrame():
    global buildingSelectCombobox
    for widget in buildingFrame.winfo_children():
        widget.destroy()
    tkinter.Label(buildingFrame, text="Add Building Information").grid(row=0, column=1)
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

    tkinter.Label(buildingFrame, text="--------").grid(row=2, column=1)


def successPopUp(message: str):
    top = tkinter.Toplevel(ownerFrame)
    top.title("Done!")
    tkinter.Label(top, text=message).grid(row=1, column=1)


def errorPopUp(errorMessage: str):
    top = tkinter.Toplevel(ownerFrame)
    top.title("Error!")
    tkinter.Label(top, text=errorMessage).grid(row=1, column=1)


def ownerSelectButtonFunc():
    selectedOperation = ownerSelectCombobox.get()
    resetOwnerFrame()

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
                resetOwnerFrame()
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
                    sqlConnection.commit()
                    resetOwnerFrame()
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
            resetOwnerFrame()
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
    sqlCursor.execute(f"SELECT * FROM building WHERE name = '{selectedBuilding}'")
    buildingInfo = sqlCursor.fetchall()

    tkinter.Label(buildingFrame, text="ID:").grid(row=4, column=0)
    tkinter.Label(buildingFrame, text=buildingInfo[0][0]).grid(row=4, column=1)
    tkinter.Label(buildingFrame, text="Owner:").grid(row=5, column=0)
    tkinter.Label(buildingFrame, text=buildingInfo[0][1]).grid(row=5, column=1)
    tkinter.Label(buildingFrame, text="Number:").grid(row=6, column=0)
    tkinter.Label(buildingFrame, text=buildingInfo[0][3]).grid(row=6, column=1)
    tkinter.Label(buildingFrame, text="Address:").grid(row=7, column=0)
    tkinter.Label(buildingFrame, text=buildingInfo[0][4]).grid(row=7, column=1)
    tkinter.Label(buildingFrame, text="Coordinates:").grid(row=8, column=0)
    tkinter.Label(buildingFrame, text=buildingInfo[0][5]).grid(row=8, column=1)

    # sqlCursor.execute(f"SELECT * FROM features WHERE buildingName = '{selectedBuilding}'")
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
            resetBuildingFrame()
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

            point += zone

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
            resetBuildingFrame()
            successPopUp("Risk point has calculated and information is added to the database.")

    ttk.Button(buildingFrame, text="Submit", command=buildingSubmit).grid(row=18, column=2)


window = tkinter.Tk()
window.title("Building Inventory and Earthquake Risk Score Calculation")

# menu
menu = tkinter.Menu(window)
window.config(menu=menu)
databaseMenu = tkinter.Menu(menu)
menu.add_cascade(label="Database", menu=databaseMenu)
databaseMenu.add_command(label='Reset Database to Initial State', command=resetTables)

# building owner part
ownerFrame = tkinter.Frame(window)
ownerFrame.grid(row=0, column=0)
ownerSelectCombobox = ttk.Combobox(ownerFrame, state="readonly", values=["Add", "Edit", "Delete", "List Information"])
ownerSelectCombobox.grid(row=1, column=1)
resetOwnerFrame()

# building information part
buildingFrame = tkinter.Frame(window)
buildingFrame.grid(row=0, column=1)
buildingSelectCombobox = ttk.Combobox(buildingFrame, state="readonly", values=[])
buildingSelectCombobox.grid(row=1, column=1)
resetBuildingFrame()


ownerFrame.mainloop()

sqlConnection.commit()
sqlConnection.close()

