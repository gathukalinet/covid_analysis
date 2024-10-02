import pandas as pd  
import plotly          
import plotly.express as px

import dash             
from dash import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']  # Adding external CSS for layout

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#---------------------------------------------------------------

df = pd.read_excel(r'C:\Users\User\Downloads\Covid 19 dashboard with Instruction to Deployment-20241001\Materials\data\coviddata.xlsx')

dff = df.groupby('countriesAndTerritories', as_index=False)[['deaths','cases']].sum()
print (dff[:5])
#---------------------------------------------------------------
app.layout = html.Div([
    html.Div([
        html.H1('Covid-19 Cases Analysis', style={'textAlign': 'center','fontFamily': 'Lucida Bright, monospace'}),
        html.H3('Data Table displaying cases and death reported per Country',style={'textAlign': 'center','fontFamily': 'Lucida Bright, monospace'})
]),
    html.Div([
        dash_table.DataTable(
            id='datatable_id',
            data=dff.to_dict('records'),
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": False} for i in dff.columns
            ],
             style_header={'backgroundColor': 'rgb(30, 30, 30)','color': 'white'
            },
            editable=False,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            row_selectable="multi",
            row_deletable=False,
            selected_rows=[],
            page_action="native",
            page_current= 0,
            page_size= 6,
            # page_action='none',
            # style_cell={
            # 'whiteSpace': 'normal'
            # },
            # fixed_rows={ 'headers': True, 'data': 0 },
            # virtualization=False,
            style_cell_conditional=[
                {'if': {'column_id': 'countriesAndTerritories'},
                 'width': '40%', 'textAlign': 'center'},
                {'if': {'column_id': 'deaths'},
                 'width': '30%', 'textAlign': 'center'},
                {'if': {'column_id': 'cases'},
                 'width': '30%', 'textAlign': 'center'},
            ],
        ),
    ],className='row'),

    html.Div([
        html.Div([
            dcc.Dropdown(id='linedropdown',
                options=[
                         {'label': 'Deaths', 'value': 'deaths'},
                         {'label': 'Cases', 'value': 'cases'}
                ],
                value='deaths',
                multi=False,
                clearable=False
            ),
        ],className='six columns'),

        html.Div([
        dcc.Dropdown(id='piedropdown',
            options=[
                     {'label': 'Deaths', 'value': 'deaths'},
                     {'label': 'Cases', 'value': 'cases'}
            ],
            value='cases',
            multi=False,
            clearable=False
        ),
        ],className='six columns'),

    ],className='row'),

    html.Div([
       html.Div([
            html.H3('Line-Chart on Reported Cases and Deaths', style={'textAlign': 'center','fontFamily': 'Lucida Bright, monospace'}),
            dcc.Graph(id='linechart',style={'width': '100%'})
        ], className='six columns', style={'padding': '10px'}), 

        html.Div([
            html.H3('Pie-Chart on Reported Cases and Deaths', style={'textAlign': 'center','fontFamily': 'Lucida Bright, monospace'}),
            dcc.Graph(id='piechart',style={'width': '100%'})
        ], className='six columns', style={'padding': '10px'})  
    ], className='row')  
])

#------------------------------------------------------------------
@app.callback(
    [Output('piechart', 'figure'),
     Output('linechart', 'figure')],
    [Input('datatable_id', 'selected_rows'),
     Input('piedropdown', 'value'),
     Input('linedropdown', 'value')]
)
def update_data(chosen_rows,piedropval,linedropval):
    if len(chosen_rows)==0:
        df_filterd = dff[dff['countriesAndTerritories'].isin(['China','Iran','Spain','Italy'])]
    else:
        print(chosen_rows)
        df_filterd = dff[dff.index.isin(chosen_rows)]

    pie_chart=px.pie(
            data_frame=df_filterd,
            names='countriesAndTerritories',
            values=piedropval,
            hole=.3,
            labels={'countriesAndTerritories':'Countries'}
            )


    #extract list of chosen countries
    list_chosen_countries=df_filterd['countriesAndTerritories'].tolist()
    #filter original df according to chosen countries
    #because original df has all the complete dates
    df_line = df[df['countriesAndTerritories'].isin(list_chosen_countries)]

    line_chart = px.area(
            data_frame=df_line,
            x='dateRep',
            y=linedropval,
            color='countriesAndTerritories',
            labels={'countriesAndTerritories':'Countries', 'dateRep':'date'},
            )
    line_chart.update_layout(uirevision='foo')

    return (pie_chart,line_chart)

#------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)