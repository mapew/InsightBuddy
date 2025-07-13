import sqlite3

def create_table():
    conn = sqlite3.connect("research.db")
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS queries(
                   id INTEGER PRIMARY KEY,
                   question TEXT,
                   answer TEXT,
                   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
    ''')

    conn.commit()
    conn.close()

def show_all_data():
    conn = sqlite3.connect("research.db")
    cursor = conn.cursor()

    cursor.execute('select * from queries')

    queries = cursor.fetchall()

    for query in queries:
        print(query)

    conn.close()


#this function is to create db table, please use this function first before start the app
create_table()

show_all_data()
