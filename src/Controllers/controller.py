from src.Models.model import getModelAll
import pysd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import urllib3
import os
import mpld3
from decouple import config
import pandas as pd
import numpy as np

# --- CONFIGURACIÓN: Variables específicas que quieres controlar ---
VARIABLES_CONTROL = [
    'Tasa Compra',
    'tasa Venta',
    'Tasa obsolencia',
    'Efectividad por difusion',
    'Gastos por difusion',
    'Demanda por cliente',
    'Control de operaciones deseado',
    'Captacion por cliente actual',
    'Tiempo de permanencia promedio'
]

def load_model_file():
    ruta_archivo = os.path.join('assets/vensim', 'document.mdl')
    if not os.path.exists(ruta_archivo):
         try:
            url = config('APP_URL_VENSIM')
            http = urllib3.PoolManager()
            resp = http.request('GET', url)
            with open(ruta_archivo, 'wb') as archivo:
                archivo.write(resp.data)
         except Exception as e:
             print(f"Error descargando modelo: {e}")
    return pysd.read_vensim(ruta_archivo)

def get_model_constants(model):
    
    constants_list = []
    try:
        import re
        def to_pysd_name(name):
            return re.sub(r'[^a-zA-Z0-9]', '_', name).lower()

        for var_name in VARIABLES_CONTROL:
            try:
                py_name = to_pysd_name(var_name)
                if hasattr(model.components, py_name):
                    val = getattr(model.components, py_name)()
                    constants_list.append({'name': var_name, 'value': float(val)})
                else:
                     doc = model.doc()
                     row = doc[doc['Real Name'] == var_name]
                     if not row.empty:
                         actual_py_name = row.iloc[0]['Py Name']
                         val = getattr(model.components, actual_py_name)()
                         constants_list.append({'name': var_name, 'value': float(val)})
            except Exception as e:
                print(f"No se pudo leer valor inicial para '{var_name}': {e}")
                constants_list.append({'name': var_name, 'value': 0.0})

    except Exception as e:
        print(f"Error general obteniendo constantes: {e}")

    return constants_list

def generate_graph_html(stocks, info_nivel):
    fig, ax = plt.subplots()
    data = stocks[info_nivel['nameNivel']]
    
    ax.plot(data, label=info_nivel['nameNivel'], linewidth=3.0, color=info_nivel['nameColor'])
    ax.set_title(info_nivel['title'], loc='center', fontsize=12)
    ax.set_ylabel(info_nivel['nameLabelY'], fontsize=10)
    ax.set_xlabel(info_nivel['nameLabelX'], fontsize=10)
    ax.grid(True, which='both', linestyle='--', alpha=0.7)
    ax.legend(loc='best', fontsize=9)
    
    graph_html = mpld3.fig_to_html(fig)
    plt.close(fig)
    return graph_html

def controller():
    try:
        model = load_model_file()
        constants = get_model_constants(model)
        response_bd = getModelAll()

        if isinstance(response_bd, list) and len(response_bd) > 0 and isinstance(response_bd[0], dict) and 'message' in response_bd[0]:
             return response_bd

        nivel = {}
        stocks = model.run()
        
        for item in response_bd:
            try:
                info_nivel = {
                    "title": item[1], "nameLabelX": item[2], "nameLabelY": item[3], 
                    "nameNivel": item[5], "nameColor": item[6]
                }
                if info_nivel['nameNivel'] in stocks.columns:
                    nivel[info_nivel['nameNivel']] = {
                        'data': stocks[info_nivel['nameNivel']], 
                        'graph': generate_graph_html(stocks, info_nivel),
                        'info': info_nivel
                    }
            except:
                pass
        return {'niveles': nivel, 'constantes': constants}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return [{'message': f'Error interno: {str(e)}'}]

def simulate_new_run(params_received):
    try:
        model = load_model_file()
        target_nivel = params_received.get('target_nivel')
        
        new_params = {}
        final_time_val = None # Variable para guardar el tiempo final si se recibe

        # Procesamos los parámetros recibidos
        for k, v in params_received.get('params', {}).items():
            try:
                val = float(v)
                # Si el parámetro es FINAL TIME, lo guardamos por separado
                if k == 'FINAL TIME':
                    final_time_val = val
                else:
                    new_params[k] = val
            except:
                pass
                
        print(f"--- DEBUG: Simulando '{target_nivel}' hasta t={final_time_val} con params: {new_params}")
        
        # Ejecutamos la simulación. Si tenemos final_time_val, lo pasamos explícitamente.
        if final_time_val is not None:
            stocks = model.run(params=new_params, final_time=final_time_val)
        else:
            stocks = model.run(params=new_params)
        
        response_bd = getModelAll()
        info_nivel = next((
            {"title": i[1], "nameLabelX": i[2], "nameLabelY": i[3], "nameNivel": i[5], "nameColor": i[6]} 
            for i in response_bd if i[5] == target_nivel
        ), None)
        
        if info_nivel:
            # Enviamos los datos como diccionario para que JS los entienda correctamente
            table_data = stocks[target_nivel].to_dict()
            
            return {
                'status': 'ok', 
                'graph': generate_graph_html(stocks, info_nivel),
                'table_data': table_data
            }
        
        return {'status': 'error', 'message': 'Nivel no encontrado en configuración BD'}

    except Exception as e:
        print(f"Error en simulación: {e}")
        return {'status': 'error', 'message': str(e)}