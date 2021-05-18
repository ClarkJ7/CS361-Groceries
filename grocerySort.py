import re
from fractions import Fraction
import unicodedata
import string

UNITS = ("whole", "half", "quarter", "third", "teaspoon", "teaspoons", "tsp", "tablespoon", "tablespoons", "tbsp",
         "tin", "drops", "cloves", "millilitres", "ml", "oz", "ounce", "ounces", "grams", "ounces", "kilograms", "lb", "pound",
         "pounds", "can", "cans", "pint", "pints", "gallon", "quart", "cup", "t.", "T.", "cups")

SIZES = ("small ", "medium ", "large ")


def sort_recipe(ingredients_list):
    sorted_list = []
    for item in ingredients_list:
        # cut list off before or after "or" in line
        length = len(item)
        if " or " in item:
            or_loc = re.search(r'\b(or)\b', item)
            if or_loc.start() > int(length/2):
                item = item[:or_loc.start()-1]
            else:
                item = item[or_loc.start()+3:]
        # cut list off after "to" in line
        if " to " in item:
            to_loc = re.search(r'\b(to)\b', item)
            item = item[to_loc.start()+3:]

        # remove anything after a comma
        try:
            item = item[:item.index(",")]
        except ValueError:
            pass

        # remove salt from ingredient list
        if "salt" in item:
            print("salt removed")
            continue

        # remove salt from ingredient list
        if "water" in item:
            print("water removed")
            continue

        # remove of from line
        item = item.replace("of ", "")

        # remove words related to size
        for size in SIZES:
            item = item.replace(size, "")

        # remove anything inside paranthesis
        item = re.sub("\(.*?\)","", item)

        # remove whitespaces
        item = item.strip()

        # split string into list for parsing
        item = item.split(" ")

        # check if line contains qty value
        try:
            if float(Fraction(item[0])):
                quantity = item.pop(0)
        except ValueError:
            quantity = 0

        # check for vulgar fraction
        try:
            if unicodedata.numeric(item[0]):
                quantity = item.pop(0)
        except:
            pass

        # if line contains unit value add
        if item[0].lower() in UNITS:
            unit = item.pop(0).lower()
        elif item[0].lower == "to" or item[0].lower == "or":
            item.pop(0)

        else:
            unit = "unk"

        # use rest of line to create item description
        desc = " ".join(item)
        output = {"description": desc, "qty": quantity, "unit": unit}
        sorted_list.append(output)

    return sorted_list


def combine_groceries(ingredients, groceries):

    for i in ingredients:
        item_updated = False

        for j in groceries:

            if j["description"] == i["description"]:
                if j["qty"] == i["qty"]:
                    quantity = float(Fraction(i['qty'])) + float(Fraction(j['qty']))
                    j["qty"] = str(quantity)
                    item_updated = True

        if item_updated is False:
            item = {"description": i["description"], "qty": i["qty"], "unit": i["unit"]}
            groceries.append(item)

    return groceries