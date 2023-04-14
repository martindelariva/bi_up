import os
import mysql.connector

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

dbcursor = mydb.cursor()
dwhcursor = mydwh.cursor()

business_types_dict = {}
temp_sql = f'select initcap, business_type_id FROM business_types'
dbcursor.execute(temp_sql)
tempresult = dbcursor.fetchall()
for temp_record in tempresult:
    business_types_dict[temp_record[1]]=temp_record[0]
print(business_types_dict)

customer_dict = {}
temp_sql = f'select customer_id, name, business_type_id, site_code, archived, is_key_account FROM customers'
dbcursor.execute(temp_sql)
tempresult = dbcursor.fetchall()
for temp_record in tempresult:
    customer_dict[temp_record[0]]={}
    customer_dict[temp_record[0]]['name']=temp_record[1]
    customer_dict[temp_record[0]]['business_type_id']=temp_record[2]
    customer_dict[temp_record[0]]['site_code']=temp_record[3]
    customer_dict[temp_record[0]]['archived']=temp_record[4]
    customer_dict[temp_record[0]]['is_key_account']=temp_record[5]
print(customer_dict)

site_codes_dict = {}
temp_sql = f'select site_code, country_name FROM site_codes'
dbcursor.execute(temp_sql)
tempresult = dbcursor.fetchall()
for temp_record in tempresult:
    site_codes_dict[temp_record[0]]=temp_record[1]
print(site_codes_dict)

currency_codes_dict = {}
temp_sql = f'select entity, alphabetic_code FROM currency_codes'
dbcursor.execute(temp_sql)
tempresult = dbcursor.fetchall()
for temp_record in tempresult:
    if temp_record[0] not in currency_codes_dict.keys():
        currency_codes_dict[temp_record[0]]=temp_record[1]
print(currency_codes_dict)

dbcursor.execute("SELECT submitted_date, delivery_date, customer_id, site_code, total, total_shipping, \
                 order_status, gmv_enabled FROM orders ORDER BY submitted_date")

myresult = dbcursor.fetchall()

total_record_count = len(myresult)
record_count = 0

