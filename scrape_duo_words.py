#!/usr/bin/env python
# coding: utf-8
# Author: rykerish

import duolingo
import os
import pandas as pd
import sys
import re
import requests

from contextlib import suppress
from getpass import getpass, getuser
from hashlib import md5
from json import dumps
from tqdm import tqdm


def drop_from_list(l, sub):
    d = {elem['id']: elem for elem in l}
    for k in sub:
        with suppress(ValueError): l.remove(d[k])
    return l

def pretty_print(dict_items):
    for k, v in dict_items:
        print(f"  {k}: {v}", flush=True)

def customize_fields(word, lingo):
    fields = ['word', 'gender', 'infinitive', 'pos', 'translations', 'canonical_path', 'tts', 'lexeme_image']
    custom = None

    while custom not in ['yes', 'no', 'y', 'n', '']:
        custom = input("Customize flashcards? [Default: NO] (y/N/?) ").lower()
        if custom == '?':
            print(f"\nIf you change the default fields, the Anki template will not be valid anymore!\n\n" +
                  f"Default fields: {fields}\n", flush=True)
    if not custom or custom[0] == 'n':
        return fields

    example = word.copy()
    example.update(lingo.get_word_definition_by_id(word['id']))
    available_fields = list(example.keys())
    print(f"Available fields:", flush=True)
    pretty_print(enumerate(available_fields))
    while True:
        print("To see example, type 'example';\n" +
              "To see an example for a specific field, enter the field's number + '?' (e.g.: 3?);\n" +
              "To select the fields you want, enter the field numbers separated by a space (e.g.: 1 3 9);\n" +
              "To cancel customization, type 'cancel' or 'x'", flush=True)
        select = input("Enter your selection : ").lower()
        if select in ['cancel', 'x']:
            return fields
        elif select == "example":
            print(dumps(example, indent=4), flush=True)
        elif re.search(r'^[0-9]+(?=\?$)', select):
            i = int(select[:-1])
            if i >= len(available_fields):
                print("Invalid input (index out of range)", flush=True)
            else:
                fld = available_fields[i]
                print(f"{fld}: {example[fld]}", flush=True)
        elif re.search(r'^[0-9]+(\s[0-9]+)*\s*$', select):
            try:
                fields = [available_fields[int(i)] for i in select.split()]
                print(f'Selected fields: {fields}', flush=True)
                if input("Confirm selection? (y/n): ").lower() in ['yes', 'y']:
                    return fields
            except:
                print("Invalid input (index out of range)", flush=True)
        print('\n==============================\n', flush=True)

def get_anki_path(lang):
    os_ = re.sub(r'[0-9]', '', sys.platform)
    default_anki_path = {
        'darwin': os.path.join(os.getenv('HOME'), 'Library/Application Support'),
        'win': os.getenv('APPDATA'),
        'cygwin': os.getenv('APPDATA'),
        'linux': os.getenv('XDG_DATA_HOME') or os.path.join(os.getenv('HOME'),'.local/share')
    }
    anki_path = os.path.join(default_anki_path[os_], "Anki2")
    anki_users = []
    while not os.path.exists(anki_path):
        print(f"{anki_path} is not a valid path.", flush=True)
        anki_path = input("Please enter the location where Anki stores its data:  ")
        print('', flush=True)
    for dir_ in os.listdir(anki_path):
        path_ = os.path.join(anki_path, dir_)
        if os.path.isdir(path_) and 'collection.media' in os.listdir(path_):
            anki_users.append(dir_)

    if not len(anki_users):
        raise FileNotFoundError("No user found in Anki directory.")
    elif len(anki_users) == 1:
        i = 0
    else:
        i = -1
        while i not in range(0, len(anki_users), 1):
            pretty_print(enumerate(anki_users))
            with suppress(ValueError): i = int(input("Select user folder (enter number): "))
    anki_path = os.path.join(anki_path, anki_users[i], 'collection.media', lang)
    with suppress(FileExistsError): os.mkdir(os.path.join(anki_path))
    return anki_path

