from bs4 import BeautifulSoup
from flask import Flask, render_template
from urllib.request import urlopen

app = Flask(__name__)

@app.route('/')
def index():
    url = 'http://www.x-rates.com/table/?from=USD&amount=1'
    page = urlopen(url)
    soup = BeautifulSoup(page, 'lxml')

    currency_table = soup.find(class_='ratesTable')  # finds the table
    currency_table_row = currency_table.find_all('td')  # pulls all the 'td' tags from the 'ratesTable'

    euro_currency = []
    for tag in currency_table_row[:3]:
        euro_text = tag.get_text()  # pull only the text from the 'td' tags
        euro_append = euro_currency.append(euro_text)  # append the text
    
    return render_template('currency.html', euro_currency=euro_currency)
    
if __name__ == '__main__':
    app.run(debug=True)
