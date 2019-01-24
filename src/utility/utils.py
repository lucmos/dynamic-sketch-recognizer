import re
import pandas

from src.constants import *


import os
import pickle
import json


def load_pickle(filename, folder="."):
    """
    Loads a given pickle file
    :param filename: the pickle file name
    :param folder: the default folder
    :return: the loaded data
    """
    filename = os.path.join(folder, filename)
    if os.path.isfile(filename):
        with open(filename, 'rb') as handle:
            return pickle.load(handle)
    return False


def save_pickle(obj, filename, folder=".", override=False):
    """
    Save a object to a pickle file with the highest protocol available
    :param obj: object to save
    :param folder: the default folder
    :param filename: pickle file name
    :param override: True if must replace existing file
    """
    filename = os.path.join(folder, filename)
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    if os.path.isfile(filename) and not override:
        filename = filename + "_be_safe" # to not lose info for distraction

    with open(filename, 'wb') as handle:
        pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_json(filename):
    """
        Loads a given json file
        :param filename: the json file name
        :return: the loaded data
    """
    if os.path.isfile(filename):
        with open(filename, 'r') as handle:
            return json.load(handle)
    return False


def save_json(obj, filename, override=False):
    """
    Save a object to a json file
    :param obj: object to save
    :param filename: json file name
    :param override: True if must replace existing file
    """
    if os.path.isfile(filename) and not override:
        filename = filename + "_be_safe" # to not lose info for distraction
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as handle:
        json.dump(obj, handle, indent=4, sort_keys=True)


def save_string(string, filename, override=False):
    """
      Save a string to a plain file
      :param string: string to save
      :param filename: file name
      :param override: True if must replace existing file
      """
    if os.path.isfile(filename) and not override:
        filename = filename + "_be_safe" # to not lose info for distraction

    with open(filename, "w") as handle:
        handle.write(string)


def min_max_normalization(array):
    """
    Performs a min-max normalization on the array
    :param array: the array to normalize
    :return: the normalized array
    """
    minx = min(array)
    maxx = max(array)
    return [(x - minx) / (maxx - minx) for x in array]


# todo elimina o sistema
def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split('(\d+)', text)]


def merge_dicts(dict1: dict, dict2: dict):
    assert set(dict1.keys()) == set(dict2.keys())
    for key in dict1.keys():
        assert isinstance(dict1[key], list)
        assert isinstance(dict2[key], list)
        dict1[key] += dict2[key]
    return dict1


def flat_nested_dict(dict_to_flat: dict):
    d = {}
    for k, v in dict_to_flat.items():
        if not isinstance(v, dict):
            d[k] = v
        else:
            d.update(flat_nested_dict(v))
    return d


def make_lists_values(d: dict):
    for k, v in d.items():
        if not isinstance(v, list):
            d[k] = [v]
    return d


def add_column(dataframe, column):
    if ITEM_ID in dataframe.columns:
        return dataframe.join(column, on=ITEM_ID)
    else:
        return dataframe.join(column)


def dataframe_to_csv(dataframe, dataset_name, path):
    mkdir(BUILD_CSV_FOLDER(dataset_name))
    dataframe.to_csv(path, decimal=",", sep=";")


def save_dataframes(dataset_name, dataframes_dict, dataframe_type, message, to_csv, frames_to_add_column, csv_column):
    mkdir(BUILD_GENERATED_FOLDER(dataset_name))
    chrono = chronometer.Chrono(message)
    for label, v in dataframes_dict.items():
        v.to_pickle(PATHS_FUN[dataframe_type][PICKLE_EXTENSION](dataset_name, label))
        if to_csv:
            if frames_to_add_column and csv_column is not None and label in frames_to_add_column:
                v = add_column(v, csv_column)
            dataframe_to_csv(v, dataset_name, PATHS_FUN[dataframe_type][CSV_EXTENSION](dataset_name, label))
    chrono.millis()


def init_dict(labels, length):
    return {x: [None] * length for x in labels}

def mkdir(path):
    if not os.path.isdir(path):
        os.makedirs(path)

# def get_infos(wordid_userid, user_data, wordid):
#     # join con l'user id_data
#     a = pandas.DataFrame(wordid_userid).join(user_data, on=USER_ID)
#
#     # consideriamo l'user che ci interessa
#     a = a[a[USER_ID] == wordid_userid[wordid]]
#
#     # contiamo quante parole ha già fatto
#     word_number = len(a.loc[: wordid]) - 1
#
#     # prendiamo il resto dei dati
#     row = a.loc[wordid].to_dict()
#     row[ITEM_INDEX] = word_number
#     return row

# def get_wordidfrom_wordnumber_name_surname(wordid_userid, user_data, name, surname, handwriting, word_number):
#     # join con l'user id_data
#     a = pandas.DataFrame(wordid_userid).join(user_data[[NAME, SURNAME, HANDWRITING]], on=USER_ID)
#
#     # consideriamo l'user e lo stile che ci interessa e prendiamo l'index corrispondente a word_number
#     b = (a.loc[(a[NAME] ==  name.lower()) & (a[SURNAME] == surname.lower()) & (a[HANDWRITING] == handwriting)])
#     assert not b.empty, "Controlla i parametri di ricerca, non è stata trovata nessuna entry"
#     return b.index[word_number]


def prettify_name(s):
    return " ".join(s.split("_")).title()


def uglify(t):
    return "".join(t.lower().split())

