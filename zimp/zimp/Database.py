# Willems Implementation
import json
import sqlite3
import sys


class Database():
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)

    def create_table(self,
                     table_name: str,
                     list_columns: list[str]) -> None:
        cur = self.conn.cursor()
        columns = ", ".join(list_columns)
        sql = "CREATE TABLE {} ({})".format(table_name, columns)

        try:
            cur.execute(sql)
        except sqlite3.OperationalError:
            self.drop_table(table_name)
            self.conn.commit()
            self.create_table(table_name, list_columns)
        finally:
            self.conn.commit()

    def create_devcards(self) -> None:
        self.create_table("devcards",
                          ["items TEXT",
                           "event_one TEXT",
                           "consquence_one INT",
                           "event_two TEXT",
                           "consquence_two INT",
                           "event_three TEXT",
                           "consquence_three INT",
                           "charges INT"])

    def create_tiles(self) -> None:
        self.create_table("tiles",
                          ["name TEXT",
                           "effect TEXT",
                           "type TEXT",
                           "north INT",
                           "south INT",
                           "east INT",
                           "west INT"])

    def insert_table_data(self, file_name: str) -> None:
        try:
            with open(f"{file_name}.json") as dc:
                data = json.load(dc)
                for item in data:
                    self.insert_data(file_name, item)
        except FileNotFoundError:
            print(f"\nCould not find {file_name}.json"
                  f"\nPlease make sure it is in the same"
                  " directory as this script")
            sys.exit()

    def drop_table(self, table: str) -> None:
        cur = self.conn.cursor()
        sql = "DROP TABLE IF EXISTS {}".format(table)
        cur.execute(sql)
        self.conn.commit()

    def insert_data(self, table_name: str, dict_data: dict) -> None:
        cur = self.conn.cursor()
        columns = ', '.join(dict_data.keys())
        placeholders = tuple(dict_data.values())

        sql = ("INSERT INTO {} ({}) VALUES {}"
               .format(table_name,
                       columns,
                       placeholders))
        try:
            cur.execute(sql)
        except sqlite3.IntegrityError:
            self.conn.rollback()
        except sqlite3.OperationalError:
            self.conn.rollback()
        finally:
            self.conn.commit()

    def select_data(self, table_name: str) -> any:
        cur = self.conn.cursor()
        sql = "SELECT * FROM {}".format(table_name)
        try:
            cur.execute(sql)
            rows = cur.fetchall()
            return rows
        except sqlite3.IntegrityError:
            self.conn.rollback()
        except sqlite3.OperationalError:
            self.conn.rollback()
        finally:
            self.conn.commit()
