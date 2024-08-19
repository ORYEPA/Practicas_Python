import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import numpy as np
from matplotlib.ticker import MaxNLocator

# Configuración de la conexión
server = 'mssql-174217-0.cloudclusters.net,10034'
database = 'QuantumEnergia'
username = 'Dictum'
password = 'KtqF86wd'

# Cadena de conexión
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

try:
    # Establecer la conexión
    connection = pyodbc.connect(connection_string)
    print("Conexión exitosa a la base de datos")

    # Crear el cursor y ejecutar la consulta para obtener los datos necesarios
    cursor = connection.cursor()
    query_lecturas = """
    SELECT 
        L.[FECHA],
        L.[Indisponilbilidad Técnica],
        P.[NOMBRE_CORTO]
    FROM 
        [QuantumEnergia].[dbo].[QE_LECTURAS_DIARIAS] as L
    JOIN
        [QuantumEnergia].[dbo].[QE_PLANTA] as P
    ON
        L.IDPLANTA = P.ID
    WHERE 
        P.[ID] NOT IN (1, 5, 12); -- Excluir los IDs 1, 5 y 12
    """

    # Cargar los resultados en un DataFrame de pandas
    df_lecturas = pd.read_sql(query_lecturas, connection)

    # Cerrar la conexión a la base de datos
    cursor.close()
    connection.close()

    # Convertir la columna FECHA a formato datetime
    df_lecturas['FECHA'] = pd.to_datetime(df_lecturas['FECHA'])

    # Obtener la lista de plantas (NOMBRE_CORTO)
    plantas = df_lecturas['NOMBRE_CORTO'].unique()
    num_plantas = len(plantas)

    # Colores para las líneas
    colores = plt.cm.tab10(np.linspace(0, 1, num_plantas))

    # Configurar la figura y el gráfico con tamaño fijo
    fig, ax = plt.subplots(figsize=(16, 10))  # Tamaño fijo de la figura
    plt.style.use('ggplot')  # Usar un estilo alternativo

    # Ajustar los márgenes para separar el título
    plt.subplots_adjust(top=0.85)  # Ajustar el espacio superior

    # Función de actualización de la gráfica con transición
    def actualizar_grafica(i):
        # Determinar la planta actual basada en el índice de animación
        planta = plantas[i % num_plantas]

        # Filtrar los datos para la planta seleccionada y el rango de fechas de hoy a 30 días atrás
        fecha_hoy = df_lecturas['FECHA'].max()
        fecha_inicio = fecha_hoy - timedelta(days=30)
        df_filtrado = df_lecturas[(df_lecturas['NOMBRE_CORTO'] == planta) & 
                                   (df_lecturas['FECHA'] >= fecha_inicio) & 
                                   (df_lecturas['FECHA'] <= fecha_hoy)]

        # Aplicar la transformación: (Indisponibilidad Técnica - 100) * -1
        df_filtrado['Disponibilidad'] = (df_filtrado['Indisponilbilidad Técnica'] - 100) * -1

        # Limpiar el eje para redibujar
        ax.clear()

        # Dibujar la nueva gráfica con una transición de color
        color = colores[i % num_plantas]
        ax.plot(df_filtrado['FECHA'], df_filtrado['Disponibilidad'], label='Disponibilidad (%)', color=color, linewidth=2, marker='o', markersize=6)

        # Ajustar título
        ax.set_title(f'Disponibilidad Técnica de {fecha_inicio.strftime("%Y-%m-%d")} hasta {fecha_hoy.strftime("%Y-%m-%d")} de {planta}', 
                      fontsize=18, fontweight='bold')

        # Configurar etiquetas y estilo
        ax.set_xlabel('Fecha', fontsize=14, fontweight='bold')
        ax.set_ylabel('Disponibilidad (%)', fontsize=14, fontweight='bold')
        
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
        ax.tick_params(axis='x', rotation=45)
        ax.tick_params(axis='both', which='major', labelsize=12)

        # Añadir una cuadrícula suave
        ax.grid(True, linestyle='--', alpha=0.6)

        # Configurar los límites para una transición suave
        ax.set_xlim([fecha_inicio, fecha_hoy])
        ax.set_ylim(0, 101)  # Establecer el límite superior del eje Y en 100

        # Mejorar la visualización
        plt.tight_layout()

    # Configurar la animación para actualizar cada 10 segundos con una transición suave
    ani = FuncAnimation(fig, actualizar_grafica, interval=10000, repeat=True)

    # Configurar la gráfica en pantalla completa
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()

    # Mostrar la gráfica
    plt.show()

except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
