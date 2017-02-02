from bs4 import BeautifulSoup
from flask import Flask, render_template
from urllib.request import urlopen
import sqlite3
import datetime

app = Flask(__name__)


@app.route('/')
def index():
    url = 'http://www.x-rates.com/table/?from=USD&amount=1'
    page = urlopen(url)
    soup = BeautifulSoup(page, 'lxml')

    currency_table = soup.find(class_='ratesTable')  # finds the table
    currency_table_row = currency_table.find_all('td')  # pulls all the 'td' tags from the 'ratesTable'

    ''' euro_currency[1] = 1.00 USD -> 1.00 EUR
        euro_currency[2] = 1.00 EUR -> 1.00 USD 
    '''
    euro_currency = []
    for tag in currency_table_row[1:3]:
        euro_text = tag.get_text()  # pull only the text from the 'td' tags
        euro_append = euro_currency.append(euro_text)  # append the text

    try:  # Try/Except for inserting into the DB
        conn = sqlite3.connect('currency.sqlite')
        c = conn.cursor()  # cursor
        c.execute('''CREATE TABLE IF NOT EXISTS euro_currency
                    (id INTEGER NOT NULL PRIMARY KEY,
                    date TEXT,
                    time TEXT,
                    usd_to_eur REAL, 
                    eur_to_usd REAL)''')
        
        current_datetime = datetime.datetime.now()
        date = str(current_datetime.date())
        time = (str(current_datetime.hour) + ':' + str(current_datetime.minute) + ':' + str(current_datetime.second))
        c.execute('INSERT INTO euro_currency VALUES (?, ?, ?, ?, ?)', (None, date, time, euro_currency[0], euro_currency[1]))
        conn.commit()

    except Exception as db_insert:
        print('The following error occured inserting into DB: ', db_insert)
    
    try:  # Try/Except for retrieving from the DB 
        euro_retrieve = '''SELECT usd_to_eur
                            FROM euro_currency'''
        output = c.execute(euro_retrieve)

        for euro in output:
            print(euro)

    except Exception as db_pull:
        print('The following error occured retrieving from the DB: ', db_pull)

            
    return render_template('currency.html', euro_currency=euro_currency)
    
if __name__ == '__main__':
    app.run(debug=True)