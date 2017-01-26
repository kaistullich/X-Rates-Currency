from bs4 import BeautifulSoup
from urllib.request import urlopen

url = 'http://www.x-rates.com/table/?from=USD&amount=1'
page = urlopen(url)
soup = BeautifulSoup(page, 'html.parser')

currency_table = soup.find(class_='ratesTable')
currency_table_row_name = currency_table.find_all('td')

euro_currency = []
for tag in currency_table_row_name:
    euro_text = tag.get_text()  # pull only the text from the 'td' tags
    euro_append = euro_currency.append(euro_text)  # append the text from 'td' tags
    if 'British Pound' in tag:  # stop when 'British Pounds' is found
        break

del euro_currency[-1]  # Delete 'British Pounds' from the list always last element

print(euro_currency)