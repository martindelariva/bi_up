import csv
import os
import shutil
import datetime
import mysql.connector

mydb = mysql.connector.connect(
  host="db",
  user="root",
  password=os.environ.get("MYSQL_ROOT_PASSWORD"),
  database="biup"
)
mycursor = mydb.cursor()

FILES_PATH = '/load/files/'
csvfiles = []

for path in os.listdir(FILES_PATH):
    print(path)
    if path[-3:] == 'csv':
        #print('Encontrado csv')
        csvfiles.append(path)

print(f'Found: {csvfiles}')

for csvfile_name in csvfiles:
    print(f'  Procesing file: {csvfile_name}')
    csv_file = open(FILES_PATH+csvfile_name)
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    last_col_empy = False
    for row in csv_reader:
        if line_count == 0:
            colnum = 0
            city_codes_check = False
            print(f'    Column names are {", ".join(row)}')
            line_count += 1
            fields = row
            for column in row:
                if column == 'site_code':
                    city_codes_col = colnum
                    city_codes_check = True
                    #print(f'encontrado site_code en {city_codes_col}')
                colnum += 1
            #print (f'    last element:->{row[-1]}<-')
            if row[-1]=='':
                #print('ultimo vacio')
                last_col_empy = True
                fields = fields [:-1]
        else:
            line_count += 1
            #print(row)
            values_str = ''
            colnum = 0
            for value in row:
                #print(f'citt_codes_check = {city_codes_check} - city_codes_col = {city_codes_col}')
                if value == 'True' or value == 'true':
                    values_str = f'{values_str}True,'
                elif value == 'False' or value == 'false':
                    values_str = f'{values_str}False,'
                elif city_codes_check and colnum == city_codes_col:
                    if len(value) > 3:
                        values_str = f'{values_str}"0",'
                        #print(f'Entre en excepcion de site_code. values_str = {values_str} ')
                    else:
                        values_str = f'{values_str}"{value}",'
                elif value == '':
                    values_str = f'{values_str}"0",'
                else:
                    values_str = f'{values_str}"{value}",'
                #print(f'value_string = {values_str}')
                colnum += 1
            if last_col_empy:
                values_str = values_str[:-4]                
                #print(f'{values_str} - {values_str[:-3]}')
            sql_string = f'INSERT INTO {csvfile_name[:-4]} ({",".join(fields)}) VALUES ({values_str[:-1]})'
            #print(sql_string)
            mycursor.execute(sql_string)
    print(f'    Processed in file {csvfile_name}: {line_count-1} records.\n')
    t=datetime.datetime.now()
    shutil.move(FILES_PATH+csvfile_name, f'{FILES_PATH}{csvfile_name}-{t.year}-{t.month}-{t.day}_{t.hour}-{t.minute}')
mydb.commit()
mycursor.close()


# https://docs.openexchangerates.org/reference/historical-json
# https://openexchangerates.org/api/historical/2022-01-01.json?app_id=a5168d8367574abfa3502091cc37cf7f
