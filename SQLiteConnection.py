from DataReader import *
from constants.cacheconstants import *
import sqlite3

'''
The SQLiteConnection class is responsible for connecting to the database stored in
the DBPATH defined in cacheconstants.py.

It is also responsible for:
1) automatically adding tables, one for each raw data file, if the DB is empty
2) adding rows to the database
3) retrieving rows from the database
4) updating rows
'''
class SQLiteConnection:
    def __init__(self, path: str):
        self.path = path
        self.con = sqlite3.connect(path)

        self.tables = self.getTableNames()
        if self.tables != FILENAMES:
            self.initTables()
            self.tables = self.getTableNames()

    '''
    This method processes tuples received from SQL queries into RowModels
    '''
    @staticmethod
    def convToRowModels(rows: list) -> list:
        convRows = []
        for row in rows:
            id, msg, label, enc = row
            enc = eval(enc)
            convRow = RowModel(msg, label, enc)
            convRows.append(convRow)
        return convRows

    '''
    This method retrieves all tables currently held in the database. This is used
    to check if tables need to be added.
    '''
    def getTableNames(self) -> list:
        cur = self.con.cursor()
        cur.execute(TABLENAMEQUERY)
        names = cur.fetchall()
        names = [i[0] for i in names]
        return names

    '''
    This method creates tables for all the filenames defined in readconstants.py
    '''
    def initTables(self) -> None:
        for name in FILENAMES:
            self.createTable(name)

    '''
    This method creates a table given a name
    '''
    def createTable(self, name: str) -> None:
        try:
            cur = self.con.cursor()
            cur.execute(CREATETABLEQUERY(name))
        except sqlite3.Error as e:
            print(e)

    '''
    This method adds a row to a given table given a RowModel object.
    Returns 1 on success, 0 on failure
    '''
    def addRow(self, table: str, row: RowModel) -> int:
        try:
            msg, label, encoding = row.msg, row.label, row.encoding
            cur = self.con.cursor()
            cur.execute(ADDROWQUERY(table, msg, label, encoding))
            self.con.commit()
            return 1
        except sqlite3.Error as e:
            print(ADDROWQUERY(table, msg, label, "encoding"))
            print(e, end='\n')
            return 0

    '''
    This method iteratively calls addRow() method and adds multiple rows
    to a given table. Returns the number of successfully added rows.
    '''
    def addRows(self, table: str, rows: list) -> int:
        c = 0
        for row in rows:
            c += self.addRow(table, row)
        return c

    '''
    This method updates a row identified by its unique ID (primary key)
    '''
    def updateRowByid(self, table: str, id: int, row: RowModel) -> None:
        try:
            cur = self.con.cursor()
            msg, label, enc = row.msg, row.label, row.encoding
            cur.execute(UPDATEROWBYIDQUERY(table, msg, label, enc, id))
            self.con.commit()
        except sqlite3.Error as e:
            print(e)

    '''
    This method deletes every row in a given table
    '''
    def deleteContentByTable(self, table: str) -> None:
        try:
            cur = self.con.cursor()
            cur.execute(DELETECONTENTBYTABLEQUERY(table))
            self.con.commit()
        except sqlite3.Error as e:
            print(e)

    '''
    This method retrieves all rows in a given table and returns them as a list of RowModels
    '''
    def getAllRowsByTable(self, table: str) -> list:
        try:
            cur = self.con.cursor()
            cur.execute(GETALLROWSQUERY(table))
            rawRows = cur.fetchall()
            rows = self.convToRowModels(rawRows)
            return rows
        except sqlite3.Error as e:
            print(e)

    '''
    This method returns a flattened list of RowModels for every table (corresponding to every data file)
    '''
    def getAllRows(self) -> list:
        rows = []
        for table in FILENAMES:
            rows += self.getAllRowsByTable(table)
        return rows

    def closeConn(self):
        self.con.close()


