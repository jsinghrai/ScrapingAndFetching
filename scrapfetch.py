#from urllib import request
import requests
from bs4 import BeautifulSoup
from file_read_backwards import FileReadBackwards
from validators import url as url_valid

def validate(url):
    '''
    Returns True if the url is valid, otherwise returns
    :class: `~validators.utils.ValidationFailure'.
    '''
    return url_valid(url)

def content_fetch(url):
    '''
    Returns :class: `Response <Response>` object received for
    the request that was made.
    '''
    return requests.get(url)

def request_successful(res):
    '''
    Takes in Response object as argument.
    Return True if the request was successful, otherwise returns
    False.
    '''
    return res.status_code == requests.codes.ok

def fetch_links(res):
    '''
    Takes in Response object as argument.
    Uses lxml XML toolkit to parse the response object with
    BeautifulSoup.
    Returns list of 'bs4.element.Tag'
    '''
    soup = BeautifulSoup(res.text, 'lxml')
    return [link for link in soup.find_all('a', class_='touch')]

def give_choices(list_choices):
    for index, link in enumerate(list_choices, start=1):
        diff_type = ' '.join(link.text.split())
        print('{}) {}'.format(index, diff_type))
    print()
    return

def choose_from(msg, *choices):
    print("Please choose from these choices: {}".format(choices))
    user_input = input(msg)
    print()

    while user_input not in choices:
        print("Please choose from these choices: {}".format(choices))
        user_input = input(msg)
        print()

    return user_input

def write_to_file(list_choices):
    give_choices(list_choices)

    message = 'Please pick your choice: '
    user_choices = list(map(str,range(1,len(list_choices)+1)))

    user_choice = choose_from(message, *user_choices, 'end')

    if user_choice == 'end':
        print("User chose not to proceed.")
        return

    user_choice = int(user_choice)-1

    link = list_choices[user_choice].get('href', None)

    filename = link.split('/')
    filename = filename[-1]

    filename = input('Insert new name default({}): '.format(filename)) or filename
    print("It's going to be saved as '{}'".format(filename))

    if not filename.endswith('.extension'):
        filename = filename + '.extension'

    with open(filename, 'wb') as file:
        fetch = content_fetch(link)
        if request_successful(fetch):
            file.write(fetch.content)
            return 'Successfully written to file.'
        else:
            print("Issues with file fetching")
            print("Code Received: '{}'".format(req))
    return

def remove_from_file(remove_this):
    pass

def main():
    li_to_del = []
    message = "Work on the next line: "
    user_choices = ['yes', 'no', 'skip']

    with FileReadBackwards('/path/to/file', encoding = 'utf-8') as file:
        for line in file:
            user_input = choose_from(message, *user_choices)
            if user_input == 'yes':
                link = line.strip()
                if validate(link):
                    req = content_fetch(link)
                    if request_successful(req):
                        which_file = link.split('/')[-1]
                        which_file = which_file.split('.')[0]
                        print('Fetching: {}'.format(which_file))
                        links = fetch_links(req)
                        if write_to_file(links):
                            li_to_del.append(line) #if successful download to delete later.
                        else:
                            print("Nothing was downloaded this time.\n")
                    else:
                        print("Request Failed!")
                        print('Code Received: {}\n'.format(req))
                else:
                    print('{} is not a valid link.\n'.format(link))
            else:
                if user_input == 'no':
                    print('Feel Free To Start Again.')
                    break
                elif user_input == 'skip':
                    print("Skipping This\n")

        remove_from_file(li_to_del)


if __name__ == "__main__":
    main()
