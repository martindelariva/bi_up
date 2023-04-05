from urllib.request import urlopen
import json

APP_ID = 'a5168d8367574abfa3502091cc37cf7f'
URL = 'https://openexchangerates.org/api/historical/'

def get_date_rate(date):
    url = f'{URL}{date}.json?app_id={APP_ID}'
    print(url)
    response = urlopen(url)
    return (response.read())
    #data_json = json.loads(response.read())
    #print(data_json)
