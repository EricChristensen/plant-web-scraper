# plant-web-scraper
A nifty project for Veya that informed me about the lxml python library

To run, first clone the repo:

`git clone https://github.com/EricChristensen/plant-web-scraper.git`

## Quick run

After cloning, from the root run the python script:

`python src/plant_site_parser.py`

The first time you run the program, the program will think that all of the plants are newly available since there is no
previous plant state. On subsequent runs the program will read the previous plant state from a local file and will tell
you if there are new plants or newly in stock plants based on that state file.

## Running with Docker
Containerizing an application with docker has the advantage of ensuring that dependencies and runtimes are the same for
every machine that decides to run the program.

To run with docker, perform the following steps:

First, make sure you have [docker desktop](https://www.docker.com/) installed

Build the docker image with the following command:
`docker build -t plant_site_parser:latest .`

Run the python script in a docker container with the following command:
`docker run plant_site_parser:latest`

## Docker limitations running locally
Unfortunately, since the current implementation of saving the previous_plant state is file based, running with docker
from a personal computer has the limitation of not letting the user know if there are new plants or if the plant was
previously out of stock. This is because each run is encapsulated in its own container and the container ceases when the
program completes. There are solutions to this problem by passing in a file as a parameter to the container run command as well
as ways to access the file system in docker, and perhaps more obvious and elegant solutions for the docker experts out there,
but the logical next step that I would take would be deploying this as a Lambda that runs once a day, saving the state into
external storage rather than a local file and then using a notification service or library like Amazon's SNS to notify whoever
wants to be notified about new plants or recently in stock plants. Saving state to a local file is mostly to demonstrate a solution
with the least amount of dependencies possible, but there are other ways to do it that would be better for building things out more.

