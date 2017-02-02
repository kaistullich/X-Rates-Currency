from bs4 import BeautifulSoup
from flask import Flask, render_template
from urllib.request import urlopen
import sqlite3

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
                    usd_to_eur REAL, 
                    eur_to_usd REAL)''')

        c.execute('INSERT INTO euro_currency VALUES (?, ?, ?)', (None, euro_currency[0], euro_currency[1]))
        conn.commit()

    except Exception as db_insert:
        print('The following error occured inserting into DB: ', db_insert)

            
    return render_template('currency.html', euro_currency=euro_currency)
    
if __name__ == '__main__':
    app.run(debug=True)
if __name__ ==