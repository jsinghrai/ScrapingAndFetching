#from urllib import request
import requests
from bs4 import BeautifulSoup

url = ''
#test = request.Request(url, headers={'User-Agent': "Firefox"})
test = requests.get(url)
print(test.status_code)
soup = BeautifulSoup(test.text, 'lxml')

#for link in soup.find_all('a', class_='touch'):
#    print(link.get('href', None))
link = soup.find_all('a', class_='touch')[2].get('href', None)
print(link)

with open(filename, 'wb') as file:
    fetch = requests.get(link)
    file.write(fetch.content)
