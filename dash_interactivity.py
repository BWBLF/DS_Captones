# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
spacex_df['num']=1
# lay version
spacex_df['Version']=spacex_df['Booster Version'].apply(lambda x: x.split(' ')[1])
filtered_df = spacex_df.groupby(['Launch Site','class'])['num'].sum().reset_index()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div([html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                

                                html.Br(),
                                  dcc.Dropdown(id='site-dropdown',
                options=[
                    {'label': 'All Sites', 'value': 'ALL'},
                    {'label': 'CCAFS LC-40	', 'value': 'CCAFS LC-40	'},
                    {'label': 'CCAFS SLC-40	', 'value': 'CCAFS SLC-40	'},
                    {'label': 'KSC LC-39A	', 'value': 'KSC LC-39A	'},
                    {'label': 'VAFB SLC-4E	', 'value': 'VAFB SLC-4E	'},
                ],
                value='ALL',
                placeholder="All Sites",
                searchable=True,

                ),

                                
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Hr(),
                                dcc.RangeSlider(id='payload-slider',
                                                marks={'0':'0',
                                                       '2500':'2500',
                                                       '5000':'5000',
                                                       '7500':'7500',
                                                       '10000':'10000'},
                                                min=0, max=10000,step=1,
                                                value=[min_payload, max_payload]),
                                                

                                html.P("Payload range (Kg):"),
                               


                                #a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


#callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
              
def get_pie_chart(entered_site):
    #print(entered_site)
    filtered_df = spacex_df.groupby(['Launch Site','class'])['num'].sum().reset_index()
    if entered_site == 'ALL':
        fig = px.pie(filtered_df[filtered_df['class']==1], values='num', 
        names='Launch Site', 
        title='Total Success Launches By Site')
        return fig
    else:
        fig = px.pie(filtered_df[filtered_df['Launch Site']==entered_site.strip()], values='num', 
        names='class', 
        title=f'Total Success Launches By Site {entered_site}')
        return fig
        


#callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
                Input(component_id="payload-slider", component_property="value")])

def get_payload_chart(entered_site, payload):
    df = spacex_df
    
    fig = px.scatter(df,x='Payload Mass (kg)',y='class',color='Version', title='Correlation between Payload and Success for all Sites')

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)


    