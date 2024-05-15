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
    sqlCursor.execute("CREATE TABLE IF NOT EXISTS features(floors, square, year, zone, type, geometry, isBasement, "
                      "width, length, damaged, risk);")  # building features table
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
            (1, "Henry Blackburne", "AA", 11, "Province1, District1, Neighbourhood1, Street1", "0, 0"),
            (2, "Henry Blackburne", "BB", 12, "Province2, District2, Neighbourhood2, Street2", "0, 1"),
            (3, "Henry Blackburne", "CC", 13, "Province3, District3, Neighbourhood3, Street3", "0, 2"),
            (4, "Emily Scarlett", "DD", 14, "Province4, District4, Neighbourhood4, Street4", "1, 0"),
            (5, "Emily Scarlett", "EE", 15, "Province5, District5, Neighbourhood5, Street5", "1, 1"),
            (6, "Emily Scarlett", "FF", 16, "Province6, District6, Neighbourhood6, Street6", "1, 2"),
            (7, "Diva Smith", "GG", 17, "Province, District7, Neighbourhood7, Street7", "2, 0"),
            (8, "Diva Smith", "HH", 18, "Province8, District8, Neighbourhood8, Street8", "2, 1"),
            (9, "Diva Smith", "II", 19, "Province9, District9, Neighbourhood9, Street9", "2, 2"),
            (10, "John Tractor", "JJ", 20, "Province10, District10, Neighbourhood10, Street10", "3, 0"),
            (11, "John Tractor", "KK", 21, "Province11, District11, Neighbourhood11, Street11", "3, 1"),
            (12, "John Tractor", "LL", 22, "Province12, District12, Neighbourhood12, Street12", "3, 2"),
            (13, "Elliot Pearl", "MM", 23, "Province13, District13, Neighbourhood13, Street13", "4, 0"),
            (14, "Elliot Pearl", "NN", 24, "Province14, District14, Neighbourhood14, Street14", "4, 1"),
            (15, "Elliot Pearl", "OO", 25, "Province15, District15, Neighbourhood15, Street15", "4, 2");
        """)


def resetTables():
    dropTables()
    createTables()
    fillTables()


# GUI
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

tkinter.Label(ownerFrame, text="Building Owner").grid(row=0, column=1)
tkinter.Label(ownerFrame, text="Select Operation:   ").grid(row=1, column=0)
ownerSelectCombobox = ttk.Combobox(ownerFrame, state="readonly", values=["Add", "Edit", "Delete", "List Information"])
ownerSelectCombobox.grid(row=1, column=1)
ttk.Button(ownerFrame, text="OK", command=ownerSelectButtonFunc).grid(row=1, column=2)
tkinter.Label(ownerFrame, text="--------").grid(row=2, column=1)
tkinter.Label(ownerFrame, text="    |   ").grid(row=0, column=4)
tkinter.Label(ownerFrame, text="    |   ").grid(row=1, column=4)
tkinter.Label(ownerFrame, text="    |   ").grid(row=2, column=4)

# building information part
buildingFrame = tkinter.Frame(window)
buildingFrame.grid(row=0, column=1)

tkinter.Label(buildingFrame, text="Building Owner").grid(row=0, column=1)
tkinter.Label(buildingFrame, text="Select Operation:   ").grid(row=1, column=0)

#sqlCursor.execute("SELECT ")
tkinter.Label(buildingFrame, text="--------").grid(row=2, column=1)

ownerFrame.mainloop()

sqlConnection.commit()
sqlConnection.close()

