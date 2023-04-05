import openexchange
import os
import mysql.connector
import datetime
import json

mydb = mysql.connector.connect(
  host="db",
  user="root",
  password=os.environ.get("MYSQL_ROOT_PASSWORD"),
  database="biup"
)
mycursor = mydb.cursor()

mycursor.execute("SELECT submitted_date FROM orders ORDER BY submitted_date")

myresult = mycursor.fetchall()

for record in myresult:
    submitted_date = record[0].strftime('%Y-%m-%d')
    sql_select = f'SELECT * FROM exchange WHERE rate_day = "{submitted_date}" limit 1'
    #print(sql_select)
    mycursor.execute(sql_select)
    check_exchange = mycursor.fetchall()
    if (len(check_exchange)) == 0:
        print(f'Quering API for rate exchanges in: {submitted_date}')
        json_exchange = json.loads(openexchange.get_date_rate(submitted_date))
        for currency_code, rate_value in json_exchange['rates'].items():
            sql_string = f'INSERT INTO exchange (rate_day, currency_code, currency_x_usd) VALUES ("{submitted_date}", "{currency_code}", "{rate_value}")'
            #print(sql_string)
            mycursor.execute(sql_string)
            mydb.commit()


