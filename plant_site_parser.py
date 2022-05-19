import lxml.html
import requests
from os.path import exists

class PlantForSale:
    def __init__(self, name, original_price, sale_price, stock_status):
        self.name = name
        self.original_price = original_price
        self.sale_price = sale_price
        self.stock_status = stock_status

def extract_plants_from_html(tree_elem):
    plants = []
    for elem in tree_elem:
        plant = PlantForSale("uninitialized", 0, -1, "")

        # I would think this wouldn't be necessary...But it works and just getting the fields from elem.xpath() does not work as intended...
        li_html = lxml.html.tostring(elem)
        li_tree = lxml.html.fromstring(li_html)

        h2_content = li_tree.xpath('//h2')
        span_content = li_tree.xpath('//span')
        p_content = li_tree.xpath('//p')

        try:
            if (len(span_content) > 0 and len(h2_content) > 0):
                if (span_content[0].text_content() == "Sale!"):
                    plant.name = h2_content[0].text_content()
                    plant.original_price = span_content[1].text_content().split(' ')[0]
                    plant.sale_price = span_content[1].text_content().split(' ')[1]
                else:
                    plant.name = h2_content[0].text_content()
                    plant.original_price = span_content[0].text_content()
        except BaseException as err:
            print(f"Unexpected error when parsing plants from the html page {err=}")

        if (len(p_content) > 0):
            plant.stock_status = "Out of stock"
        else:
            plant.stock_status = "In stock"
        if (plant.name != "uninitialized"):
            plants.append(plant)
    return plants

def extract_plants_from_file():
    previous_plants = []
    filename = 'previous_plants.txt'
    previous_plants_file = open(filename, 'r') if exists(filename) else open(filename, 'a+')
    lines = previous_plants_file.readlines()

    for line in lines:
        try:
            plant_items = line.split('|')
            previous_plant = PlantForSale(plant_items[0], plant_items[1], plant_items[2], plant_items[3].strip())
            previous_plants.append(previous_plant)
        except BaseException as err:
            print(f"Unexpected error when parsing plants from the file {err=}")


    previous_plants_file.close()
    return previous_plants

def output_to_console(plants_dict, previous_plants_dict):
    for plant in plants_dict:
        print(plants_dict[plant].name, plants_dict[plant].original_price, plants_dict[plant].stock_status)
        if (plants_dict[plant].sale_price != -1):
            print("This plant is on sale for", plants_dict[plant].sale_price, "Buy it now!!!")
        if plant not in previous_plants_dict.keys():
            print("This is a newly available plant! Buy it now!!!")
        else:
            if previous_plants_dict[plant].stock_status == "Out of stock" and plants_dict[plant].stock_status == "In stock":
                print(plant + " was out of stock but is now in stock! Buy it now!!!")
        print("-----")

def write_to_file(plants):
    f = open("previous_plants.txt", "w")
    for plant in plants:
        f.write("{}|{}|{}|{}\n".format(plant.name, plant.original_price, plant.sale_price, str(plant.stock_status)))
    f.close()

if __name__ == "__main__":
    headers = {'User-Agent': 'My User Agent 1.0'}
    response = requests.get("https://www.nsetropicals.com/product-category/restocks/", headers=headers)
    tree = lxml.html.fromstring(response.text)
    tree_elem = tree.xpath('//li')

    plants = extract_plants_from_html(tree_elem)
    previous_plants = extract_plants_from_file()

    plants_dict = {}
    for plant in plants:
        plants_dict[plant.name] = plant

    previous_plants_dict = {}
    for plant in previous_plants:
        previous_plants_dict[plant.name] = plant

    output_to_console(plants_dict, previous_plants_dict)
    write_to_file(plants)
