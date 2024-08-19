import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import numpy as np
import tkinter as tk
from tkinter import simpledialog
import multiprocessing
import time

# Configuración de la conexión
server = 'mssql-174217-0.cloudclusters.net,10034'
database = 'QuantumEnergia'
username = 'Dictum'
password = 'KtqF86wd'

# Cadena de conexión
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

def abrir_ventana_grafica(df_lecturas, plantas, ventana_id):
    # Configurar la figura y el gráfico
    fig, ax = plt.subplots(figsize=(16, 10))
    plt.style.use('ggplot')

    def actualizar_grafica(i):
        # Rotar entre plantas
        planta = plantas[i % len(plantas)]
        
        # Filtrar los datos para la planta seleccionada y el rango de fechas de hoy a 30 días atrás
        fecha_hoy = df_lecturas['FECHA'].max()
        fecha_inicio = fecha_hoy - timedelta(days=30)
        df_filtrado = df_lecturas[(df_lecturas['NOMBRE_CORTO'] == planta) & 
                                   (df_lecturas['FECHA'] >= fecha_inicio) & 
                                   (df_lecturas['FECHA'] <= fecha_hoy)]
        
        # Aplicar la transformación: (Indisponibilidad Técnica - 100) * -1
        df_filtrado['Disponibilidad'] = (df_filtrado['Indisponilbilidad Técnica'] - 100) * -1

        # Actualizar la gráfica
        ax.clear()
        ax.plot(df_filtrado['FECHA'], df_filtrado['Disponibilidad'], color=np.random.rand(3,), linewidth=2, marker='o', markersize=6)
        ax.set_title(f'Disponibilidad Técnica de {fecha_inicio.strftime("%Y-%m-%d")} hasta {fecha_hoy.strftime("%Y-%m-%d")} de {planta}', fontsize=18, fontweight='bold')
        ax.set_xlabel('Fecha', fontsize=14, fontweight='bold')
        ax.set_ylabel('Disponibilidad (%)', fontsize=14, fontweight='bold')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
        ax.tick_params(axis='x', rotation=45)
        ax.tick_params(axis='both', which='major', labelsize=12)
        ax.set_xlim([fecha_inicio, fecha_hoy])
        ax.set_ylim(98, 100.1)
        plt.tight_layout()

    # Configurar la animación para actualizar cada 10 segundos
    ani = FuncAnimation(fig, actualizar_grafica, interval=10000, frames=len(plantas))

    # Mostrar la gráfica en pantalla completa
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    plt.show()

def main():
    try:
        # Establecer la conexión
        connection = pyodbc.connect(connection_string)
        print("Conexión exitosa a la base de datos")

        # Crear el cursor y ejecutar la consulta
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
            P.[ID] NOT IN (1, 5, 12); 
        """

        # Cargar los resultados en un DataFrame
        df_lecturas = pd.read_sql(query_lecturas, connection)
        df_lecturas['FECHA'] = pd.to_datetime(df_lecturas['FECHA'])

        # Obtener la lista de plantas
        plantas = df_lecturas['NOMBRE_CORTO'].unique()

        # Ventana para pedir la cantidad de ventanas
        root = tk.Tk()
        root.withdraw()
        num_ventanas = simpledialog.askinteger("Número de Ventanas", f"Ingrese el número de ventanas a abrir (máximo {len(plantas)}):", minvalue=1, maxvalue=len(plantas))

        # Dividir plantas para cada ventana
        plantas_por_ventana = np.array_split(plantas, num_ventanas)

        # Crear y ejecutar un proceso por cada ventana gráfica
        procesos = []
        for i, plantas_ventana in enumerate(plantas_por_ventana):
            proceso = multiprocessing.Process(target=abrir_ventana_grafica, args=(df_lecturas, plantas_ventana, i))
            procesos.append(proceso)
            proceso.start()
            time.sleep(1)  # Dar un pequeño retraso entre la apertura de ventanas para evitar conflictos

        for proceso in procesos:
            proceso.join()

    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")

if __name__ == "__main__":
    multiprocessing.freeze_support()  # Necesario para compatibilidad en Windows
    main()
