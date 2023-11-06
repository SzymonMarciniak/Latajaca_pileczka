import sqlite3


def inicjalize_db():
    update_db("CREATE TABLE game_data (id INTEGER PRIMARY KEY, choosen_class INTEGER, choosen_category TEXT, sub_category TEXT, choosen_lvl INTEGER, points INTEGER)")
    update_db("INSERT INTO game_data (choosen_class, choosen_category, sub_category, choosen_lvl, points) VALUES (?, ?, ? ,?, ?)", ("NULL", "NULL", "NULL", "NULL", 0))
    update_db("CREATE TABLE mouse_data (id INTEGER PRIMARY KEY, pos_y INTEGER)")
    update_db("INSERT INTO mouse_data (id, pos_y) VALUES (?, ?)", (0, 10000))


def execute_query(my_query):
    connection = sqlite3.connect("MyDataBase.db")
    cursor = connection.cursor()
    cursor.execute(my_query)
    results = cursor.fetchall()
    connection.commit()
    connection.close()
    return results


def update_db(query, values = None):
    connection = sqlite3.connect("MyDataBase.db")
    cursor = connection.cursor()
    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)
    connection.commit()
    connection.close()


def set_default_values():
    connection = sqlite3.connect("MyDataBase.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE game_data SET choosen_class = ?, choosen_category = ?, sub_category = ?, choosen_lvl = ?, points = ? WHERE id = 1", ("NULL", "NULL", "NULL", "NULL", 0))
    cursor.execute("UPDATE mouse_data SET id = ?, pos_y = ?", (0, 10000))
    connection.commit()
    connection.close()


def print_all_data():
    connection = sqlite3.connect("MyDataBase.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM game_data")
    results = cursor.fetchall()
    names = [description[0] for description in cursor.description]
    print("\nGame data:")

    for nr in range(0, len(results[0])):
        print(f"{names[nr]} ==> {results[0][nr]}")

    print("\nMouse data:")

    cursor.execute("SELECT * FROM mouse_data")
    results = cursor.fetchall()
    names = [description[0] for description in cursor.description]

    for nr in range(0, len(results[0])):
        print(f"{names[nr]} ==> {results[0][nr]}")
    print()

try:
    inicjalize_db()
except: pass 
set_default_values()
print_all_data()