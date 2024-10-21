import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime


file_path = 'clientes_perdidos.csv'
data = pd.read_csv(file_path, skiprows=4)

drop_columns = ["Nombre", "Fecha de cierre prevista", "Empresa", "Persona", "Interesado en", "Embudo"]
data = data.drop(columns=drop_columns)
data = data.dropna(how='all')
data["Creado"] = pd.to_datetime(data["Creado"], errors='coerce')

# Configuración de la aplicación
st.title('Dashboard de Clientes - Academia de Inglés')
st.sidebar.header('Filtros')

# Filtro por asignacion
persona = data['Asignado a'].dropna().unique()
persona_seleccionada = st.sidebar.multiselect('Seleccionar persona', persona, default=persona)

# Filtrar datos según la selección del usuario
data_filtrada = data[data['Asignado a'].isin(persona_seleccionada)]

# Visualización de la distribución de clientes por provincia
st.subheader('Distribución de Clientes por Persona')
clientes_por_provincia = data_filtrada['Asignado a'].value_counts()
fig, ax = plt.subplots()
clientes_por_provincia.plot(kind='bar', ax=ax)
ax.set_ylabel('Número de Clientes')
st.pyplot(fig)

# Mostrar tabla de datos filtrados
st.subheader('Datos de Clientes perdidos')
st.write(data_filtrada[['Etapa', 'Creado', 'Tags', 'Estado']])

# Gráfico de inscripciones a lo largo del tiempo
st.subheader('Tendencias de Inscripción de Clientes')
inscripciones_por_fecha = data_filtrada.groupby(data_filtrada['Creado'].dt.to_period('M')).size()
st.line_chart(inscripciones_por_fecha)

