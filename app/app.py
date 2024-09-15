import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
from flask import Flask
import pandas as pd
import plotly.express as px
import os

# Inicializar Flask
server = Flask(__name__)

# Inicializar Dash
app = dash.Dash(__name__, server=server, url_base_pathname='/dash/', suppress_callback_exceptions=True)

# Ruta de la carpeta donde se encuentran los archivos CSV
path_Predictions = r'C:\\Users\\joset\\OneDrive\\Documentos\\Master Big Data UCM\\18-TFN\\NaturgyProject\\data\\Predictions\\'
path = r'C:\\Users\\joset\\OneDrive\\Documentos\\Master Big Data UCM\\18-TFN\\NaturgyProject\\data'

# Asegúrate de que la ruta termine con una barra invertida
if not path_Predictions.endswith('\\'):
    path_Predictions += '\\'

# Cargar los datos del archivo CSV para el mapa de consumo
provincia_coef_mes = pd.read_csv(os.path.join(path, 'Cleaning', 'provincia_coef_mes.csv'), encoding='latin1')
# Convertir la columna AÑO_MES a tipo datetime
provincia_coef_mes.rename(columns={'AÃO_MES': 'AÑO_MES'}, inplace=True)
provincia_coef_mes['AÑO_MES'] = pd.to_datetime(provincia_coef_mes['AÑO_MES'])
provincia_coef_mes['AÑO_MES'] = provincia_coef_mes['AÑO_MES'].dt.strftime('%Y-%m')

# Normalizar los nombres de las provincias
provincia_coef_mes['PROVINCIA'] = provincia_coef_mes['PROVINCIA'].str.upper()

# Crear el gráfico inicial utilizando el primer mes disponible
initial_month = provincia_coef_mes['AÑO_MES'].min()
df_initial = provincia_coef_mes[provincia_coef_mes['AÑO_MES'] == initial_month]

# Crear el gráfico de barras
fig_barras_consumo = px.bar(
    df_initial,
    x="PROVINCIA",
    y="Consumo_kWh",
    hover_data=["%_Consumo"],
    labels={'Consumo_kWh': 'Consumo (kWh)', '%_Consumo': '% Consumo'},
    title=f"Consumo de Gas por Provincia - {initial_month}",
    color="Consumo_kWh",
    color_continuous_scale="Oranges"
)
fig_barras_consumo.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})

# Opciones para las comercializadoras y horizontes
comercializadoras = ['GNS', 'NC', 'SUR']
horizontes = ['N1', 'M3', 'M15']

