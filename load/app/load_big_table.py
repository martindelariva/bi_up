import os
import mysql.connector

mydb = mysql.connector.connect(
  host="db",
  user="root",
  password=os.environ.get("MYSQL_ROOT_PASSWORD"),
  database="biup"
)
mycursor = mydb.cursor()