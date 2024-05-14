import sqlite3
import tkinter
from tkinter import ttk

# sqlite database
sqlConnection = sqlite3.connect("sqlDatabase.db")
sqlCursor = sqlConnection.cursor()


# GUI
def ownerSelectButtonFunc():
    selectedOperation = ownerSelectCombobox.get()
    if selectedOperation == "Add":
        pass
    elif selectedOperation == "Edit":
        pass
    elif selectedOperation == "Delete":
        ownerDeleteLabel = tkinter.Label(window, text="Select a owner to delete:   ")
        ownerDeleteLabel.grid(row=2, column=0)

        sqlCursor.execute("SELECT ownerName, ownerSurname FROM owner")
        ownerFullNames = list()
        for name, surname in sqlCursor:
            ownerFullNames.append(name + " " + surname)

        ownerDeleteCombobox = ttk.Combobox(window, state="readonly", values=ownerFullNames)
        ownerDeleteCombobox.grid(row=2, column=1)

        def ownerDeleteButtonFunc():
            selectedOwner = ownerDeleteCombobox.get()
            ownerName, ownerSurname = selectedOwner.split()
            sqlCursor.execute(f"DELETE FROM owner WHERE ownerName = '{ownerName}'")

        ownerDeleteButton = ttk.Button(window, text="Delete Owner", command=ownerDeleteButtonFunc)
        ownerDeleteButton.grid(row=2, column=2)



window = tkinter.Tk()
window.title("Building Inventory and Earthquake Risk Score Calculation")
# building owner part
ownerLabel = tkinter.Label(window, text="Building Owner")
ownerLabel.grid(row=0, column=0)
ownerSelectLabel = tkinter.Label(window, text="Select Operation:   ")
ownerSelectLabel.grid(row=1, column=0)
ownerSelectCombobox = ttk.Combobox(window, state="readonly", values=["Add", "Edit", "Delete"])
ownerSelectCombobox.grid(row=1, column=1)
ownerSelectButton = ttk.Button(window, text="Get Value", command=ownerSelectButtonFunc)
ownerSelectButton.grid(row=1, column=2)




window.mainloop()







def createTables():  # for creating tables
    sqlCursor.execute("CREATE TABLE IF NOT EXISTS building(id, owner INTEGER, name, number, address, "
                      "coordinate);")  # building table
    sqlCursor.execute("CREATE TABLE IF NOT EXISTS features(floors, square, year, zone, type, geometry, isBasement, "
                      "width, length, damaged, risk);")  # building features table
    sqlCursor.execute("CREATE TABLE IF NOT EXISTS owner(no, ownerName, ownerSurname, gender, age);")  # owner table


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









# createTables()
# fillTables()

#for row in sqlCursor.execute("SELECT * FROM owner"):
 #   print(row)

sqlConnection.commit()
sqlConnection.close()

