import re
from fractions import Fraction
import unicodedata

LIQ_UNITS = ("ounce", "oz",
             "teaspoon", "tsp",
             "tablespoon", "tbsp",
             "cup",
             "pint", "pt",
             "quart", "qt",
             "gallon", "gal",
             "milliliter", "ml",
             "liter", "l")

MISC_LIQ_UNITS = ("drop")

WEIGHT_UNITS = ("gram", "g",
                "pound", "lb",
                "kilogram", "kg")

MISC_UNITS = ("tin", "container", "can", "clove", "slice", "loaf")

FRACTIONS = ("whole", "half", "quarter", "third")

SIZES = ("small ", "medium ", "large ")

UNIT_DICT = {"ounce": 1,"oz": 1,
             "teaspoon": 0.167, "tsp": 0.167,
             "tablespoon": 0.5, "tbsp": 0.5,
             "cup": 8,
             "pint": 16, "pt": 16,
             "quart": 32, "qt": 32,
             "gallon": 128, "gal": 128,
             "milliliter": 0.034, "ml": 0.034,
             "liter": 34, "l": 34}


def sort_recipe(ingredients_list):
    sorted_list = []
    for item in ingredients_list:

        item = format_line(item)
        if item == "skip":
            continue

        parse_object = find_qty(item)
        quantity = parse_object[0]
        item = parse_object[1]
        parse_object = find_qty(item)
        if parse_object[0] != 0:
            quantity = int(quantity)*2

        parse_object = find_unit(item)
        unit = parse_object[0]
        item = parse_object[1]

        # use rest of line to create item description
        desc = " ".join(item)
        desc = desc.strip()
        output = {"description": desc, "qty": quantity, "unit": unit}
        sorted_list.append(output)

    return sorted_list


def format_line(item):
    # cut list off before or after "or" in line, targets "3 or 4 cups" AND "blah blah or blah"
    # remove anything inside parenthesis
    item = re.sub("\(.*?\)", "", item)

    length = len(item)
    if " or " in item:
        or_loc = re.search(r'\b(or)\b', item)
        if or_loc.start() > int(length / 2):
            item = item[:or_loc.start() - 1]
        else:
            item = item[or_loc.start() + 3:]
    # cut list off after "to" in line, targets "4 to 5 cups"
    if " to " in item:
        to_loc = re.search(r'\b(to)\b', item)
        item = item[to_loc.start() + 3:]

    # remove anything after a comma, targets "1 whole onion, diced"
    try:
        item = item[:item.index(",")]
    except ValueError:
        pass

    # remove salt from ingredient list
    if "salt" in item or "black pepper" in item:
        return "skip"

    # remove water from ingredient list
    if "water" in item:
        return "skip"

    # remove of from line
    item = item.replace("of ", "")

    # remove words related to size
    for size in SIZES:
        item = item.replace(size, "")

    # remove whitespaces
    item = item.strip()

    # split string into list for parsing
    item = item.split(" ")

    return item


def find_qty(item):
    if "-" in item[0]:
        placeholder = item[0].split("-")
        item[0] = placeholder[0]
        item.insert(1, placeholder[1])

    try:
        if unicodedata.numeric(item[0]):
            quantity = item.pop(0)
    except (TypeError, ValueError):
        try:
            if float(Fraction(item[0])):
                quantity = item.pop(0)
        except ValueError:
            quantity = 0

    output = [quantity, item]
    return output


def find_unit(item):
    unit_fog = (".", "s")
    if item[0][-1] in unit_fog:
        item[0] = item[0][0:-1]

    if item[0].lower() == "t":
        if item[0] == "t":
            item[0] = "tsp"
        else:
            item[0] = "tbsp"

    if item[0].lower() in LIQ_UNITS:
        unit = item.pop(0).lower()
    elif item[0].lower() in MISC_LIQ_UNITS:
        unit = item.pop(0).lower()
    elif item[0].lower() in WEIGHT_UNITS:
        unit = item.pop(0).lower()
    elif item[0].lower() in MISC_UNITS:
        unit = item.pop(0).lower()
    else:
        unit = "unk"

    output = [unit, item]
    return output


def combine_groceries(ingredients, groceries):

    for i in ingredients:
        item_updated = False

        for j in groceries:

            if j["description"] == i["description"]:
                if j["unit"] in UNIT_DICT and i["unit"] in UNIT_DICT:
                    j_qty = convert_fraction(j["qty"])
                    i_qty = convert_fraction(i["qty"])
                    test1 = j_qty*float(UNIT_DICT[j["unit"]])
                    test2 = i_qty*float(UNIT_DICT[i["unit"]])
                    output = (test1 + test2) / UNIT_DICT[j["unit"]]
                    j["qty"] = str(output)
                    item_updated = True

        if item_updated is False:
            item = {"description": i["description"], "qty": i["qty"], "unit": i["unit"]}
            groceries.append(item)

    return groceries


def convert_fraction(item):
    try:
        output = float(unicodedata.numeric(item))
    except (TypeError, ValueError):
        try:
            output = float(Fraction(item))
        except ValueError:
            output = 1

    return output
