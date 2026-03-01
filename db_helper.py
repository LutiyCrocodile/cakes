import pymysql.cursors
from dotenv import load_dotenv
import pymysql as pms
import os

load_dotenv()

class DB_Helper:
    def __init__(self):
        self.DB_HOST = os.environ.get("HOST")
        self.DB_USER = os.environ.get("USER")
        self.DB_PASSWORD = os.environ.get("PASSWORD")
        self.DB_NAME = os.environ.get("NAME")

    def query(self, query):
        try:
            with pms.connect(
                host=self.DB_HOST,
                user=self.DB_USER,
                password=self.DB_PASSWORD,
                database=self.DB_NAME,
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True
            ) as self.conn:
                self.curs = self.conn.cursor()
                self.curs.execute(query)
                self.res = self.curs.fetchall()
                # print(*self.res, sep="\n")
                return self.res
        except Exception as e:
            print(e)

    def query_params(self, query, params):
        try:
            with pms.connect(
                host=self.DB_HOST,
                user=self.DB_USER,
                password=self.DB_PASSWORD,
                database=self.DB_NAME,
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True
            ) as self.conn:
                self.curs = self.conn.cursor()
                self.curs.execute(query, params)
                self.res = self.curs.fetchall()
                # print(*self.res, sep="\n")
                return self.res
        except Exception as e:
            print(e)

db = DB_Helper()