for record in myresult:

    submitted_date = record[0]
    submitted_date_dow = record[0].weekday()
    submitted_date_hr = record[0].hour
    submitted_date_day = record[0].day
    submitted_date_mon =record[0].month
    submitted_date_year = record[0].year
    delivery_date = record[1]
    delivery_date_dow = record[1].weekday()
    delivery_date_day = record[1].day
    delivery_date_mon =record[1].month
    delivery_date_year = record[1].year
    customer_id = record[2]
    site_code = record[3]
    total = record[4]
    total_shipping = record[5]
    order_status = record[6]
    gmv_enabled = record[7]
    """
    temp_sql = f'select business_types.initcap FROM business_types INNER JOIN customers ON \
                  customers.business_type_id=business_types.business_type_id WHERE customers.customer_id = "{record[2]}"'
    dbcursor.execute(temp_sql)
    business_name_result = dbcursor.fetchall()
    if len(business_name_result)>0:
        business_name_result = business_name_result[0][0]
    else:
        business_name_result = 'UNDEFINED'
    """
    if customer_id in customer_dict.keys() and customer_dict[customer_id]['business_type_id'] in business_types_dict.keys():
        business_name_result = business_types_dict[customer_dict[customer_id]['business_type_id']]
    else:
        business_name_result = 'UNDEFINED'

    #print (business_name_result)
    
    """
    temp_sql = f'select customers.site_code, customers.archived, customers.is_key_account, customers.name FROM customers INNER JOIN orders ON \
                  customers.customer_id=orders.customer_id WHERE customers.customer_id = "{record[2]}" limit 1'
    dbcursor.execute(temp_sql)
    sql_result = dbcursor.fetchall()
    if len(sql_result)>0:
        customer_site_code_result = sql_result[0][0]
        customer_archived = sql_result[0][1]
        is_key_account = sql_result[0][2]
        customer_name = sql_result[0][3]
        customer_notfound = 0
    else:
        customer_notfound = 1
        customer_site_code_result = '000'
        customer_archived = 0
        is_key_account = 0
        customer_name = 'NOT_FOUND'
    """
    if customer_id in customer_dict.keys():
        customer_site_code_result = customer_dict[customer_id]['site_code']
        customer_archived = customer_dict[customer_id]['archived']
        is_key_account = customer_dict[customer_id]['is_key_account']
        customer_name = customer_dict[customer_id]['name']
        customer_notfound = 0
    else:
        customer_notfound = 1
        customer_site_code_result = '000'
        customer_archived = 0
        is_key_account = 0
        customer_name = 'NOT_FOUND'

    #Busqueda de country_code
    """
    temp_sql = f'select country_name FROM site_codes WHERE site_code = "{site_code}"'
    dbcursor.execute(temp_sql)
    sql_result = dbcursor.fetchall()
    if len(sql_result)>0:
        country_name = sql_result[0][0]
    else:
        country_name = 0
    """
    if site_code in site_codes_dict.keys():
        country_name = site_codes_dict[site_code]
    else:
        country_name = 0
    #print (sql_result)

    #Busqueda de currency
    temp_sql = f'select currency_x_usd FROM exchange WHERE \
                  rate_day = "{submitted_date_year}-{submitted_date_mon}-{submitted_date_day}" AND \
                  exchange.currency_code = "{currency_codes_dict[country_name]}" limit 1'
    """
    temp_sql = f'select currency_codes.alphabetic_code, exchange.currency_x_usd FROM exchange INNER JOIN currency_codes ON \
                  currency_codes.alphabetic_code=exchange.currency_code WHERE \
                  exchange.rate_day = "{submitted_date_year}-{submitted_date_mon}-{submitted_date_day}" AND \
                  currency_codes.entity = "{country_name}"'
    """
    dbcursor.execute(temp_sql)
    sql_result = dbcursor.fetchall()
    if len(sql_result)>0:
        country_currency = currency_codes_dict[country_name]
        currency_x_usd = sql_result[0][0]
    else:
        #country_currency = 0
        currency_x_usd = 0
    #print (sql_result)

    #Calculo en USD
    if currency_x_usd != 0:
        total_usd = total / currency_x_usd
        total_shipping_usd = total_shipping / currency_x_usd
    else:
        total_usd = 0
        total_shipping_usd = 0

    sql_insert = f'INSERT INTO sales_fact (business_name_type, customer_site_code, customer_archived, is_key_account, customer_notfound, \
      submitted_date, submitted_date_hr, submitted_date_dow, submitted_date_day, submitted_date_mon, submitted_date_year, delivery_date, \
      delivery_date_dow, delivery_date_day, delivery_date_mon, delivery_date_year, customer_id, customer_name,\
      site_code, total, total_shipping, order_status, gmv_enabled, total_usd, total_shipping_usd, country_name, \
      country_currency, currency_x_usd) VALUES ("{business_name_result}", "{customer_site_code_result}", {customer_archived}, {is_key_account}, \
      {customer_notfound}, "{submitted_date}", "{submitted_date_hr}", "{submitted_date_dow}", "{submitted_date_day}", "{submitted_date_mon}", \
      "{submitted_date_year}", "{delivery_date}", "{delivery_date_dow}", "{delivery_date_day}", "{delivery_date_mon}", \
      "{delivery_date_year}", "{customer_id}", "{customer_name}", "{site_code}", "{total}", "{total_shipping}", "{order_status}", "{gmv_enabled}", "{total_usd}", \
      "{total_shipping_usd}", "{country_name}", "{country_currency}", "{currency_x_usd}" )'
    #print(sql_insert)
    dwhcursor.execute(sql_insert)
    record_count += 1
    if record_count%100 == 0:
        print (f'Proceced {record_count} / {total_record_count} records')

mydwh.commit()
dwhcursor.close()
dbcursor.close()