def media_dl(lang, fields):
    dl = None
    if set(['tts', 'lexeme_image']).intersection(fields):
        while dl not in ['yes', 'no', 'y', 'n', '']:
            dl = input("Do you want to download media files to your computer? [Default: NO] (y/N/?) ").lower()
            if dl == '?':
                print(f"\nDownloading media will take longer and can require manually telling the script where to " +
                      "find the correct destination folder in order for Anki to find them. However, this will " +
                      "allow you to have access to the information even when you are not connected to the " +
                      "internet\n", flush=True)
        if dl and dl[0] == 'y':
            return get_anki_path(lang)
    return None

def get_media(def_, fld, dl=False):
    if not dl or not def_[fld]:
        return def_[fld]
    ext = '.mp3' if fld == 'tts' else '.svg'
    response = requests.get(def_[fld])
    filename = md5(def_['word'].encode('utf-8')).hexdigest()+ext
    file = open(os.path.join(dl, filename), "wb")
    file.write(response.content)
    file.close()
    return os.path.join(os.path.basename(dl), filename)

def ids_to_df(vocab, lingo, fields, lang):
    dl = media_dl(lang, fields)

    with suppress(ValueError): fields.remove('id')
    tts = 'tts' in fields
    with suppress(ValueError): fields.remove('tts')
    lximg = 'lexeme_image' in fields
    with suppress(ValueError): fields.remove('lexeme_image')

    for word in tqdm(vocab):
        id_ = word['id']
        d = {'index': id_}

        def_ = {}
        if set(fields) != set(word.keys()).intersection(set(fields)):
            def_ = lingo.get_word_definition_by_id(id_)
        for fld in fields:
            d[fld] = def_[fld] if fld in def_.keys() else word[fld]
            if not d[fld]:
                d[fld] = "None"
        if tts:
            audio = get_media(def_, 'tts', dl)
            d['audio'] = f"<audio controls><source src='{audio}' type='audio/mpeg'></audio>" if audio else "No audio"
        if lximg:
            img = get_media(def_, 'lexeme_image', dl)
            d['img'] = f"<img src='{img}'/>" if img else "No image"
        try:
            res_df = res_df.append(d, ignore_index=True)
        except:
            res_df = pd.DataFrame(d, index=[0])
    res_df = res_df.set_index('index')
    res_df.index.name = None
    return res_df

def main(lingo):
    lang_dict = {lang: lingo.get_abbreviation_of(lang) for lang in lingo.get_languages()}
    print("Here are the languages you are learning:", flush=True)
    pretty_print(lang_dict.items())
    print("Which language do you want to scrap ?", flush=True)
    lang = ''
    while lang not in lang_dict.values():
        lang = input("(Please enter the corresponding 2-letter abbreviation): ").lower()
    filename = list(lang_dict.keys())[list(lang_dict.values()).index(lang)].lower()+'.tsv'
    sep = '\t'

    vocab = lingo.get_vocabulary(lang)['vocab_overview']
    fields = customize_fields(vocab[0], lingo)
    try:
        df = pd.read_csv(filename, sep=sep, index_col=0)
        ids = drop_from_list(vocab, df.index.to_list())
        if not len(vocab):
            return
        df = pd.concat([df, ids_to_df(vocab, lingo, fields, lang)])
    except:
        df = ids_to_df(vocab, lingo, fields, lang)
    df = df.drop_duplicates()
    df.to_csv(filename, sep=sep)
    return df

if __name__ == "__main__":
    lingo = None
    while not lingo:
        try:
            username = input("Enter your username: ")
            password = getpass("Enter your password: ")
            lingo  = duolingo.Duolingo(username, password)
        except duolingo.DuolingoException as e:
            print(e)
    main(lingo)

