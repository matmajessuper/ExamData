import json
import sqlite3
import requests


class Row:
    def __init__(self, tup):
        self.tuple = tup
        self.territory = tup[0]
        self.passed_attended = tup[1]
        self.sex = tup[2]
        self.year = tup[3]
        self.people_number = tup[4]


class DBapi:
    database = "data.db"

    def create_connection(self):
        try:
            conn = sqlite3.connect(self.database)
            return conn
        except sqlite3.Error as e:
            print(e)

        return None

    def __init__(self, db=None):
        if db:
            self.database = db
        self.conn = self.create_connection()

    def create_tables(self):
        sql = '''CREATE TABLE exam_data (id Integer Primary key autoincrement, territory varchar(30), 
                  passed_attended varchar(15), sex varchar(15), year integer, people_number integer);'''
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()

    def insert_data(self, data):
        sql = '''insert into exam_data (territory, passed_attended, sex, year, people_number) VALUES(?,?,?,?,?);'''
        cur = self.conn.cursor()
        cur.executemany(sql, data)
        self.conn.commit()

    def request_and_insert_data(self):
        data = json.loads(requests.get("http://api.dane.gov.pl/resources/17363/data?page=1").text)
        selflink = data['links']['self']
        lastlink = data['links']['last']
        nextlink = selflink

        while selflink != lastlink:
            dictionary = json.loads(requests.get(nextlink).text)
            selflink = dictionary['links']['self']
            values = []

            for row in dictionary['data']:
                data = Row((row['attributes']['col1'], row['attributes']['col2'], row['attributes']['col3'],
                           int(row['attributes']['col4']), int(row['attributes']['col5']),))
                values.append(data.tuple)

            self.insert_data(values)

            if selflink != lastlink:
                nextlink = dictionary['links']['next']
            print('Please wait, downloading data...')

        self.conn.close()

    def select_data(self, query, data=None):
        cur = self.conn.cursor()
        if data:
            cur.execute(query, data)
        else:
            cur.execute(query)

        rows = cur.fetchall()

        return rows




