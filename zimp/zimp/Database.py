#!/usr/bin/python3
import mysql.connector
from mysql.connector import errorcode

class Database():

    def connect_to_database(self):
        try:
            cnx = mysql.connector.connect(
                    user='root',
                    password='password',
                    database='zimp')
            print("Database connected")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            cnx.close()
            print("connection closed")