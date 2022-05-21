FROM python:3.8

COPY src/plant_site_parser.py .
COPY requirements.txt .

RUN pip3 install -r requirements.txt

CMD ["python", "./plant_site_parser.py"]