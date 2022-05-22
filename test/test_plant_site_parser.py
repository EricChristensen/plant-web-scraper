import sys
import lxml.html
sys.path.append("../src")

import unittest
import plant_site_parser

class TestPlantSiteParser(unittest.TestCase):

    def test_extract_plant_from_file_happy_path_one_plant(self):
        file = open("previous_plants.txt", "w")
        file.write("Thaumatophyllum evansii x|$125.00|-1|In stock")
        file.close()
        plants = plant_site_parser.extract_plants_from_file()
        self.assertEqual(len(plants), 1)
        self.assertEqual(plants[0].name, "Thaumatophyllum evansii x")

    def test_extract_plant_from_file_happy_path_two_plant(self):
        file = open("previous_plants.txt", "w")
        file.write("Thaumatophyllum evansii x|$125.00|-1|In stock\n")
        file.write("Thaumatophyllum evansii x 2|$126.00|-1|In stock")
        file.close()
        plants = plant_site_parser.extract_plants_from_file()
        self.assertEqual(len(plants), 2)
        self.assertEqual(plants[0].name, "Thaumatophyllum evansii x")
        self.assertEqual(plants[1].name, "Thaumatophyllum evansii x 2")

    # test exceptions are done properly

    def test_lxml_exploratory(self):
        html_string = '<html><body><div><p>text</p></div><div></div></body></html>'
        tree = lxml.html.fromstring(html_string)
        self.assertEqual(len(tree), 1)
        divs = tree.xpath('//div')
        self.assertEqual(len(divs), 2)
        p_tag = tree.xpath('//p')
        self.assertEqual(len(p_tag), 1)
        self.assertEqual(p_tag[0].text_content(), 'text')

if __name__ == '__main__':
    unittest.main()