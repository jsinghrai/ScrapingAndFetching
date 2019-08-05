#from urllib import request
import requests
from bs4 import BeautifulSoup
from file_read_backwards import FileReadBackwards

def content_fetch(url):
    return requests.get(url)

def request_successful(req):
    return req.status_code == requests.codes.ok

def fetch_links(file):
    soup = BeautifulSoup(file.text, 'lxml')
    return [link for link in soup.find_all('a', class_='touch')]

def give_choices(list_choices):
    for index, link in enumerate(list_choices, start=1):
        diff_type = ' '.join(link.text.split())
        print('{}) {}'.format(index, diff_type))
    print()

def write_to_file(list_choices):
    give_choices(list_choices)

    user_choice = int(input('Please pick your choice: '))
    user_choice = user_choice-1

    link = list_choices[user_choice].get('href', None)

    filename = link.split('/')
    filename = filename[-1]
    print("It's going to be saved as {}".format(filename))

    filename = input('Insert new name default({}): '.format(filename)) or filename

    if not filename.endswith('.extension'):
        filename = filename + '.extension'

    with open(filename, 'wb') as file:
        fetch = content_fetch(link)
        if request_successful(fetch):
            file.write(fetch.content)
        else:
            print("Issues with file fetching")
            print("Code Received: {}".format(req))

def main():
    li_to_del = []
    with FileReadBackwards('/path/to/file', mode='r', encoding = 'utf-8') as file:
        for line in file:
            user_input = input("Work on the next line: ")
            if user_input == 'y':
                req = content_fetch(line.strip())
                if request_successful(req):
                    links = fetch_links(req)
                    write_to_file(links)
                    li_to_del.append(line) #if successful download to delete later.
                else:
                    print("Request Failed!")
                    print('Code Received: {}'.format(req))
            else:
                print("Feel free to start again.")
                break

if __name__ == "__main__":
    main()