# Definir el layout de la aplicación
app.layout = html.Div(children=[
    # Barra superior con botones en la parte izquierda con estilo flotante
    html.Div(children=[
        html.A('Predicciones', href="#predicciones-section", style={
            'margin': '10px',
            'background-color': '#CCCCCC',
            'color': '#FF4E00',
            'border': '2px solid #666666',
            'padding': '10px 15px',  # Ajuste de padding para más espacio
            'border-radius': '5px',
            'font-size': '14px',
            'cursor': 'pointer',
            'text-decoration': 'none'
        }),
        html.A('Tabla Predicciones', href="#tabla-consumo-section", style={
            'margin': '10px',
            'background-color': '#CCCCCC',
            'color': '#FF4E00',
            'border': '2px solid #666666',
            'padding': '10px 15px',  # Ajuste de padding para más espacio
            'border-radius': '5px',
            'font-size': '14px',
            'cursor': 'pointer',
            'text-decoration': 'none'
            
        }),
        html.A('Historico', href="#consumo-section", style={
            'margin': '10px',
            'background-color': '#CCCCCC',
            'color': '#FF4E00',
            'border': '2px solid #666666',
            'padding': '10px 15px',  # Ajuste de padding para más espacio
            'border-radius': '5px',
            'font-size': '14px',
            'cursor': 'pointer',
            'text-decoration': 'none'
        }),
        

    ], style={
        'position': 'fixed',
        'top': '0',
        'left': '0',  # Ajustamos el contenedor hacia la izquierda
        'right': '0',
        'width': '100%',
        'display': 'flex',
        'justify-content': 'flex-start',  # Alineación a la izquierda
        'padding': '15px',
        'background-color': 'transparent',
        'z-index': '800'
    }),
    

    # Espaciado para compensar la barra fija
    html.Div(id='predicciones-section', style={'height': '60px'}),  # Ajustar este valor según la altura de la barra fija

    # Sección de predicciones con un id para referencia
    html.Div(
        children=[
            # Título estilizado
            html.Div(children=[
                html.Span("Dashboard de Predicciones de", style={'color': '#004481', 'font-size': '36px', 'font-family': 'sans-serif'}),
                html.Span(" Gas", style={'color': '#FF4E00', 'font-size': '36px', 'font-family': 'sans-serif', 'font-weight': 'bold'})
            ], style={'text-align': 'center', 'margin-bottom': '30px', 'margin-top': '10px'}),

            # Contenedor para la selección de comercializadora y horizonte (disposición horizontal)
            html.Div(children=[
                # Dropdown para seleccionar la comercializadora
                html.Div(children=[
                    html.Label('Seleccionar Comercializadora', style={'color': 'black', 'text-align': 'center'}),
                    dcc.Dropdown(
                        id='comercializadora-dropdown',
                        options=[{'label': comercializadora, 'value': comercializadora} for comercializadora in comercializadoras],
                        value='GNS',  # Valor inicial
                        clearable=False,
                        style={'width': '200px'}
                    )
                ], style={'margin-right': '20px'}),  # Margen derecho para espacio entre elementos

                # Slider para seleccionar el horizonte (como una línea de tiempo)
                html.Div(children=[
                    html.Label('Seleccionar Horizonte', style={'color': 'black', 'text-align': 'center'}),
                    dcc.Slider(
                        id='horizonte-slider',
                        min=0,
                        max=len(horizontes) - 1,
                        marks={i: horizonte for i, horizonte in enumerate(horizontes)},
                        value=0,
                        step=1,
                        included=False,
                        tooltip={"placement": "bottom", "always_visible": True},
                        updatemode='drag'
                    )
                ], style={'width': '300px'})  # Ancho del slider acortado a 300px
            ], style={
                'display': 'flex',
                'align-items': 'center',
                'justify-content': 'center',
                'margin-bottom': '40px'
            }),

            # Contenedor de gráficos (solo 2 gráficos, línea y barras)
            html.Div(children=[
                dcc.Graph(id='graph-1', style={'width': '100%', 'height': '400px', 'margin': '5px'}),
                dcc.Graph(id='graph-2', style={'width': '100%', 'height': '400px', 'margin': '5px'})
            ], style={'display': 'flex', 'justify-content': 'space-around'})
        ],
        id='predicciones-container'  # Opcional: añadir un ID para facilitar el acceso
    ),
    
    # Sección de la tabla de consumo
    html.Div(children=[
        # Título de la tabla
        html.Div(children=[
            html.Span("Predicciones consumo de Gas", style={'color': '#004481', 'font-size': '36px', 'font-family': 'sans-serif'}),
            html.Span(" Proximos dias", style={'color': '#FF4E00', 'font-size': '36px', 'font-family': 'sans-serif', 'font-weight': 'bold'})
        ], style={'text-align': 'center', 'margin-bottom': '30px', 'margin-top': '75px','padding-top': '105px'}),
        
        # Contenedor de la tabla
        html.Div(children=[
            dash_table.DataTable(
                id='data-table',
                columns=[],
                data=[],
                style_table={'overflowX': 'auto','backgroundColor': 'transparent'},
                style_cell={'textAlign': 'center', 'padding': '5px', 'whiteSpace': 'normal','color': 'black'},
                style_header={
                'backgroundColor': '#FF4E00',  # Cabeceras en naranja
                'color': 'white',
                'fontWeight': 'bold',
                'textAlign': 'center'
            },
                style_data={
                'backgroundColor': 'transparent',  # Fondo transparente en los datos
                'color': 'black'  # Texto en negro
            },
            )
        ], style={'width': '80%', 'margin': '20px auto'}),
    ], id='tabla-consumo-section'),  # Opcional: añadir un ID para facilitar el acceso

    # Sección del mapa de consumos
    html.Div(id='consumo-section',
             children=[
                 html.Div([
                     html.Span("Consumo de Gas agrupado por ", style={
                         'color': '#004481', 
                         'font-size': '36px', 
                         'font-family': 'sans-serif',
                         'display': 'inline-block',  # Mantiene el texto en línea
                         'text-align': 'center',
                         'margin-right': '10px'
                     }),
                     html.Span(" Provincia", style={
                         'color': '#FF4E00', 
                         'font-size': '36px', 
                         'font-family': 'sans-serif', 
                         'font-weight': 'bold',
                         'display': 'inline-block',  # Mantiene el texto en línea
                         'text-align': 'center'
                     })
                 ], style={'text-align': 'center', 'padding-top': '65px'}), 
                 
                 # Dropdown para seleccionar el mes
                 html.Div([
                     dcc.Dropdown(
                         id='mes-dropdown',
                         options=[{'label': date, 'value': date} for date in provincia_coef_mes['AÑO_MES'].unique()],
                         value=provincia_coef_mes['AÑO_MES'].unique()[0],  # Valor inicial
                         clearable=False,
                         style={'width': '40%', 'margin': 'auto', 'z-index': '9999'}  # Achica el ancho del dropdown
                     )
                 ], style={'width': '40%', 'margin': 'auto', 'z-index': '9999'}),  # Ajusta el contenedor del dropdown
                 
                 # Gráfico de barras
                 html.Div([
                     dcc.Graph(id='barras-consumo', figure=fig_barras_consumo, style={'width': '80%', 'height': '500px', 'margin': '0 auto'})
                 ], style={'display': 'flex', 'justify-content': 'center'})
             ])
], style={
    'backgroundColor': 'transparent',
    'padding': '0px',
    'border': 'none'
})

