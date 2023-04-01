import mysql.connector
import os

mydb = mysql.connector.connect(
  host="db",
  user="root",
  password=os.environ.get("MYSQL_ROOT_PASSWORD"),
  database="biup"
)

mycursor = mydb.cursor()

mycursor.execute("SHOW TABLES")


print(mycursor)
for x in mycursor:
  print(x)

mycursor.execute("CREATE TABLE business_types (initcap VARCHAR(64), active BOOLEAN, business_type_id INT PRIMARY KEY)")

mycursor.execute("CREATE TABLE customers (customer_id INT PRIMARY KEY, email_address VARCHAR(255), name VARCHAR(128), business_type_id INT, site_code VARCHAR(3), archived BOOLEAN, is_key_account BOOLEAN, date_updated DATETIME, date_created DATETIME)")

mycursor.execute("CREATE TABLE orders (id INT PRIMARY KEY AUTO_INCREMENT, order_id INT, batch_id INT, created_date DATETIME, updated_date DATETIME, submitted_date DATETIME, delivery_date DATE, customer_id INT, site_code VARCHAR(8), total DECIMAL(8,1), total_shipping DECIMAL(8,1), tracking_code VARCHAR(64), order_status VARCHAR(128), gmv_enabled BOOLEAN, order_number VARCHAR(128), shipping_by_tracking DECIMAL(8,1), latitude FLOAT, longitude FLOAT)")
