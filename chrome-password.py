import sqlite3
from sqlite3 import Error
import getpass
import json
import threading

login_data = list()
top_sites = list()
history = list()
bookmarks = list()

class Bookmarks:
    def __init__(self,date,name,url):
        self.name = name
        self.date = date
        self.url = url

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
    freezeDatabse(conn)
    cur = conn.cursor()
    cur.execute("SELECT origin_url FROM logins")

    rows = cur.fetchall()

    for row in rows:
        #print(row)
        login_data.append(row)
        # with open("password.txt",'wb') as file:
        #     file.write(row[1])


def getHistory(conn):
    freezeDatabse(conn)
    cur = conn.cursor()
    cur.execute("SELECT * FROM downloads")

    rows = cur.fetchall()

    for row in rows:
        #print(row)
        history.append(row)


def getTopSites(conn):
    freezeDatabse(conn)
    cur = conn.cursor()
    cur.execute("SELECT * FROM top_sites")

    rows = cur.fetchall()

    for row in rows:
        #print(row)
        history.append(row)


def getBookmarks():
    path = '/home/'+user+'/.config/google-chrome/Default/Bookmarks'
    with open(path) as json_file:
        data = json.load(json_file)
    roots = data['roots']
    book_marks_bar = roots['bookmark_bar']
    children = book_marks_bar['children']
    for p in children:
       # print(p)
        bookmarks.append(Bookmarks(p['date_added'],p['name'],p['url']))
    # freezeDatabse()
    # cur = conn.cursor()
    # cur.execute("SELECT * FROM bookmarks")

    # rows = cur.fetchall()

    # for row in rows:
    #     print(row)
    #     history.append(row)

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
                # create a database connection for 'Bookmarks'
                with conn:
                    print("Get Bookmarks")
                    thread4 = threading.Thread(target=getBookmarks())
                    thread4.start()
            finally:
                print(login_data)
    
if __name__ == '__main__':
    user = getpass.getuser()
    print(user)
    main()