# Función para cargar el dataset basado en la selección
def cargar_dataset(comercializadora, horizonte):
    file_name = f"{comercializadora}_{horizonte}.xlsx"
    file_path = os.path.join(path_Predictions, file_name)
    
    if os.path.exists(file_path):
        try:
            df = pd.read_excel(file_path)
            df['Fecha'] = pd.to_datetime(df['Fecha'])  # Convertir la columna de fechas a datetime
            return df
        except Exception as e:
            print(f"Error al cargar el archivo {file_path}: {e}")
            return None
    else:
        print(f"Archivo no encontrado: {file_path}")
        return None

# Callback para actualizar los gráficos y la tabla en función de las selecciones
@app.callback(
    [Output('graph-1', 'figure'),
     Output('graph-2', 'figure'),
     Output('barras-consumo', 'figure'),
     Output('data-table', 'columns'),
     Output('data-table', 'data')],
    [Input('comercializadora-dropdown', 'value'),
     Input('horizonte-slider', 'value'),
     Input('mes-dropdown', 'value')]
)
def update_graphs_and_table(selected_comercializadora, selected_horizonte, selected_month):
    # Convertir el índice del slider al valor correspondiente
    horizonte = horizontes[selected_horizonte]
    df = cargar_dataset(selected_comercializadora, horizonte)

    # Actualización de los gráficos de predicciones
    if df is not None:
        # Gráfico de línea
        fig1 = {
            'data': [{'x': df['Fecha'], 'y': df['Prediccion'], 'type': 'line', 'name': selected_comercializadora}],
            'layout': {
                'title': f'Predicción de Gas - {selected_comercializadora} (Horizonte {horizonte})',
                'plot_bgcolor': 'rgba(255, 255, 255, 0)',
                'paper_bgcolor': 'rgba(255, 255, 255, 0)',
                'font': {'color': 'black'}
            }
        }
        # Gráfico de barras
        fig2 = {
            'data': [{'x': df['Fecha'], 'y': df['Prediccion'], 'type': 'bar', 'name': selected_comercializadora}],
            'layout': {
                'title': f'Predicción de Gas (Barras) - {selected_comercializadora} (Horizonte {horizonte})',
                'plot_bgcolor': 'rgba(255, 255, 255, 0)',
                'paper_bgcolor': 'rgba(255, 255, 255, 0)',
                'font': {'color': 'black'}
            }
        }
    else:
        fig1, fig2 = {}, {}

    # Actualización del consumo por provincia
    df_filtered = provincia_coef_mes[provincia_coef_mes['AÑO_MES'] == selected_month]
    df_filtered = df_filtered.sort_values(by='Consumo_kWh', ascending=False)

    fig3 = px.bar(
        df_filtered,
        x="PROVINCIA",
        y="Consumo_kWh",
        hover_data=["%_Consumo"],
        labels={'Consumo_kWh': 'Consumo (kWh)', '%_Consumo': '% Consumo'},
        title=f"Consumo de Gas por Provincia - {selected_month}",
        color="Consumo_kWh",
        color_continuous_scale="Oranges"
    )
    
    fig3.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Fondo del gráfico transparente
        paper_bgcolor='rgba(0,0,0,0)'  # Fondo del papel transparente
    )

    # Actualización de la tabla
    if df is not None:
        columns = [{"name": i, "id": i} for i in df.columns]
        data = df.to_dict('records')
    else:
        columns, data = [], []

    return fig1, fig2, fig3, columns, data

# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)
