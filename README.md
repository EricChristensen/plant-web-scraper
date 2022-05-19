# plant-web-scraper
A nifty project for Veya that informed me about the lxml python library

To run, first clone the repo:

`got clone https://github.com/EricChristensen/plant-web-scraper.git`

Then run the python script:

`python plant_site_parser.py`

Make sure the python version you are running is python 3. Note that the first time this is run, the program thinks that all of the plants are new plants. The plant information gets saved to a local file, previous_plants.txt and the program will only think there are new plants if there really are new plants in the web page that don't match with the previous_plants file.
