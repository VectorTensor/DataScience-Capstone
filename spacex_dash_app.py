# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)
options_x = {x: x for x in spacex_df['Launch Site'].unique()}
options_x['ALL'] = 'ALL Sites'
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options= options_x,
                                             value='ALL', placeholder="sites",searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),


                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=min_payload, max=max_payload,value=[min_payload,max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(
    Output('success-pie-chart','figure'),
    Input("site-dropdown","value")
)
def update_pie_chart(site_chosen):
    df = pd.DataFrame()
    if site_chosen =='ALL':
        df['names'] = spacex_df['Launch Site'].unique()
        df['success'] = [getSuccess(item) for item in df['names']]
        pie_chart = px.pie(df, names='names', values='success')
        return pie_chart
    else:

        df['outcome'] = ['success','failure']
        p = spacex_df[spacex_df['Launch Site'] == site_chosen]
        df['count']=[len(p[p['class'] == 1].index),len(p[p['class'] == 0].index)]
        print(df)
        pie_chart = px.pie(df, names='outcome', values='count')
        return pie_chart

def getSuccess(i):
    return spacex_df[spacex_df['Launch Site'] == i]['class'].sum()

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart','figure'),
    Input('site-dropdown',"value"),
    Input('payload-slider',"value")
)
def update_line_chart(site_chosen,payload_range):
    df = pd.DataFrame()
    print(payload_range)
    min = payload_range[0]
    max = payload_range[1]
    if site_chosen == 'ALL':
        x = spacex_df[(spacex_df['Payload Mass (kg)'] >= min) & (spacex_df['Payload Mass (kg)'] <= max)]
        df['Payload'] = x['Payload Mass (kg)']
        df['class'] = x['class']
        df['color'] = x['Booster Version Category']
    else:
        x = spacex_df[(spacex_df['Payload Mass (kg)'] >= min) & (spacex_df['Payload Mass (kg)'] <=max) &  (spacex_df['Launch Site'] == 'VAFB SLC-4E')]
        df['Payload'] = x['Payload Mass (kg)']
        df['class'] = x['class']
        df['color'] = x['Booster Version Category']

    scatter_plot = px.scatter(df,x='Payload', y='class',color='color')
    return scatter_plot





# Run the app
if __name__ == '__main__':
    app.run_server()
