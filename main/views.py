from django.shortcuts import render
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.formatters import DatetimeTickFormatter, BasicTickFormatter

from .models import Record

from datetime import datetime, timedelta


def index(request):

    # We init the plot dictionary
    plot = dict()

    for country in ['Germany', 'Austria', 'Switzerland']:

        # We init the country dictionary inside the plot dictionary
        plot[country] = {}

        # We retrieve all records for the country
        records = Record.objects.filter(country=country)

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
