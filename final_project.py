from dash import dcc, html
#import plotly.graph_objects as go
#import plotly.express as px
#import matplotlib.pyplot as plt
import pandas as pd
#import numpy as np
#import seaborn as sns
#import re
import dash
from dash.dependencies import Input, Output, State

path ='https://raw.github.com/ricardosequeira1/Data-Visualization-Project/tree/main/data'

# Data
data = pd.read_csv(path + 'database.csv')

strikes = [data[['Radome Strike',
                 'Windshield Strike',
                 'Nose Strike',
                 'Engine1 Strike',
                 'Engine2 Strike',
                 'Engine3 Strike',
                 'Engine4 Strike',
                 'Propeller Strike',
                 'Wing or Rotor Strike',
                 'Fuselage Strike',
                 'Landing Gear Strike',
                 'Tail Strike',
                 'Lights Strike',
                 'Other Strike']]]

damages = [data[['Aircraft Damage',
                 'Radome Damage',
                 'Windshield Damage',
                 'Nose Damage',
                 'Engine1 Damage',
                 'Engine2 Damage',
                 'Engine3 Damage',
                 'Engine4 Damage',
                 'Engine Ingested',
                 'Propeller Damage',
                 'Wing or Rotor Damage',
                 'Fuselage Damage',
                 'Landing Gear Damage',
                 'Tail Damage',
                 'Lights Damage',
                 'Other Damage']]]

# Interactive Components

airline_options = [dict(label=airline, value=airline) for airline in data['Operator'].unique()]

aircraft_options = [dict(label=aircraft, value=aircraft) for aircraft in data['Aircraft'].unique()]

airport_options = [dict(label=airport, value=airport) for airport in data['Airport'].unique()]

region_options = [dict(label=region, value=region) for region in data['FAA Region'].unique()]

species_options = [dict(label=species, value=species) for species in data['Species Name'].unique()]

strikes_options = [dict(label=strikes, value=strikes) for strikes in strikes]

damages_options = [dict(label=damages, value=damages) for damages in damages]

dropdown_airline = dcc.Dropdown(
    id='airline_drop',
    options=airline_options,
    value=['TAP AIR Portugal'],
    multi=True)

dropdown_aircraft = dcc.Dropdown(
    id='aircraft_option',
    options=aircraft_options,
    value=[],
    multi=True)

dropdown_airport = dcc.Dropdown(
    id='airport_option',
    options=airport_options,
    value=[],
    multi=True)

dropdown_region = dcc.Dropdown(
    id='region_option',
    options=region_options,
    value=['ASO'],
    multi=True)

dropdown_species = dcc.Dropdown(
    id='species_option',
    options=species_options,
    value=[],
    multi=True)

dropdown_strikes = dcc.Dropdown(
    id='strikes_option',
    options=strikes_options,
    value=['Nose Strike'],
    multi=True)

dropdown_damages = dcc.Dropdown(
    id='damages_option',
    options=damages_options,
    value=['Nose Damage'],
    multi=True)

slider_year = dcc.Slider(
    id='year_slider',
    min=data['Incident Year'].min(),
    max=data['Incident Year'].max(),
    marks={str(i): '{}'.format(str(i)) for i in
           [1990, 1995, 2000, 2005, 2010, 2015]},
    value=data['Incident Year'].min(),
    step=1)

# App

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
    html.H1('Airport Wildlife Strikes Dashboard'),
    html.Label('Airline Choice'),
    dropdown_airline,
    html.Br(),
    html.Label('Aircraft Choice'),
    dropdown_aircraft,
    html.Br(),
    html.Label('Airport Choice'),
    dropdown_airport,
    html.Br(),
    html.Label('Region Choice'),
    dropdown_region,
    html.Br(),
    html.Label('Species Choice'),
    dropdown_species,
    html.Br(),
    html.Label('Strikes Choice'),
    dropdown_strikes,
    html.Br(),
    html.Label('Damages Choice'),
    dropdown_damages,
    html.Br(),
    html.Label('Year Slider'),
    slider_year,
    html.Br(),
    dcc.Graph(id='bar_graph')
])


# Callbacks

@app.callback(
    [
        Output("bar_graph", "figure"),
        Output("bar_graph", "figure")
    ],
    [
        Input("year_slider", "value"),
        Input("region_drop", "value"),
        Input("airline_option", "value"),
        Input("aircraft_option", "value"),
        Input("airport_option", "value"),
        Input("species_option", "value"),
        Input("strikes_option", "value"),
        Input("damages_option", "value")])

# First Bar Plot
def plots_strikes(year, regions, airline, aircraft, airport, species, strikes):
    data_bar = []
    for region in regions:
        df_bar = data.loc[((data['FAA Region'] == region)
                           & (data['Operator'] == airline)
                           & (data['Aircraft'] == aircraft)
                           & (data['Incident Year'] == year)
                           & (data['Airport'] == airport)
                           & (data['Species Name'] == species))]
        df_bar['Strikes'] = df_bar[['Radome Strike',
                                        'Windshield Strike',
                                        'Nose Strike',
                                        'Engine1 Strike',
                                        'Engine2 Strike',
                                        'Engine3 Strike',
                                        'Engine4 Strike',
                                        'Propeller Strike',
                                        'Wing or Rotor Strike',
                                        'Fuselage Strike',
                                        'Landing Gear Strike',
                                        'Tail Strike',
                                        'Lights Strike',
                                        'Other Strike']].sum(axis=1)

        x_bar = df_bar['Incident Year']
        y_bar = df_bar['Strikes']

        data_bar.append(dict(type='bar', x=x_bar, y=y_bar, name=region))

    layout_bar = dict(title=dict(text='Airport Wildlife from 1990 until 2015'),
                      yaxis=dict(title='Strikes'),
                      paper_bgcolor='#f9f9f9')

def plots_damages(year, regions, airline, aircraft, airport, species, damages):
    data_bar = []
    for region in regions:
        df_bar = data.loc[((data['FAA Region'] == region)
                           & (data['Operator'] == airline)
                           & (data['Aircraft'] == aircraft)
                           & (data['Incident Year'] == year)
                           & (data['Airport'] == airport)
                           & (data['Species Name'] == species))]
        df_bar['Damages'] = df_bar[['Aircraft Damage',
                                    'Radome Damage',
                                    'Windshield Damage',
                                    'Nose Damage',
                                    'Engine1 Damage',
                                    'Engine2 Damage',
                                    'Engine3 Damage',
                                    'Engine4 Damage',
                                    'Engine Ingested',
                                    'Propeller Damage',
                                    'Wing or Rotor Damage',
                                    'Fuselage Damage',
                                    'Landing Gear Damage',
                                    'Tail Damage',
                                    'Lights Damage',
                                    'Other Damage']].sum(axis=1)

        x_bar = df_bar['Incident Year']
        y_bar = df_bar['Damages']

        data_bar.append(dict(type='bar', x=x_bar, y=y_bar, name=region))

    layout_bar = dict(title=dict(text='Airport Wildlife from 1990 until 2015'),
                      yaxis=dict(title='Damages'),
                      paper_bgcolor='#f9f9f9')


if __name__ == '__main__':
    app.run_server(debug=False)