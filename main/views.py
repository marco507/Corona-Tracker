import mimetypes
from django.shortcuts import render
from django.http import HttpResponse

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.formatters import DatetimeTickFormatter, BasicTickFormatter
import pandas as pd
import os

from scraper.settings import BASE_DIR

from .models import Record


def index(request):

    # We init the plot dictionary
    plot = dict()

    for country in ['Germany', 'Austria', 'Switzerland']:

        # We init the country dictionary inside the plot dictionary
        plot[country] = {}

        # We retrieve all records for the country sorted by ascending date
        records = Record.objects.filter(country=country).order_by('date')

        # From the queryset, we create three lists for the three different data types and a list for the dates
        total_infections = [record.total_infections for record in records]
        total_deaths = [record.total_deaths for record in records]
        incidence = [record.incidence for record in records]
        dates = [record.date for record in records]

        # We append the data lists to a dictionary
        data = {
            'total_infections': total_infections,
            'total_deaths': total_deaths,
            'incidence': incidence,
        }

        # We iterate through the data dictonary
        for key, value in data.items():
            # We create a figure for the data
            p = figure(plot_width=400, plot_height=400, x_axis_type='datetime', sizing_mode='stretch_width', tools="pan,wheel_zoom,box_zoom,reset")
            # We add the data to the figure
            p.line(dates, value, line_width=2)

            # We format the days display in the x-axis
            p.xaxis.formatter = DatetimeTickFormatter(days='%m/%d')
            # We format the y-axis to only integers
            p.yaxis.formatter = BasicTickFormatter(use_scientific=False, precision=0)
            
            # We remove the toolbar and logo
            p.toolbar.logo = None
            #p.toolbar_location = None

            # We split the figure into a script and a div
            script, div = components(p)
            
            # We add the script and div to the plot dictionary
            plot[country][key] = {
                'script': script,
                'div': div,
            }

    return render(request, 'index.html', {'plot': plot})

def download(request):

    # We create an empty HDF5 file
    hdf5_file = pd.HDFStore('static/data.h5')

    # We iterate through the countries
    for country in ['Germany', 'Austria', 'Switzerland']:
        # We retrieve all records for the country sorted by ascending date
        records = Record.objects.filter(country=country).order_by('date')
        # We create a dataframe from the queryset.
        df = pd.DataFrame(list(records.values()), columns=['date', 'total_infections', 'total_deaths', 'incidence'])
        # We remove the time component from the date
        df['date'] = df['date'].dt.date
        # We convert the date to a string
        df['date'] = df['date'].astype(str)
        # We convert the incidence column to a float
        df['incidence'] = df['incidence'].astype(float)

        # We append the dataframe to a HDF5 file, key = country
        hdf5_file.put(country, df, format='table', data_columns=True)

    # We close the HDF5 file
    hdf5_file.close()

    # We send the HDF5 file to the browser
    response = HttpResponse(open('static/data.h5', 'rb'), content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename=data.h5'

    return response

