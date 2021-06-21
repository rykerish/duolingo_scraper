# Duolingo scraper for Anki flashcards

First of all, a quick disclaimer: this script doesn't actually create Anki flashcards. It create a `.tsv` file which you can then import into Anki. 

You are free to modify and share the script as you wish (though I would prefer to be credited). However, note that if you do, the Anki template (`Template.apkg`) will probably not be valid anymore.

Last updated: 21/06/2021

## Initialising

Made using Python 3.8.5

### On Linux / OS X

Run `pip install -r requirements.txt`

### On Windows 10

Run `py -m pip install -r requirements.txt`

### On Windows < 10

Run `python3 -m pip install -r requirements.txt`

Import `Template.apkg` into Anki to have the card template. The code will not work if you try to download media without having Anki installed.

## Running

### On Linux / OS X

Run `python scrape_duo.py` and follow the instructions (I have tried to make them as clear as possible).

### On Windows 10

Run `py scrape_duo.py` and follow the instructions (I have tried to make them as clear as possible).

### On Windows < 10

Run `py scrape_duo.py` and follow the instructions (I have tried to make them as clear as possible).
