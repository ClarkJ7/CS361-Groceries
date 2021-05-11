import re

UNITS = ("whole", "teaspoon", "teaspoons", "tsp", "tablespoon", "tablespoons", "tbsp", "tin", "drops", "cloves", "ml", "oz", "grams", "ounces", "kilograms", "lb", "pound", "pounds", "can", "pint", "gallon", "quart")

SIZES = ("small ", "medium ", "large ")


def sort_recipe(ingredients_list):
    sorted_list = []
    for item in ingredients_list:

        # cut list off before or after "or" in line
        if " or " in item:
            length = len(item)
            or_loc = re.search(r'\b(or)\b', item)
            if or_loc.start() > int(length/2):
                item = item[:or_loc.start()-1]
            else:
                item = item[or_loc.start()+3:]

        # remove salt from ingredient list
        #if " salt" in item:
            #continue

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

        # check if line contains qty value add
        try:
            if float(item[0]):
                quantity = item.pop(0)
        except ValueError:
            quantity = "1"

        # if line contains unit value add
        if item[0].lower() in UNITS:
            unit = item.pop(0).lower()
        else:
            unit = "whole"

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
                print("Match!")
                quantity = int(i["qty"]) + int(j["qty"])
                j["qty"] = str(quantity)
                item_updated = True

        if item_updated is False:
            item = {"description": i["description"], "qty": i["qty"], "unit": i["unit"]}
            groceries.append(item)

    return groceries
