import mysql.connector
from pprint import pprint

def main():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="dslevel1_fp"
        )
    except mysql.connector.Error as e:
        print("Connection error:", e)
        return

    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        pprint(tables)
    except mysql.connector.Error as e:
        print("Query error:", e)
    finally:
        cursor.close()
        db.close()

if __name__ == "__main__":
    main()
