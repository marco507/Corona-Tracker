import requests
from bs4 import BeautifulSoup
from unicodedata import normalize
from datetime import datetime as dt
from lxml import etree
import numpy as np
import logging

from .models import Record

def get_data():

    # Init logging
    logging.basicConfig(filename='log.txt', level=logging.ERROR)

    # ------------------------ Gemany ------------------------

    try:
        page = requests.get('https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html')
        soup = BeautifulSoup(page.content, 'lxml')
        table = soup.find('table')

        # Retrieve the elements
        tbody = table.find('tbody')
        rows = tbody.find_all('tr')

        data_ger = []
        for row in rows:
            data_ger.append([element.getText() for element in row.find_all('td')])
            
        # Retrieve the last row
        data_ger = data_ger[-1]
        # Retrieve the total infections, 7-day-incidence, deaths
        data_ger = [data_ger[index] for index in [1,4,5]]
        # Remove points
        data_ger = [element.replace('.', '') for element in data_ger]
        # Replace commas with points
        data_ger = [element.replace(',', '.') for element in data_ger]

        if len(data_ger) != 3:
            raise Exception('Data length is not 3')
        else:
            # We add the data to the database
            Record.objects.create(country='Germany', total_infections=data_ger[0], incidence=data_ger[1], total_deaths=data_ger[2])

    except:
        # Log the error
        logging.error('Error while retrievieng data for Germany')

    # ------------------------ Austria ------------------------

    try:
        page = requests.get('https://coronavirus.datenfakten.at/')
        soup = BeautifulSoup(page.content, 'lxml')
        dom = etree.HTML(str(soup))

        # Retrieve the 7-day-incidence
        incidence = dom.xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div/h1')[0].text

        # Retrieve the table
        table = etree.tostring(dom.xpath('/html/body/div[1]/div/div/div[4]/div[1]/div[3]/div/div/div/table')[0])
        table = BeautifulSoup(table, 'lxml')

        rows = table.find_all('tr')

        data_aut = []
        for row in rows:
            data_aut.append([element.getText() for element in row.find_all('td')])

        # Retrieve the last row
        data_aut = data_aut[-1]
        # Retrieve the total infections and deaths
        data_aut = [data_aut[index] for index in [1,3]]
        # Add the incidence
        data_aut.insert(1, incidence.replace(' ', ''))
        # Remove points
        data_aut = [element.replace('.', '') for element in data_aut]
        # Replace commas with points
        data_aut = [element.replace(',', '.') for element in data_aut]

        if len(data_aut) != 3:
            raise Exception('Data length is not 3')
        else:
            # We add the data to the database
            Record.objects.create(country='Austria', total_infections=data_aut[0], incidence=data_aut[1], total_deaths=data_aut[2])

    except:
        # Log the error
        logging.error('Error while retrievieng data for Austria')

    # ------------------------ Schweiz ------------------------

    try:
        page = requests.get('https://www.corona-in-zahlen.de/weltweit/schweiz/')
        soup = BeautifulSoup(page.content, 'lxml')
        dom = etree.HTML(str(soup))

        # Retrieve the total infections, 7-day-incidence, deaths
        total = dom.xpath('/html/body/div[3]/div[2]/div[2]/div/div/p[1]/b')[0].text
        incidence = dom.xpath('/html/body/div[3]/div[3]/div[1]/div/div/p[1]/b')[0].text
        deaths = dom.xpath('/html/body/div[3]/div[3]/div[2]/div/div/p[1]/b')[0].text

        data_swi = []
        # Add the retrieved data
        data_swi.append(total)
        data_swi.append(incidence.replace('\n', '').replace(' ', ''))
        data_swi.append(deaths)
        # Remove points
        data_swi = [element.replace('.', '') for element in data_swi]
        # Replace commas with points
        data_swi = [element.replace(',', '.') for element in data_swi]

        if len(data_aut) != 3:
            raise Exception('Data length is not 3')
        else:
            # We add the data to the database
            Record.objects.create(country='Switzerland', total_infections=data_swi[0], incidence=data_swi[1], total_deaths=data_swi[2])

    except:
        # Log the error
        logging.error('Error while retrievieng data for Switzerland')

