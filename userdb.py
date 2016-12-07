import sqlite3
import json

class UserDB:

    def __init__(self):
        pass

    def GetUsersByEmail(self):
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()
        cursor.execute("SELECT email from users")
        result = cursor.fetchall()
        return result

    def ParseDictionary(self,data):
        values = ["", "", "", ""]
        print(values)
        for key in data:
            if key == "email":
                values[0] = data.get(key)[0]
            if key == "password":
                values[1] = data.get(key)[0]
            if key == "fname":
                values[2] = data.get(key)[0]
            if key == "lname":
                values[3] = data.get(key)[0]
        return values

    def RowFact(self, cursor, row):
        d = {}
        for idX, col in enumerate(cursor.description):
            d[col[0]] = row[idX]
        return d

    def GetPath(self, idPath):
        i = -1
        endChar = idPath[i]
        while endChar != "/":
            i -= 1
            endChar = idPath[i]
        personID = idPath[i+1:]
        return personID

    def AddUser(self,UserInfo):
        UserInfo = self.ParseDictionary(UserInfo)
        connection = sqlite3.connect("users.db")
        connection.row_factory = self.RowFact
        cursor = connection.cursor()
        print(UserInfo)
        cursor.execute("INSERT INTO users (email,password,fname,lname) VALUES (?,?,?,?)",(UserInfo[0],UserInfo[1],UserInfo[2],UserInfo[3]))
        connection.commit()
        cursor.execute("SELECT * FROM users;")
        rows = cursor.fetchall()
        connection.close()
        return json.dumps(rows)

    def GetUser(self, idPath):
        personID = idPath[0]
        connection = sqlite3.connect("users.db")
        connection.row_factory = self.RowFact
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = (?)", (personID,))
        rows = cursor.fetchall()
        connection.close()
        return rows

    def GetALLUsersInfo(self):
        connection = sqlite3.connect("users.db")
        connection.row_factory = self.RowFact
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        connection.close()
        return json.dumps(rows)
