import re
from fractions import Fraction
import unicodedata


MISC_UNITS = ("tin", "container", "can", "clove", "slice", "loaf", "drop", "packet", "package", "shot", "drizzle",
              "head")

FRACTIONS = ("whole", "half", "quarter", "third")

SIZES = ("small ", "medium ", "large ")

UNIT_DICT = {"ounce": 1, "oz": 1,
             "teaspoon": 0.167, "tsp": 0.167,
             "tablespoon": 0.5, "tbsp": 0.5,
             "cup": 8, "c": 8,
             "pint": 16, "pt": 16,
             "quart": 32, "qt": 32,
             "gallon": 128, "gal": 128,
             "milliliter": 0.034, "ml": 0.034,
             "deciliter": 0.34, "dl": 0.34,
             "liter": 34, "l": 34,
             "kilogram": 35, "kg": 35,
             "gram": 0.035, "g": 0.035,
             "pound": 16, "lb": 16}


def sort_recipe(ingredients_list):
    sorted_list = []
    for item in ingredients_list:

        item = format_line(item)

        parse_object = find_qty(item)
        quantity = print_qty(parse_object[0])
        item = parse_object[1]

        parse_object = find_unit(item)
        unit = parse_object[0]
        item = parse_object[1]

        # use rest of line to create item description
        desc = " ".join(item)
        desc = desc.strip()
        desc = format_desc(desc)
        output = {"description": desc, "qty": quantity, "unit": unit}
        sorted_list.append(output)

    return sorted_list


def format_line(item_string):
    # remove anything inside parenthesis
    item = re.sub("\(.*?\)", "", item_string)
    item = item.strip()
    item_list = item.split(" ")

    return item_list


def format_desc(item):
    try:
        item = item[:item.index(",")]
    except ValueError:
        pass

    item = item.replace("of ", "")

    return item


def slice_before_after(item, string):
    length = len(item)
    if string in item:
        str_index = re.search(string, item)
        if str_index.start() > int(length / 2):
            item = item[:str_index.start() - 1]
        else:
            item = item[str_index.start() + 3:]
    return item


def find_qty(item):
    # split 1-lb into 1, -, lb
    if "-" in item[0]:
        placeholder = item[0].split("-")
        item[0] = placeholder[0]
        item.insert(1, placeholder[1])

    quantity = 0
    prev_value = False
    index = 0

    for i in range(len(item)):
        if is_numeric(item[i]):
            temp_qty = find_numeric_qty(item[i])
            if prev_value is True:
                quantity += temp_qty
                index = i+1
            else:
                quantity = temp_qty
                index = i+1
            prev_value = True
        elif len(item[i]) == 2:
            if is_numeric(item[i][0]):
                if prev_value is True:
                    quantity += find_numeric_qty(item[i][0])
                    quantity += find_numeric_qty(item[i][1])
                    index = i + 1
                else:
                    quantity = find_numeric_qty(item[i][0])
                    quantity += find_numeric_qty(item[i][1])
                    index = i + 1

                prev_value = True
            else:
                prev_value = False
        else:
            prev_value = False
    print(index)
    item = item[index:]
    output = [quantity, item]
    return output


def find_numeric_qty(item):
    try:
        if unicodedata.numeric(item):
            quantity = float(unicodedata.numeric(item))
    except (TypeError, ValueError):
        try:
            if Fraction(item):
                quantity = float(Fraction(item))
        except ValueError:
            quantity = 0
    return quantity


def is_numeric(item):
    try:
        if unicodedata.numeric(item):
            return True
    except (TypeError, ValueError):
        try:
            if float(Fraction(item)):
                return True
        except ValueError:
            return False


def print_qty(qty_float):
    whole_number = int(qty_float)
    if whole_number == 0:
        whole_number = None
    else:
        whole_number = str(whole_number)

    decimals = qty_float % 1
    if decimals > 0.8:
        decimals = "5/6"
    elif decimals > .70:
        decimals = "3/4"
    elif decimals > .60:
        decimals = "2/3"
    elif decimals > .44:
        decimals = "1/2"
    elif decimals > .30:
        decimals = "1/3"
    elif decimals > .20:
        decimals = "1/4"
    elif decimals > .10:
        decimals = "1/6"
    else:
        decimals = None

    if whole_number and decimals:
        return whole_number + "-" + decimals
    elif whole_number and not decimals:
        return whole_number
    elif decimals and not whole_number:
        return decimals
    else:
        return 0


def find_unit(item):
    unit_fog = (".", "s")
    if item[0][-1] in unit_fog:
        item[0] = item[0][0:-1]

    if item[0].lower() == "t":
        if item[0] == "t":
            item[0] = "tsp"
        else:
            item[0] = "tbsp"

    if item[0].lower() in UNIT_DICT.keys():
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
                    j_qty = qty_to_float(j["qty"])
                    i_qty = qty_to_float(i["qty"])
                    test1 = j_qty*float(UNIT_DICT[j["unit"]])
                    test2 = i_qty*float(UNIT_DICT[i["unit"]])
                    output = (test1 + test2) / UNIT_DICT[j["unit"]]
                    j["qty"] = print_qty(output)
                    item_updated = True
                elif j["unit"] == i["unit"]:
                    j_qty = qty_to_float(j["qty"])
                    i_qty = qty_to_float(i["qty"])
                    output = (j_qty + i_qty)
                    j["qty"] = print_qty(output)
                    item_updated = True

        if item_updated is False:
            item = {"description": i["description"], "qty": i["qty"], "unit": i["unit"]}
            groceries.append(item)

    return groceries


def qty_to_float(qty_string):
    qty_float = 0
    # break up whole number and fraction
    if "-" in qty_string:
        placeholder = qty_string.split("-")
        qty_float += Fraction(placeholder[0])
        qty_float += Fraction(placeholder[1])
    else:
        qty_float += Fraction(qty_string)

    return float(qty_float)
