import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Assuming CSV files are in the correct path
df_full_grouped = pd.read_csv('full_grouped.csv')
df_latest = pd.read_csv('country_wise_latest.csv')

# Initializing Dash app
app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

# App layout enhancements
app.layout = html.Div([
    html.Div([
        html.H1("COVID-19 Dashboard",
                style={'text-align': 'center', 'color': '#000000', 'font-family': 'Lato, sans-serif',
                       'margin-top': '20px', 'margin-bottom': '20px'}),
        html.H2("Visualizing the impact of COVID-19",
               style={'text-align': 'center', 'color': '#000000', 'font-family': 'Lato, sans-serif'}),
        html.P("A dashboard created by Etsub Demile and Ala'a Tamam",
               style={'text-align': 'center', 'color': '#555', 'font-family': 'Lato, sans-serif'}),
        html.Div([
            html.Div([
                html.Label("Select Country/Region:", style={'font-weight': 'bold', 'color': '#333'}),
                dcc.Dropdown(
                    id='location-input',
                    options=[{'label': i, 'value': i} for i in df_full_grouped['Country/Region'].unique()],
                    value=df_full_grouped['Country/Region'].unique()[0],  # Set default value to the first country
                    style={'margin-bottom': '20px'}
                ),
            ], className='six columns'),

            html.Div([
                html.Label("Select Date Range:", style={'font-weight': 'bold', 'color': '#333'}),
                dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date=df_full_grouped['Date'].min(),
                    end_date=df_full_grouped['Date'].max(),
                    display_format='YYYY-MM-DD',
                    style={'margin-bottom': '20px'}
                ),
            ], className='six columns'),
        ], className='row', style={'margin': '20px 0'}),

        html.Div([
            dcc.Graph(id='cumulative-confirmed-chart'),
            dcc.Graph(id='new-confirmed-chart'),
        ], className='row'),

        html.Div([
            dcc.Graph(id='latest-cumulative-confirmed-chart'),
            dcc.Graph(id='latest-new-confirmed-chart'),
        ], className='row'),
    ], style={'padding': '20px', 'border-radius': '15px', 'background': 'white',
              'box-shadow': '0 2px 4px rgba(176, 206, 255,.9)'}),
    html.Div([
        html.H2("Data Source:"),
    html.A("We sourced out data from Kaggle! Click here to access it.",
           href="https://www.kaggle.com/datasets/imdevskp/corona-virus-report", target="_blank",
           style={'color': '#2B3A67'}),
 ], style={'text-align': 'center', 'margin-top': '40px', 'font-family': 'Lato, sans-serif'}),
], style={'backgroundColor': '#D9E7FF', 'font-family': 'Lato, sans-serif', 'padding': '20px'})


# Callback for updating charts
@app.callback(
    [Output('cumulative-confirmed-chart', 'figure'),
     Output('new-confirmed-chart', 'figure'),
     Output('latest-cumulative-confirmed-chart', 'figure'),
     Output('latest-new-confirmed-chart', 'figure')],
    [Input('location-input', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_charts(selected_country, start_date, end_date):
    # Filter datasets for the selected inputs
    filtered_full_grouped_df = df_full_grouped[(df_full_grouped['Country/Region'] == selected_country) &
                                               (df_full_grouped['Date'] >= start_date) &
                                               (df_full_grouped['Date'] <= end_date)]

    # Plotly Express charts with updated aesthetics
    cumulative_confirmed_fig = px.line(filtered_full_grouped_df, x='Date', y='Confirmed',
                                       title=f'Cumulative Confirmed Cases - {selected_country}',
                                       template='plotly_white', color_discrete_sequence=['#636EFA'])
    cumulative_confirmed_fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')

    new_confirmed_fig = px.line(filtered_full_grouped_df, x='Date', y='New cases',
                                title=f'New Confirmed Cases - {selected_country}',
                                template='plotly_white', color_discrete_sequence=['#EF553B'])
    new_confirmed_fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')

    filtered_latest_df = df_latest[df_latest['Country/Region'] == selected_country]

    latest_cumulative_confirmed_fig = px.bar(filtered_latest_df, x='Country/Region', y='Confirmed',
                                             title=f'Latest Cumulative Confirmed Cases - {selected_country}',
                                             template='plotly_white', color_discrete_sequence=['#00CC96'])
    latest_cumulative_confirmed_fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')

    latest_new_confirmed_fig = px.bar(filtered_latest_df, x='Country/Region', y='New cases',
                                      title=f'Latest New Confirmed Cases - {selected_country}',
                                      template='plotly_white', color_discrete_sequence=['#AB63FA'])
    latest_new_confirmed_fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')

    return cumulative_confirmed_fig, new_confirmed_fig, latest_cumulative_confirmed_fig, latest_new_confirmed_fig


if __name__ == '__main__':
    app.run_server(debug=True)
