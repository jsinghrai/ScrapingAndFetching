#from urllib import request
import requests
from bs4 import BeautifulSoup
from file_read_backwards import FileReadBackwards
from validators import url as url_valid
import fileinput
import os


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
    '''
    Takes in list of 'bs4.element.Tag'.
    Iterates over list of 'bs4.element.Tag' and parses out list of
    choices to present to the user to pick from.
    Returns None
    '''
    for index, link in enumerate(list_choices, start=1):
        diff_type = ' '.join(link.text.split())
        print('{}) {}'.format(index, diff_type))
    print()
    return


def choose_from(msg, *choices):
    '''
    Takes two argument: user message to present for input and a
    tuple that packs list of choices.
    Runs as long as user choice doesn't match given choices.
    Returns the choice user made.
    '''
    print("Please choose from these choices: {}".format(choices))
    user_input = input(msg).lower()
    print()

    while user_input not in choices:
        print("Please choose from these choices: {}".format(choices))
        user_input = input(msg).lower()
        print()

    return user_input


def fetch_file_name(url):
    '''
    Takes url as the argument to parse out the file's name.
    Returns the file's name from the url or None if empty.
    '''
    # In case string is empty
    if not url:
        return
    file_name = url.split('/')
    file_name = file_name[-1]
    return file_name


def verify_file_exist(file_name):
    '''
    Takes file name as argument and checks if it exists in the given
    path if file already exists. Ask user to change name while distinct name
    is not chosen.
    '''
    while os.path.isfile(os.path.join(look_path, file_name)):
        file_name = input("File '{}' exist, either verify the file is different"
                          " or choose a different name: "".format(file_name)) or file_name

        if not file_name.endswith('.extension'):
            file_name = file_name + '.extension'

    return file_name


def write_to_file(list_choices):
    '''
    Takes in list of 'bs4.element.Tag'.
    Returns String for successful download and write to file, otherwise
    returns None.
    '''
    give_choices(list_choices)

    # Preparing the message and user choices to present to user.
    message = 'Please pick your choice: '
    user_choices = list(map(str, range(1, len(list_choices)+1)))
    user_choices.append('end')

    user_choice = choose_from(message, *user_choices)

    if user_choice == 'end':
        print("User chose not to proceed.")
        return

    user_choice = int(user_choice)-1

    # grabs the href attribute from the list with given user choice
    link = list_choices[user_choice].get('href', None)

    # Parses the file name out from the link.
    file_name = fetch_file_name(link)

    # remove this if you want to save it as default and not be asked to change it
    file_name = input('Insert new name default({}): '.format(file_name)) or file_name

    if not file_name.endswith('.extension'):
        file_name = file_name + '.extension'

    # this needs to be there to verify if the file name doesn't exist.
    file_name = verify_file_exist(file_name)

    print("It's going to be saved as '{}'\n".format(file_name))

    with open(os.path.join(look_path, file_name), 'wb') as file:
        fetch = content_fetch(link)
        if request_successful(fetch):
            file.write(fetch.content)
            return 'Successfully written to file.'
        else:
            print("Issues with file fetching")
            print("Code Received: '{}'".format(req))
    return


def remove_from_file(remove_this, file_name):
    '''
    Takes two inputs: list of links and file name.
    Removes everything in the list from the given file name.
    '''
    print("Removing These: ")

    for line in remove_this:
        print(line.strip())

    for link in fileinput.input(file_name, inplace=True, backup='.bak'):
        if link.strip() not in remove_this:
            print(link.strip())
    return


def main():
    # stores links which will be deleted from the file.
    li_to_del = []

    # message which will be displayed to user for input.
    message = "Do you want to continue: "

    # Gives the user choices to pick from.
    user_choices = ['yes', 'end', 'skip']

    # the file which stores the links.
    link_file = '/path/to/file'

    try:
        with FileReadBackwards(link_file, encoding='utf-8') as file:
            for line in file:
                file_name = fetch_file_name(line)
                print('*'*50)
                print('Requesting: {}'.format(file_name))

                user_input = choose_from(message, *user_choices)

                if user_input == 'yes':
                    if validate(line):
                        response = content_fetch(line)
                        if request_successful(response):
                            links = fetch_links(response)
                            if write_to_file(links):
                                print("Successfully written to file. Adding link to "
                                      "the list to delete.\n")
                                li_to_del.append(line)  # if successful download to delete later.
                            else:
                                print("Nothing was downloaded this time.\n")
                        else:
                            print("Request Failed!")
                            print('Code Received: {}\n'.format(response))
                    else:
                        print('{} is not a valid link.\n'.format(line))
                else:
                    if user_input == 'end':
                        print('Feel Free To Start Again.')
                        print('*'*50)
                        break
                    elif user_input == 'skip':
                        print("Skipping: {}\n".format(file_name))
    except FileNotFoundError:
        print("No such file: '{}'".format(link_file))

    if li_to_del:
        remove_from_file(li_to_del, link_file)


if __name__ == "__main__":
    # After fetching files will be stored in this directory.
    look_path = os.path.join(os.getcwd(), 'StoreHere')
    # main()
