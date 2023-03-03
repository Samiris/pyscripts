import pyodbc
from concurrent.futures import ThreadPoolExecutor

threads = 1
query = "SELECT TOP 2 * FROM [dev].[Card]"

def connect_to_database():
    connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'SERVER=localhost;'
                      'DATABASE=dev;'
                      'Trusted_Connection=yes;')
    return connection

def execute_query(query, connection):
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results


def getResults(connection):
   results = execute_query(query, connection)
   for value in results:
        print(f"{value.CardId or ''} {value.Encrypted or ''}")


def task(connection):
    getResults(connection)
    

with ThreadPoolExecutor() as executor:
    for i in range(threads):
        connection = connect_to_database()
        executor.submit(task(connection))
        print("=================")
        connection.close()