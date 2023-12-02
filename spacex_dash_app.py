# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

# Read the SpaceX data into pandas dataframe
spacex_df = pd.read_csv('/home/project/spacex_launch_dash.csv')

# Create a dash application
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', 
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # Dropdown for selecting Launch Site
    dcc.Dropdown(id='site-dropdown',
                 options=[{'label': 'All Sites', 'value': 'ALL'}] +
                         [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True),
    html.Br(),

    # Graph for success-pie-chart
    dcc.Graph(id='success-pie-chart'),

    # Range Slider for selecting payload mass
    dcc.RangeSlider(id='payload-slider',
                    min=0,  # Update this based on your data
                    max=10000,  # Update this based on your data
                    step=1000,
                    value=[0, 10000],  # Update this based on your data
                    marks={i: f'{i}' for i in range(0, 10001, 1000)}),
    html.Br(),

    # Graph for success-payload-scatter-chart
    dcc.Graph(id='success-payload-scatter-chart'),

    # Additional Line Plot (Example)
    html.H2("Example Line Plot"),
    dcc.Graph(id='example-line-plot'),

    # Additional Scatter Plot (Example)
    html.H2("Example Scatter Plot"),
    dcc.Dropdown(
        id='scatter-feature-dropdown',
        options=[{'label': feature, 'value': feature} for feature in ['Feature1', 'Feature2']],  # Update with real features
        value='Feature1'
    ),
    dcc.Graph(id='example-scatter-plot'),
])

# Callback for the Pie Chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def update_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
    fig = go.Figure(data=[go.Pie(labels=filtered_df['class'], 
                                 values=filtered_df['Flight Number'])])  # Update this based on your data
    fig.update_layout(title='Launch Success Count for Site')
    return fig

# Callback for the Scatter Plot
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_plot(entered_site, payload_range):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    if entered_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
    fig = go.Figure(data=[go.Scatter(x=filtered_df['Payload Mass (kg)'], y=filtered_df['class'], 
                                     mode='markers')])  # Update this based on your data
    fig.update_layout(title='Payload vs. Outcome for Site')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
