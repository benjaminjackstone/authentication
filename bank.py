import time
import json
import sqlite3

class Bank:
    
    def getPath(self, path):
        i = -1
        lastch = path[i]
        while lastch != "/":
            i -= 1
            lastch = path[i]
        cid = path[i + 1:]
        return cid

    def parseDict(self,data):
        values = ["", "", "", "", "", "","", "", ""]
        for key in data:
            if key == "ID":
                values[0] = (data.get(key)[0])
            if key == "fname":
                values[1] = (data.get(key)[0])
            if key == "lname":
                values[2] = (data.get(key)[0])
            if key == "age":
                values[3] = data.get(key)[0]
            if key == "acct_number":
                values[4] = data.get(key)[0]
            if key == "balance":
                values[5] = data.get(key)[0]
            if key == "acct_type":
                values[6] = (data.get(key)[0])
            if key == "phone_number":
                values[7] = (data.get(key)[0])
            if key == "time":
                values[8] = (data.get(key)[0])
        return values

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def getIDS(self):
        connection = sqlite3.connect("bankDB.db")
        connection.row_factory = self.dict_factory
        cursor = connection.cursor()
        cursor.execute("SELECT ID FROM customers")
        rows = cursor.fetchall()
        connection.close()
        json_data = json.dumps(rows)
        return json_data

    def getCustomerInfo(self, path):
        cid = self.getPath(path)
        connection = sqlite3.connect("bankDB.db")
        connection.row_factory = self.dict_factory
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM customers WHERE ID = (?)", (cid,))
        rows = cursor.fetchall()
        connection.close()
        json_data = json.dumps(rows)
        return json_data

    def getAllCustomers(self):
        connection = sqlite3.connect("bankDB.db")
        connection.row_factory = self.dict_factory
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM customers")
        rows = cursor.fetchall()
        #row factory for tuple into dictionary then into json
        connection.close()
        json_data = json.dumps(rows)
        return json_data

    def deleteCustomer(self, path):
        cid = self.getPath(path)
        print("IS IT FREAKING DELETING?.................................")
        connection = sqlite3.connect("bankDB.db")
        connection.row_factory = self.dict_factory
        cursor = connection.cursor()
        cursor.execute("DELETE FROM customers WHERE ID = (?)", (cid,))
        connection.commit()
        # rows = cursor.fetchall()
        # connection.close()
        # return json.dumps(bytes(rows))
        return

    def updateCustomer(self, path, data):
        cid = self.getPath(path)
        values = self.parseDict(data)
        print(values, "HELLO...................................")
        connection = sqlite3.connect("bankDB.db")
        connection.row_factory = self.dict_factory
        cursor = connection.cursor()
        cursor.execute("UPDATE customers SET fname=?,lname=?,age=?,acct_number=?,"
                       "balance=?,acct_type=?,phone_number=? WHERE ID =?",
                       (values[1],values[2],values[3],values[4],values[5],values[6],values[7],cid))
        connection.commit()
        rows = cursor.fetchall()
        connection.close()
        json_data = json.dumps(rows)
        return json_data

    def insertCustomer(self, customer):
        opentime = time.strftime("%d/%m/%Y")
        print(customer, "ADDING NEW CUSTOMER")
        customer = self.parseDict(customer)
        connection = sqlite3.connect("bankDB.db")
        connection.row_factory = self.dict_factory
        cursor = connection.cursor()
        cursor.execute("INSERT INTO customers(fname, lname,age,acct_number,balance,acct_type,phone_number, time) VALUES(?,?,?,?,?,?,?,?)",
                       (customer[1], customer[2], customer[3],
                        customer[4], customer[5], customer[6], customer[7], opentime))
        connection.commit()
        connection.close()
