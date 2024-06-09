#!/usr/bin/env python3

"""This module defines a function save_to_json_file(my_obj, filename)

save_to_json_file(my_obj, filename) writes an Object to a text file,
using a JSON representation

"""
import json
from datetime import datetime


def save_to_json_file(my_obj, filename):
    """ Writes an Object to a text file,
    using a JSON representation

    args:
        my_obj: an object to it's json representation to a text file.
        filename: a file to write a json representation of my_obj object.
    """
    with open(filename, "w") as file:
        json.dump(my_obj, file, indent=4)


def load_from_json_file(filename):
    """Creates an Object from a JSON file

    args:
        filename: JSON file to create an object from.
    Returns: the object created or Deserialized
    """
    with open(filename) as file:
        obj = json.load(file)
        return (obj)


def collect_and_calculate_models(filename):
    """collects and calculate models or products being sold.
    This calculates how many times a particular model has been
    record(sold) in the current month

    args:
       filename: The dataset file where it reads and calculates models.
    Returns: nothing.
    """
    models = []
    count = []
    model_list = []
    n = 0
    date = datetime.today().strftime("%B")
    data_list = load_from_json_file(filename)
    for data in data_list:
        try:
            r_date = datetime.strptime(data["Date"], "%d/%m/%Y %H:%M:%S")
            if date == r_date.strftime("%B"):
                if data["Model"] not in models:
                    n += 0
                    models.append(data["Model"])
                    count.append(n)
                if data["Model"] in models:
                    index = models.index(data["Model"])
                    count[index] += 1
        except ValueError:
            pass
        n = 0
    for x in range(len(models)):
        model_dict = {}
        model_dict["type"] = models[x]
        model_dict["total"] = count[x]
        model_list.append(model_dict)
    save_to_json_file(model_list, "hafeez_shop/data/models.json")


def search_and_populate(new_data_list, filename):
    """Search the existing data for cpllection any was made or adds a new
    object at the end of the data list.

    args:
       new_data_list: a list of dictonaries containing product information
       filename: A json file contain the base data (This is where we search for
       existing data and update or append new object)
   Returns: nothing.
    """
    data_list = load_from_json_file(filename)
    for new in new_data_list:
        is_found = False
        if data_list:
            for pos in range(len(data_list)):
                if new["Date"] == data_list[pos]["Date"]:
                    if new["IMEI"] == data_list[pos]["IMEI"]:
                        is_found = True
                        if (data_list[pos]["Contract_No"] != new["Contract_No"] and
                        (data_list[pos]["Contract_No"] == "Missing contract number" or 
                            data_list[pos]["Contract_No"] == "Contract number may be incomplete!")):
                            data_list[pos]["Contract_No"] = new["Contract_No"]
                    else:
                        if (new["Contract_No"] == data_list[pos]["Contract_No"] or
                            data_list[pos]["IMEI"] == "IMEI Length Error"):
                            is_found = True
                            if (new["IMEI"] != "IMEI Length Error" and
                                data_list[pos]["IMEI"] == "IMEI Length Error"):
                                data_list[pos]["IMEI"] = new["IMEI"]
                            if (data_list[pos]["Contract_No"] != new["Contract_No"] and
                            (data_list[pos]["Contract_No"] == "Missing contract number" or 
                                data_list[pos]["Contract_No"] == "Contract number may be incomplete!")):
                                data_list[pos]["Contract_No"] = new["Contract_No"]
        if not is_found:
            data_list.append(new)
    save_to_json_file(data_list, filename)
    collect_and_calculate_models(filename)
