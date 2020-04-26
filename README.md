# ScrapingAndFetching
ScrapingAndFetching is created with a certain types of websites in mind, type of websites that provides user with different variations of download option to select from. It scrapes that information and provides to user with an option to select from. This script makes the file fetching easier for those websites.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites
You must have the following installed on your machine to run the project:

```
python3
git
```

You can look into the [requirements.txt](https://github.com/jsinghrai/ScrapingAndFetching/blob/master/requirements.txt) file to install the packages listed inside to where you store your global Python libraries.

I will show you how to create isolated Python environment for this project, so you can easily remove it when you are done using this program.

### Installation
```
git clone https://github.com/jsinghrai/ScrapingAndFetching.git
python -m venv ScrapFetch
cd ScrapingAndFetching
source /path/to/ScrapFetch/bin/activate
pip install -r requirements.txt
```

The last line in installation step installs the packages listed in requirements.txt into the ScrapFetch directory. So when you are done with using the script, you can deactivate the python virtual environment with `deactivate` command and remove the ScrapFetch directory to remove packages installed for this project.

### Uninstallation
These instructions will help you remove the project and packages installed with it:

```
deactivate
rm -r /path/to/ScrapFetch
sudo rm -r /path/to/ScrapingAndFetching
```

You should deactivate the python virtual environment if you have activated it, otherwise skip the first step. If you are using linux, then replace `/path/to/` with path to the directory from your current location in terminal.

If you are using any Desktop Environment then you can just delete the folder named `ScrapFetch` and `ScrapingAndFetching`.

### Running
If you are running the file as main module then you have to edit few things before running the `scrapfetch.py` script. First, you must edit the `link_file` variable in `main()` function and assign the file with links in it.

`Ex: link_file = '/home/$USER/Desktop/file_name.txt'`.

You also have to edit the functions: `verify_file_exist(file_name)` and `write_to_file(list_choices)` and make sure to change `.extension` to the type of extension you want it to be.

Also This script is made to fetch audio, video, images and other files for which you need to write as binary. If you are fetching text you must edit the open mode in `write_to_file(list_choices)` from `'wb' to 'w'`.

After you have made the changes mentioned above, you can run the script with:
`python scrapfetch.py`.

On successful download, the script adds the processed link to a list which it will process when user choose to end the script. It will create a new `file_name.txt` with processed links removed and create a new file `file_name.txt.bak` which is a backup file and contain the original content of `file_name.txt`.  

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License - see the [LICENSE.txt](https://github.com/jsinghrai/ScrapingAndFetching/blob/master/LICENSE.txt) file for details
