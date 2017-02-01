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

    ''' euro_currency[0] = Euro
        euro_currency[1] = 1.00 USD -> 1.00 EUR
        euro_currency[2] = 1.00 EUR -> 1.00 USD 
    '''
    euro_currency = []
    for tag in currency_table_row[1:3]:
        euro_text = tag.get_text()  # pull only the text from the 'td' tags
        euro_append = euro_currency.append(euro_text)  # append the text

    try:
        conn = sqlite3.connect('current_currency.sqlite')
        c = conn.cursor()  # cursor
        # c.execute('''CREATE TABLE currency 
        #             (usd_to_eur real, eur_to_usd real)''')
        c.execute('INSERT INTO currency VALUES (?, ?)', (euro_currency[0], euro_currency[1]))
        conn.commit()
        conn.close()

    except Exception as e:
        print(e)
            
    return render_template('currency.html', euro_currency=euro_currency)
    
if __name__ == '__main__':
    app.run(debug=True)
