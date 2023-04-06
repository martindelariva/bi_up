import mysql.connector
import os

mydb = mysql.connector.connect(
  host="db",
  user="root",
  password=os.environ.get("MYSQL_ROOT_PASSWORD"),
  database="biup"
)
mydwh = mysql.connector.connect(
  host="dwh-db",
  user="root",
  password=os.environ.get("MYSQL_ROOT_PASSWORD"),
  database="biup"
)

mycursor = mydb.cursor()
dwhcursor = mydwh.cursor()


mycursor.execute("CREATE TABLE IF NOT EXISTS business_types (initcap VARCHAR(64), active BOOLEAN, business_type_id INT PRIMARY KEY)")

mycursor.execute("CREATE TABLE IF NOT EXISTS customers (customer_id INT PRIMARY KEY, email_address VARCHAR(255), name VARCHAR(128), \
                 business_type_id INT, site_code VARCHAR(3), archived BOOLEAN, is_key_account BOOLEAN, date_updated DATETIME, date_created DATETIME)")

mycursor.execute("CREATE TABLE IF NOT EXISTS orders (id INT PRIMARY KEY AUTO_INCREMENT, order_id INT, batch_id INT, created_date DATETIME, \
                 updated_date DATETIME, submitted_date DATETIME, delivery_date DATE, customer_id INT, site_code VARCHAR(8), total DECIMAL(8,1), \
                 total_shipping DECIMAL(8,1), tracking_code VARCHAR(64), order_status VARCHAR(128), gmv_enabled BOOLEAN, order_number VARCHAR(128), \
                 shipping_by_tracking DECIMAL(8,1), latitude FLOAT, longitude FLOAT)")

mycursor.execute("CREATE TABLE IF NOT EXISTS currency_codes (id INT PRIMARY KEY AUTO_INCREMENT, entity VARCHAR(128), currency VARCHAR(128), \
                 alphabetic_code CHAR(3) NULL, numeric_code INT NULL, minor_unit VARCHAR(3) NULL)")

mycursor.execute("CREATE TABLE IF NOT EXISTS site_codes (site_code CHAR(3) PRIMARY KEY, city_name VARCHAR(128), country_name VARCHAR(128) NULL, \
                 continent CHAR(2), iso_country CHAR(2) NULL)")

mycursor.execute("CREATE TABLE IF NOT EXISTS exchange (id INT PRIMARY KEY AUTO_INCREMENT, rate_day DATE NOT NULL, currency_code CHAR(3) NOT NULL, \
                 currency_x_usd DECIMAL(14,7) NOT NULL)")

dwhcursor.execute("CREATE TABLE IF NOT EXISTS sales_fact (id INT PRIMARY KEY AUTO_INCREMENT, business_name_type VARCHAR(64), \
  customer_site_code VARCHAR(3), customer_archived BOOLEAN, is_key_account BOOLEAN, customer_notfound BOOLEAN, \
  submitted_date DATETIME, submitted_date_hr INT, submitted_date_dow INT, submitted_date_day INT, submitted_date_mon INT, \
  submitted_date_year INT, delivery_date DATETIME, delivery_date_dow INT, delivery_date_day INT, \
  delivery_date_mon INT, delivery_date_year INT, customer_id INT, site_code VARCHAR(3), total DECIMAL(8,1), total_shipping DECIMAL(8,1), \
  order_status VARCHAR(128), gmv_enabled BOOLEAN, total_usd DECIMAL(8,2), total_shipping_usd DECIMAL(8,2), country_name VARCHAR(128), \
  country_currency VARCHAR(3), currency_x_usd DECIMAL(14,7))")

mycursor.execute("SHOW TABLES")