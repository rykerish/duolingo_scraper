# [Duolingo](https://www.duolingo.com/) scraper for Anki flashcards

First of all, a quick disclaimer: this script doesn't actually create Anki flashcards. It creates a `<language>.tsv` file which you can then import into Anki.

Basically, it takes the [list of words you've learned](https://www.duolingo.com/words) and retrieves their [definition](https://www.duolingo.com/dictionary) which it writes into a spreadsheet.

You are free to modify and share the script as you wish (see [license](https://github.com/rykerish/duolingo_scraper/blob/main/LICENSE)). However, note that if you change it, the Anki template (`Template.apkg`) will probably not be valid anymore.

Last updated: 21/06/2021

## Initialising

Made using Python 3.8.5

Import `Template.apkg` into Anki to have the card template. The code will not work if you try to download media without having Anki installed.

### On Linux / OS X

Run `pip install -r requirements.txt`

### On Windows 10

Run `py -m pip install --user -r requirements.txt`

### On Windows < 10

Run `python3 -m pip install --user -r requirements.txt`

## Running

Run the script and follow the instructions (I have tried to make them as clear as possible).

### On Linux / OS X

`python scrape_duo_words.py`

### On Windows 10

`py scrape_duo_words.py`

### On Windows < 10

`python3 scrape_duo_words.py`

## Importing into Anki

Open Anki, click "Import File" and choose the resulting `<language>.tsv` file. 

Set the card Type to `duolingo` (from the Template), and select your target deck; fields should be separated by Tab.

***Make sure the "Allow HTML in fields" option is checked or you won't have audio and images.***

Unless you modified the script or did not use the default fields when running the script, the field mapping should be done automatically.

Now you can just import and practice!
